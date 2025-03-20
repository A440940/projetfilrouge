from kedro.pipeline import Pipeline, node
from .nodes import prepare_data, fit_preprocessor, fit_nn


def create_training_pipeline() -> Pipeline:
    pipeline = Pipeline([
        node(func=prepare_data,
             inputs=dict(dataset="clean_dataset",
                         col_to_drop="params:COLUMNS_TO_DROP",
                         poisonous_col="params:POISONOUS_COL"),
             outputs=["X", "recommendation_dataset"],
             name="prepare_data_for_knn_training_node"
             ),

        node(func=fit_preprocessor,
             inputs=dict(X="X"),
             outputs="recommendation_preprocessor",
             name="fit_preprocessor_node"
             ),

        node(func=fit_nn,
             inputs=dict(X="X",
                         fitted_preprocessor="recommendation_preprocessor",
                         n_neighbors="params:K_NEIGHBORS"),
             outputs="nearest_neighbors",
             name="fit_nearest_neighbors_node"
             ),
    ])

    return pipeline
