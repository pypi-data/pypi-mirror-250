import os
from typing import Any, Callable, Dict, Iterable, Optional, Set, Union
from seaplane.config import config
from seaplane.errors import SeaplaneError

from seaplane.sdk_internal_utils.buckets import create_bucket_if_needed

from .executor import execute


"""
SDK Tasks are mapped to Seaplane flows. To define a flow, use code like the following:

# Tasks live in the scope of an app, which is also a unit
# of task deployment.
app = seaplane.pipes.App("my-app")

def repeat_input(context):
    # This code will be run on the seaplane infrastructure.
    # The context will contain messages from upstream
    # in Seaplane carrier, and this code will yield
    # messages to its downstream listeners
    repeated = context.body + context.body
    yield repeated

repeat_input_task = app.task(repeat_input)

# To wire the flow into other flows, use app.edge()

# read input messages from the seaplane input endpoint
app.edge(app.input(), repeat_input_task)

# push the results to the seaplane output endpoint
app.edge(repeat_input_task, app.output())
"""


class Subject:
    """
    Subject is a base pubsub subject.

    Subject should represent a concrete, publishable subject - it can
    contain fun ${! meta} macros, but should not contain wildcards.

    Tasks can write to subjects but not subscribe to them.

    app.edge(my_task, Subject("known-stream.explicit-subject"))
    """

    def __init__(self, subject: str):
        self.subject = subject

    def __hash__(self) -> int:
        return hash(self.subject)

    def __eq__(self, other: Any) -> Any:
        return self.subject == other.subject


class Subscription:
    """
    The possibly-filtered name of a subject, for matching.

    Should not ever contain macros and things, but may contain wildcards.

    Tasks can subscribe to Subscriptions but not write to them.

    app.edge(Subscription("known-stream.explicit-subscription.>"), my_task)
    """

    def __init__(self, filter: str, deliver: str = "all"):
        self.filter = filter
        self.deliver = deliver

    def __hash__(self) -> int:
        return hash(self.filter)

    def __eq__(self, other: Any) -> Any:
        return self.filter == other.filter

    def stream(self) -> str:
        return self.filter.split(".", 1)[0]


class OutEndpoint(Subject):
    """The output seaplane endpoint. Does not accept subscriptions."""

    def __init__(self, endpoint: str):
        super(OutEndpoint, self).__init__(
            f"_SEAPLANE_ENDPOINT.out.{endpoint}."
            '${! meta("_seaplane_output_id") }'
            '${! meta("_seaplane_batch_hierarchy") }'
        )


class InEndpoint(Subscription):
    """
    Endpoint represents the Subject of a seaplane input endpoint.

    Unlike most subscriptions, apps subscribing to the seaplane endpoint are
    configured to receive only new messages, rather than pull all messages
    from their upstream peers in order.
    """

    def __init__(self, endpoint: str):
        super(InEndpoint, self).__init__(f"_SEAPLANE_ENDPOINT.in.{endpoint}.>", deliver="new")
        self.endpoint = endpoint


class _FlowSubject(Subject):
    """Task subjects conform to a standard format

    app.task.address-tag.output_id.batch.batch.batch
    """

    def __init__(self, app_name: str, instance_name: str):
        self.app_name = app_name
        self.instance_name = instance_name
        super(_FlowSubject, self).__init__(
            f"{app_name}.{instance_name}"
            '.${! meta("_seaplane_address_tag") }'
            '.${! meta("_seaplane_output_id") }'
            '${! meta("_seaplane_batch_hierarchy") }'
        )

    # TODO support output addresses in customer code
    def flow_subscription(self, address: str) -> Subscription:
        """use address = '*' to match all outputs from this task"""
        return Subscription(f"{self.app_name}.{self.instance_name}.{address}.>")


class Bucket:
    """
    A reference to a bucket and it's associated notification subscription.

    Get a bucket by asking the app to query the Seaplane infrastructure, like this:

    app = App("bucket-demo-app")

    # This queries the Seaplane infrastructure, and may creaet a bucket
    # if one doesn't exist already
    bucket = app.bucket("bucket-demo-bucket")

    app.edge(bucket, task)
    """

    def __init__(self, name: str, notify: str):
        self.name = name
        self.notify_subscription = Subscription(notify)


class Flow:
    """
    Description of deployment intent associated with a Seaplane flow.

    Create flows through an App, like this

    app = App("task-demo")

    def do_it(context):
        print("done!")

    my_task = app.flow(do_it)
    """

    def __init__(
        self,
        app: "App",
        work: Callable[..., Any],
        instance_name: str,
        subject: _FlowSubject,
        replicas: int,
        ack_wait_secs: int,
    ):
        # Note that app is a circular reference, so Tasks will not be GC'd
        self.app = app
        self.work = work
        self.instance_name = instance_name
        self.subject: Subject = subject  # task output
        self.replicas = replicas
        self.ack_wait_secs = ack_wait_secs
        self.subscriptions: Set[Subscription] = set()  # pull input from these subjects

    def subscribe(self, source: Subscription) -> None:
        self.subscriptions.add(source)


EdgeFrom = Union[Flow, Subscription]
EdgeTo = Union[Flow, Subject]


