from dataclasses import dataclass

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
