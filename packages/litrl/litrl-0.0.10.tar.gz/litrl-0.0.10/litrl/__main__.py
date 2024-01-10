from pathlib import Path

import hydra
from lightning import LightningModule, Trainer
from omegaconf import DictConfig

from litrl.common.hydra import VERSION_BASE, omegaconf_to_schema, register_resolvers
from litrl.common.mlflow import get_load_path
from litrl.common.schema import ConfigSchema

register_resolvers()


@hydra.main(config_path="../config", config_name="default", version_base=VERSION_BASE)
def main(omegaconf_cfg: DictConfig) -> None:
    """Enter the project."""
    cfg: ConfigSchema = omegaconf_to_schema(cfg=omegaconf_cfg)
    load_path: Path | None = get_load_path(tags=cfg.tags, load=cfg.load_path)
    model: LightningModule = cfg.model.instantiate()
    trainer: Trainer = cfg.trainer.instantiate()
    trainer.fit(
        model=model,
        ckpt_path=str(load_path) if load_path is not None else None,
    )


if __name__ == "__main__":
    main()
