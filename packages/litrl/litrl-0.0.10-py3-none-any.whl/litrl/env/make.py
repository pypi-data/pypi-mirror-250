from copy import deepcopy
from typing import Any

import gymnasium as gym
from gymnasium.core import ActType, ObsType
from gymnasium.wrappers.record_episode_statistics import RecordEpisodeStatistics
from loguru import logger

from litrl.algo.mcts.typing import MctsEnv
from litrl.env.connect_four import ConnectFour
from litrl.env.typing import EnvId, MultiAgentId
from litrl.wrappers import ClipRewardWrapper, StaticOpponentWrapper, ValidationWrapper


def make_multiagent(
    id: MultiAgentId,  # noqa: A002
    **kwargs: Any,
) -> ConnectFour:
    del id
    return ConnectFour(**kwargs)


def make(
    id: EnvId,  # noqa: A002
    *,
    val: bool = False,
    **kwargs: Any,
) -> gym.Env[ActType, ObsType]:
    logger.debug(f"Creating environment: {id}")
    render_mode = "rgb_array" if val else kwargs.pop("render_mode", None)
    render_each_n_episodes = kwargs.pop("render_each_n_episodes", 1)
    opponent = kwargs.pop("opponent", None)
    match id:
        case "CartPole-v1":
            env = gym.make(id="CartPole-v1", render_mode=render_mode, **kwargs)
        case "ConnectFour-v3":
            env = StaticOpponentWrapper(
                ConnectFour(render_mode=render_mode, **kwargs),
                opponent=opponent,
            )
        case "LunarLander-v2":
            env = ClipRewardWrapper(
                env=gym.make(id="LunarLander-v2", render_mode=render_mode, **kwargs),
                min_reward=-1,
            )
        case _:
            message = f"Unsupported environment: {id}"
            raise ValueError(message)
    env = RecordEpisodeStatistics(env=env)
    if val:
        env = ValidationWrapper(env=env, render_each_n_episodes=render_each_n_episodes)
    return env


def copy(env: MctsEnv) -> MctsEnv:
    if not isinstance(env, ConnectFour):
        raise NotImplementedError
    copied_env = ConnectFour()
    copied_env.agent_selection = deepcopy(env.unwrapped.agent_selection)
    copied_env.board = deepcopy(env.unwrapped.board)
    copied_env.truncations = deepcopy(env.unwrapped.truncations)
    copied_env.terminations = deepcopy(env.unwrapped.terminations)
    copied_env._agent_selector = deepcopy(env.unwrapped._agent_selector)
    copied_env.rewards = deepcopy(env.unwrapped.rewards)
    copied_env._cumulative_rewards = deepcopy(env.unwrapped._cumulative_rewards)
    copied_env.infos = deepcopy(env.unwrapped.infos)
    return copied_env
