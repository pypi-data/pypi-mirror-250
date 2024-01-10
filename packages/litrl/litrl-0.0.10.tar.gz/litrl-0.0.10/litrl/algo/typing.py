from abc import ABC
from typing import Any

import torch
from lightning import LightningModule
from torchrl.data.replay_buffers.replay_buffers import TensorDictReplayBuffer

from litrl.common.schema import ModelConfigSchema


class LitRLModule(LightningModule, ABC):
    default_config: ModelConfigSchema

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.buffer: TensorDictReplayBuffer
        self.obs: torch.Tensor
        self.cfg: ModelConfigSchema
