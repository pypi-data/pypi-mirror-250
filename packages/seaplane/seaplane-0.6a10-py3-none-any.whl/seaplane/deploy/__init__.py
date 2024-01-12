import os
import shutil
from typing import Any, Dict, List
from urllib.parse import urlparse

from seaplane.logs import log
from seaplane.pipes import App, Flow
from seaplane.config import config, runner_image

from .utils import (
    add_secrets,
    create_flow,
    create_store,
    create_stream,
    delete_flow,
    delete_store,
    delete_stream,
    upload_project,
)

"""
Tools for taking a fully constructed App / Task complex and deploying it
into the Seaplane infrastructure.

Call `deploy(app, project_directory_name)` to push your application to Seaplane.
"""


class ProcessorInfo:
    """Information about the docker container to run applications"""

    def __init__(self, runner_image: str, runner_args: List[str]):
        self.runner_image = runner_image
        self.runner_args = runner_args


def flow_into_config(flow: Flow, processor_info: ProcessorInfo) -> Dict[str, Any]:
    """Produces JSON.dump-able flow configuration suitable for running the given task"""

    ret = {
        "processor": {
            "docker": {
                "image": processor_info.runner_image,
                "args": processor_info.runner_args,
            }
        },
        "output": {
            "switch": {
                "cases": [
                    {
                        "check": 'meta("_seaplane_drop") == "True"',
                        "output": {"drop": {}},
                    },
                    {
                        "check": 'meta("_seaplane_drop") != "True"',
                        "output": {
                            "carrier": {
                                "subject": flow.subject.subject,
                            }
                        },
                    },
                ]
            }
        },
        "replicas": flow.replicas,
    }

    if len(flow.subscriptions) == 0:
        log.logger.warning(
            f"task {flow.instance_name} does not appear to consume any input, it may not run"
        )

    broker: List[Dict[str, Any]] = []
    for ix, src in enumerate(sorted(flow.subscriptions, key=lambda s: s.filter)):
        # this durable scheme means we're committed to destroying
        # the consumers associated with these flows on redeploy.
        # Future fancy hot-swap / live-update schemes may need
        # to use different durable names
        durable = f"{flow.instance_name}-{ix}"
        broker.append(
            {
                "carrier": {
                    "ack_wait": f"{flow.ack_wait_secs}s",
                    "bind": True,
                    "deliver": src.deliver,
                    "durable": durable,
                    "stream": src.stream(),
                    "subject": src.filter,
                },
            }
        )

    ret["input"] = {"broker": broker}

    return ret


def deploy(app: App, project_directory_name: str) -> None:
    """
    Runs a complete deploy of a given app.

    project_directory_name is the name of the directory, a peer to the
    pyproject.toml, that contains

    pyproject = toml.loads(open("pyproject.toml", "r").read())
    project_directory_name = pyproject["tool"]["poetry"]["name"]

    Will delete and recreate a "build" directory

    """
    shutil.rmtree("build/", ignore_errors=True)
    os.makedirs("build")

    project_url = upload_project(project_directory_name)
    processor_info = ProcessorInfo(runner_image(), [project_url])

    for bucket in app.buckets:
        delete_stream(bucket.notify_subscription.stream())
        create_stream(bucket.notify_subscription.stream())

    delete_stream(app.name)
    create_stream(app.name)

    delete_store(f"_SP_REQUEST_{app.name}")
    create_store(f"_SP_REQUEST_{app.name}")
    delete_store(f"_SP_RESPONSE_{app.name}")
    create_store(f"_SP_RESPONSE_{app.name}")

    for task in app.flow_registry.values():
        new_flow_config = flow_into_config(task, processor_info)
        delete_flow(task.instance_name)
        create_flow(task.instance_name, new_flow_config)

        secrets = {"INSTANCE_NAME": task.instance_name} | config._api_keys
        add_secrets(task.instance_name, secrets)

    use_input = any(
        any(subsc == app.input() for subsc in task.subscriptions)
        for task in app.flow_registry.values()
    )

    if use_input:
        log.logger.info(
            f"post to https://{urlparse(config.carrier_endpoint).netloc}"
            f"/v1/endpoints/{app.input().endpoint}/request"
        )
        log.logger.info("or run: seaplane request -d <data>")


def destroy(app: App) -> None:
    delete_stream(app.name)
    delete_store(f"_SP_REQUEST_{app.name}")
    delete_store(f"_SP_RESPONSE_{app.name}")

    for task in app.flow_registry.values():
        delete_flow(task.instance_name)
