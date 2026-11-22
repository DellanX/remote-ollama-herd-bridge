from dataclasses import dataclass
import os

@dataclass
class Context:
    instance_id: str | None = None

    host: str | None = None
    port: int | None = None

    ssh_pid: int | None = None
    herd_pid: int | None = None

@dataclass
class InstanceInfo:
    id: int
    host: str
    port: int | None
    label: str | None = None
    status: str | None = None

@dataclass
class IdentifyConfig:
    host: str | None = None
    port: int | None = None

    api_key: str | None = None

    instance_id: int | None = None

    instance_label: str | None = None
    instance_index: int = 0

    @classmethod
    def from_env(cls) -> "IdentifyConfig":
        instance_id = os.getenv("VASTAI_INSTANCE_ID")

        port = os.getenv("VASTAI_PORT")

        return cls(
            host=os.getenv("VASTAI_HOST"),
            port=int(port) if port else None,

            api_key=os.getenv("VASTAI_API_KEY"),

            instance_id=int(instance_id)
            if instance_id
            else None,

            instance_label=os.getenv(
                "VASTAI_INSTANCE_LABEL"
            ),

            instance_index=int(
                os.getenv(
                    "VASTAI_INSTANCE_INDEX",
                    "0",
                )
            ),
        )

@dataclass
class TunnelConfig:
    ssh_user: str = "root"

    ssh_identity_file: str | None = None

    local_host: str = "0.0.0.0"
    local_port: int = 11434

    remote_host: str = "localhost"
    remote_port: int = 11434

    wait_interval: float = 2
    wait_max_retries: int = 30

    @classmethod
    def from_env(cls) -> "TunnelConfig":
        return cls(
            ssh_user=os.getenv(
                "SSH_USER",
                "root",
            ),
            ssh_identity_file=os.getenv(
                "SSH_IDENTITY_FILE"
            ),
            local_host=os.getenv(
                "LOCAL_HOST",
                "0.0.0.0",
            ),
            local_port=int(
                os.getenv(
                    "LOCAL_PORT",
                    "11434",
                )
            ),
            remote_host=os.getenv(
                "REMOTE_HOST",
                "localhost",
            ),
            remote_port=int(
                os.getenv(
                    "REMOTE_PORT",
                    "11434",
                )
            ),
            wait_interval=float(
                os.getenv(
                    "WAIT_INTERVAL",
                    "2",
                )
            ),
            wait_max_retries=int(
                os.getenv(
                    "WAIT_MAX_RETRIES",
                    "30",
                )
            ),
        )

@dataclass
class HerdConfig:
    node_id: str | None = None
    router_url: str | None = None
    learn_capacity: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "HerdConfig":
        return cls(
            node_id=os.getenv(
                "NODE_ID"
            ),

            router_url=os.getenv(
                "ROUTER_URL"
            ),

            learn_capacity=os.getenv(
                "LEARN_CAPACITY",
                "false",
            ).lower() == "true",

            log_level=os.getenv(
                "LOG_LEVEL",
                "INFO",
            ),
        )

@dataclass
class RunConfig:
    identify: IdentifyConfig
    tunnel: TunnelConfig
    herd: HerdConfig