from kedro.pipeline import Pipeline, node
from .nodes import recommand_plant


def create_inference_pipeline() -> Pipeline:
    pipeline = Pipeline([
        node(func=recommand_plant,
             inputs=dict(user_data="user_data",
                         nn="nearest_neighbors",
                         preprocessor="recommendation_preprocessor",
                         plants_dataset="recommendation_dataset"),
             outputs="recommendations",
             name="recommend_plants_node"
             ),
    ])

    return pipeline
