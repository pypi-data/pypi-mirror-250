# Lightning RL

Implementation of Reinforcement Learning algorithms using PyTorch Lightning, TorchRL and MLFlow.

The code structure was influenced by implementations in:

- [CleanRL](https://github.com/vwxyzjn/cleanrl/tree/master)
- [Lizhi-sjtu](https://github.com/Lizhi-sjtu/DRL-code-pytorch)
- [lightning_bolts](https://github.com/Lightning-Universe/lightning-bolts/tree/master/src/pl_bolts/models/rl)

Specific algorithms were also influenced by:

- SAC: [Haarnooja SAC](https://github.com/haarnoja/sac)
- Online Decision Transformer: [ODT](https://github.com/facebookresearch/online-dt)
- AlphaGo/Zero/MuZero: [Muzero](https://github.com/werner-duvaud/muzero-general)

## Demo

![Demo](demo.html)

## Get Started

LitRL currently only supports python-3.11.6. To install the dependencies, run:

```bash
pip install litrl[all]
```

:warning: The code relies partially on the **torchrl** and **tensordict** libraries, which can have installation problems. The solution is to download the package directly from source, then download litrl without the extra dependencies.

```bash
pip install 'tensordict @ git+https://github.com/pytorch/tensordict.git@c3caa7612275306ce72697a82d5252681ddae0ab'
pip install 'torchrl @ git+https://github.com/pytorch/rl.git@1bb192e0f3ad9e7b8c6fa769bfa3bb9d82ca4f29'
pip install litrl
```

## Developing

```bash
# Ensure you have python==3.11.6
make .venv
source .venv/bin/activate
bash scripts/train/sac_connect4.sh
```

## TODO

reproducibility

integration test with boring multiagent env

repoduce.py on huggingface that makes dockerfile etc...

throw errors if config in hydra not in schema

commitizen bump

list of validation opponents (MCTS50, MCTS500, MCTS5000)

code coverage

val run n times instead of rolling window

Add Pong environment for CNN processing

## Future features

Implement Rainbow
Implement ODT
AlphaGoOffline
AlphaZero
MuZero
