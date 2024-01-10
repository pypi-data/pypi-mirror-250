import warnings
from abc import ABC
from typing import Generic, Literal, Protocol, Self, TypedDict, TypeVar, runtime_checkable

with warnings.catch_warnings():
    warnings.filterwarnings(action="ignore", category=DeprecationWarning)
    from nptyping import Shape

from typing import Any

from gymnasium.spaces import Space
from pettingzoo.utils import agent_selector  # type: ignore[import-untyped]

SingleAgentId = Literal["CartPole-v1", "LunarLander-v2"]
MultiAgentId = Literal["ConnectFour-v3"]
EnvId = SingleAgentId | MultiAgentId
ActType = TypeVar("ActType")
ObsType = TypeVar("ObsType")
MaskType = TypeVar("MaskType")
ObsType_co = TypeVar("ObsType_co", covariant=True)
EnvType = TypeVar("EnvType")
ObsShape = TypeVar("ObsShape", bound=Shape)
MaskShape = TypeVar("MaskShape")
AgentID = TypeVar("AgentID")


class MaskedObs(TypedDict, Generic[ObsType, MaskType]):
    obs: ObsType  # NDArray[ObsShape, Float64]
    action_mask: MaskType  # NDArray[Shape[MaskShape], Int64]


class MaskedInfo(TypedDict, Generic[MaskType]):
    action_mask: MaskType  # NDArray[MaskShape, Int64]


@runtime_checkable
class SingleAgentEnv(Protocol, Generic[ObsType_co, ActType]):
    """Gym environments interface.

    We use this class to facilitate typing consistency within the LitRL codebase.
    The API remains the same as in OpenAI Gym.
    """

    @property
    def action_space(self) -> Space[ActType]:
        ...

    def __init__(self, env_id: EnvId, **kwargs: Any) -> None:
        ...

    def step(
        self,
        action: ActType,
    ) -> tuple[ObsType_co, float, bool, bool, dict[str, Any]]:
        ...

    def reset(
        self,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[ObsType_co, dict[str, Any]]:
        ...


class MultiAgentEnv(ABC, Generic[ObsType_co, ActType, AgentID]):
    """PettingZoo environments are not very mature yet and yield unexpected bugs.

    LitRL environments follow the gym/pettingzoo API as closely as possible,
    but we ensure the environments are stable by converting them to a MultiAgentEnv class.
    """

    agent_selection: AgentID
    unwrapped: Self
    truncations: dict[str, int]
    terminations: dict[str, int]
    infos: dict[str, Any]
    _cumulative_rewards: dict[str, float]
    rewards: dict[str, float]
    _agent_selector: agent_selector

    def step(self, action: ActType) -> None:
        raise NotImplementedError

    def last(self) -> tuple[ObsType_co, float, bool, bool, dict[str, Any]]:
        raise NotImplementedError

    def observe(self, agent: AgentID) -> ObsType_co:
        raise NotImplementedError

    def action_space(self, agent: AgentID) -> Space[ActType]:
        raise NotImplementedError

    def reset(
        self,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> None:
        raise NotImplementedError
