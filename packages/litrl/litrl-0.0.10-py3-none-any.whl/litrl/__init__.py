import warnings

from pydantic.warnings import PydanticDeprecatedSince20

from litrl.env.make import make, make_multiagent

warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20, module="mlflow")
warnings.filterwarnings(
    "ignore",
    category=PydanticDeprecatedSince20,
    module="huggingface_hub",
)

__version__ = "0.0.10"
__all__ = ["make", "make_multiagent"]