class App:
    """
    App is a namespace and unit of deployment for
    a collection of Tasks. Apps create a namespace for task messages
    and manage deployment together.
    """

    # Global registry of all known apps.
    _REGISTRY: Dict[str, "App"] = {}

    def __init__(self, name: str, name_prefix: Optional[str] = None):
        """Create a new `App`.

        Creates a new `App` named `name`. Initializes an empty task
        registry and registers the app in the process-wide registry.

        if name_prefix is provided, stream and task names will use that
        prefix.
        """
        if name_prefix is None:
            name_prefix = config.name_prefix

        self.name_prefix = name_prefix
        self.name = name_prefix + name
        self.buckets: Set[Bucket] = set()
        self.flow_registry: Dict[str, Flow] = {}
        self._REGISTRY[name] = self
        self.input_endpoint = InEndpoint(self.name)
        self.output_endpoint = OutEndpoint(self.name)

    @classmethod
    def all(cls) -> Iterable["App"]:
        return cls._REGISTRY.values()

    def flow(
        self,
        work: Callable[..., Any],
        instance_name: Optional[str] = None,
        replicas: int = 1,
        ack_wait_secs: int = 8 * 60,
    ) -> Flow:
        if instance_name is None:
            instance_name = work.__name__.replace("_", "-") + "-default"

        prefixed_name = self.name_prefix + instance_name

        if prefixed_name in self.flow_registry:
            raise SeaplaneError(
                f"duplicate task name {prefixed_name} in app {self.name}."
                " Try providing a unique instance_name argument when you create your task"
            )

        subject = _FlowSubject(self.name, prefixed_name)
        ret = Flow(self, work, prefixed_name, subject, replicas, ack_wait_secs)
        self.flow_registry[ret.instance_name] = ret
        return ret

    def input(self) -> InEndpoint:
        """Return the "in" `Endpoint` for this App."""
        return self.input_endpoint

    def output(self) -> OutEndpoint:
        """Return the "out" `Endpoint` for this App."""
        return self.output_endpoint

    def bucket(self, bucket_name: str) -> Bucket:
        """
        Return a notify-capable bucket.

        Makes a network request to the Seaplane object store. Will
        attempt to create a new bucket if one doesn't exist, and may
        fail with an Exception if there is a service failure or if
        the named bucket exists but is not configured to send notifications.
        """

        notify = create_bucket_if_needed(self.name, bucket_name)
        b = Bucket(bucket_name, notify)
        self.buckets.add(b)
        return b

    def edge(
        self,
        source: EdgeFrom,
        dest: EdgeTo,
    ) -> None:
        """
        Add an edge from a to b, binding b to a's output.

        Tasks can be wired to publish informatino to other tasks and explicit subjects.
        Tasks can be wired to recieve information from other tasks or subscriptions.
        At least one of source or dest must be a Task.
        """

        if not (isinstance(source, Flow) or isinstance(dest, Flow)):
            raise RuntimeError("edges must pass through a task")

        if isinstance(source, Subject):
            raise SeaplaneError(
                "the first argument to edge must be a Task, Bucket, or Subscription"
            )

        if isinstance(dest, Subscription):
            raise SeaplaneError("the second argument to edge must be a Task or a Subject")

        if isinstance(source, Flow) and isinstance(dest, Flow):
            # TODO the lhs of an edge should be parameterized by the address
            # TODO already, so do some similar "Subscription" -> "AddressedSubscription"
            # TODO foolery here.
            if isinstance(source.subject, _FlowSubject):
                # This is a typical, addresssable subject that we know how to match
                source = source.subject.flow_subscription("*")
            else:
                raise SeaplaneError(
                    f"can't listen to task subject {source.subject.subject} automatically."
                    " To listen to this, you'll need to use an explicit Subscription"
                    " and write the Seaplane carrier filter yourself"
                )

        if isinstance(source, Flow) and isinstance(dest, Subject):
            source.subject = dest

        elif isinstance(source, Subscription) and isinstance(dest, Flow):
            dest.subscribe(source)
        else:
            raise AssertionError("unreachable")

    def run(self) -> None:
        """
        Run the application as the main work of a process.

        Reads command line arguments and the INSTANCE_NAME environment variable. If INSTANCE_NAME
        is present, will attempt to execute the associated task, otherwise will
        print out the structure of the application.
        """
        # This has a bunch of circular dependencies but the ergonomics of `app.run()`
        # seem to make it worthwhile.
        import sys
        import tabulate
        import toml

        import seaplane.deploy
        import seaplane.run_load_dotenv

        command = None
        if len(sys.argv) > 1:
            command = sys.argv[1]

        instance_name = os.getenv("INSTANCE_NAME")

        if command == "deploy":
            pyproject = toml.loads(open("pyproject.toml", "r").read())
            project_directory_name = pyproject["tool"]["poetry"]["name"]
            seaplane.deploy.deploy(self, project_directory_name)
        elif command == "destroy":
            seaplane.deploy.destroy(self)
        elif instance_name:
            task = self.flow_registry[instance_name]
            execute(task.instance_name, task.work)
        else:
            rows = []
            for task in self.flow_registry.values():
                rows.append(
                    (
                        ",".join(x.filter for x in task.subscriptions),
                        "=>",
                        task.instance_name,
                        "->",
                        task.subject.subject,
                    )
                )
            print(tabulate.tabulate(rows, headers=["input", "", "task", "", "output"]))
