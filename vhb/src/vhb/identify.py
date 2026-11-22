from __future__ import annotations

import os
from dataclasses import dataclass

from vastai import VastAI

from vhb.models import InstanceInfo, IdentifyConfig

def _instance_host(instance: dict) -> str:
    return (
        instance.get("public_ipaddr")
        or instance.get("ssh_host")
        or instance.get("host")
    )


def _instance_port(
    instance: dict,
) -> int | None:
    return (
        instance.get("ssh_port")
        or instance.get("ports", {})
        .get("22/tcp", [{}])[0]
        .get("HostPort")
        or None
    )


def identify(
    config: IdentifyConfig | None = None,
) -> InstanceInfo:

    config = (
        config
        if config is not None
        else IdentifyConfig.from_env()
    )

    #
    # Manual override
    #

    if config.host and config.port:
        return InstanceInfo(
            id=-1,
            host=config.host,
            port=config.port,
            label="manual",
            status="manual",
        )

    #
    # API configuration
    #

    if not config.api_key:
        raise RuntimeError(
            "VASTAI_API_KEY is required."
        )

    vast = VastAI(
        api_key=config.api_key
    )

    #
    # Instance ID mode
    #

    if config.instance_id is not None:

        instance = vast.show_instance(
            config.instance_id
        )

        return InstanceInfo(
            id=instance["id"],
            host=_instance_host(
                instance
            ),
            port=_instance_port(
                instance
            ),
            label=instance.get(
                "label"
            ),
            status=instance.get(
                "actual_status"
            ),
        )

    #
    # Query all instances
    #

    instances = vast.show_instances()

    running = [
        instance
        for instance in instances
        if instance.get(
            "actual_status"
        ) == "running"
    ]

    #
    # Label mode
    #

    if config.instance_label:

        matches = [
            instance
            for instance in running
            if instance.get("label")
            == config.instance_label
        ]

        matches.sort(
            key=lambda x: x["id"]
        )

        if (
            config.instance_index
            >= len(matches)
        ):
            raise RuntimeError(
                f"No instance found for label "
                f"'{config.instance_label}' "
                f"at index "
                f"{config.instance_index}"
            )

        instance = matches[
            config.instance_index
        ]

    #
    # Automatic discovery
    #

    else:

        if not running:
            raise RuntimeError(
                "No running Vast.ai instances found."
            )

        running.sort(
            key=lambda x: x["id"]
        )

        instance = running[0]

    return InstanceInfo(
        id=instance["id"],
        host=_instance_host(
            instance
        ),
        port=_instance_port(
            instance
        ),
        label=instance.get(
            "label"
        ),
        status=instance.get(
            "actual_status"
        ),
    )