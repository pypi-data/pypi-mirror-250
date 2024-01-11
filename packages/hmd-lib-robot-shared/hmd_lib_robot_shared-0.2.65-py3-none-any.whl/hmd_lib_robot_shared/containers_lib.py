import os
from typing import Dict, List
from robot.api.deco import keyword, library

from hmd_lib_containers.hmd_lib_containers import run_container as rc


@library
class ContainerLib:
    @keyword
    def run_container(
        self,
        image: str,
        name: str = None,
        entrypoint: str = None,
        command: List[str] = None,
        environment: Dict = {},
        volumes: List = [],
    ):
        rc(
            image,
            name=name,
            entrypoint=entrypoint,
            command=command,
            network="neuronsphere",
            environment=environment,
            volumes=volumes,
        )

    @keyword
    def run_transform_container(
        self,
        image: str,
        context: Dict,
        environment: Dict = {},
        volumes: List = [],
    ):
        volumes.append((os.environ["HMD_REPO_PATH"], "/hmd_transform/input"))
        volumes.append((os.environ["HMD_REPO_PATH"], "/hmd_transform/output"))

        environment["TRANSFORM_INSTANCE_CONTEXT"] = context

        rc(image, environment=environment, volumes=volumes)
