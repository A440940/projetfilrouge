"""Project pipelines."""
from __future__ import annotations

from kedro.pipeline import Pipeline
from .pipelines.data_processing.pipeline import create_data_processing_pipeline
from .pipelines.training.pipeline import create_training_pipeline
from .pipelines.predict.pipeline import create_inference_pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    data_processing_pipeline = create_data_processing_pipeline()
    training_pipeline = create_training_pipeline()
    inference_pipeline = create_inference_pipeline()

    return {'inference': inference_pipeline,
            'training': data_processing_pipeline + training_pipeline,
            '__default__': inference_pipeline}
