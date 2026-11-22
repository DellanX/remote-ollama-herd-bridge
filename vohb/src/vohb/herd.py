from fleet_manager.cli.node_cli import start as start_herd_node

from vohb.models import HerdConfig

def start_herd(
    ollama_host: str,
    config: HerdConfig | None = None,
) -> None:
    config = config if config is not None else HerdConfig.from_env()
    start_herd_node(
        ollama_host=ollama_host,
        node_id=config.node_id,
        router_url=config.router_url,
        learn_capacity=config.learn_capacity,
        log_level=config.log_level,
    )