import uuid
from pathlib import Path
from typing import Literal, TypeAlias

import hydra
import mlflow
from loguru import logger
from omegaconf import DictConfig, OmegaConf

from litrl.common.mlflow import get_mlflow_run_id
from litrl.common.schema import ConfigSchema

EnvConfig: TypeAlias = Literal["cartpole", "connect_four", "default", "lunar_lander"]
ModelConfig: TypeAlias = Literal["masac", "sac"]
VERSION_BASE: str = "1.3.2"


def register_resolvers() -> None:
    mlflow.set_tracking_uri("./temp/mlruns/")
    OmegaConf.register_new_resolver(name="uuid", resolver=lambda _: uuid.uuid4().hex)
    OmegaConf.register_new_resolver(
        name="mlflow", resolver=lambda run_id: get_mlflow_run_id(run_id),
    )


def get_omegaconf(overrides: list[str] | None) -> DictConfig:
    with hydra.initialize_config_dir(
        config_dir=str(Path("config").absolute()),
        version_base=VERSION_BASE,
    ):
        return hydra.compose(config_name="default", overrides=overrides)


def omegaconf_to_schema(cfg: DictConfig) -> ConfigSchema:
    OmegaConf.resolve(cfg)
    logger.info(f"config is \n{OmegaConf.to_yaml(cfg)}")
    return ConfigSchema(**OmegaConf.to_container(cfg))
