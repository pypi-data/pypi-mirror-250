from typing import Any

from lightning.pytorch.loggers import MLFlowLogger


class LitRLLogger(MLFlowLogger):
    def __init__(
        self,
        run_id: str | None = None,
        tags: dict[str, Any] | None = None,
        save_dir: str = "./temp/mlruns",
        *,
        log_model: bool = True,
    ) -> None:
        super().__init__(
            tracking_uri=save_dir,
            artifact_location=save_dir,
            save_dir=save_dir,
            tags=tags,
            log_model=log_model,
            run_id=run_id,
        )
        self._save_dir = save_dir  # type: ignore[attr-defined]

    @property
    def save_dir(self) -> str:
        return self._save_dir
