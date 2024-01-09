"""
Registered callbacks for sequence models.
"""

from pathlib import Path
from typing import Literal

from lightning.pytorch.callbacks import (
    Callback,
    EarlyStopping,
    LearningRateMonitor,
    ModelCheckpoint,
)
from snp_transformer.config import Registry


@Registry.callbacks.register("callback_list")
def create_callback_list(*args: Callback) -> list[Callback]:
    return list(args)


@Registry.callbacks.register("early_stopping")
def create_early_stopping(
    monitor: str = "Validation loss",
    min_delta: float = 0.0,
    patience: int = 10,
    verbose: bool = False,
    mode: Literal["min", "max"] = "min",
) -> EarlyStopping:
    return EarlyStopping(
        monitor=monitor,
        min_delta=min_delta,
        patience=patience,
        verbose=verbose,
        mode=mode,
    )


@Registry.callbacks.register("model_checkpoint")
def create_model_checkpoint(
    save_dir: Path,
    every_n_epochs: int = 1,
    save_top_k: int = 5,
    mode: Literal["min", "max"] = "min",
    monitor: str = "Validation loss",
) -> ModelCheckpoint:
    return ModelCheckpoint(
        dirpath=save_dir / "checkpoints",
        every_n_epochs=every_n_epochs,
        verbose=True,
        save_top_k=save_top_k,
        mode=mode,
        monitor=monitor,
    )


@Registry.callbacks.register("learning_rate_monitor")
def create_learning_rate_monitor(
    logging_interval: str = "epoch",
) -> LearningRateMonitor:
    return LearningRateMonitor(logging_interval=logging_interval, log_momentum=True)  # type: ignore
