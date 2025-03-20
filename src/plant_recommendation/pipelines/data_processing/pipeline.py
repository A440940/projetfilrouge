from kedro.pipeline import Pipeline, node
from .nodes.nodes import select_relevant_features, clean_several_features, clean_feature_hardiness, clean_feature_maintenance, clean_feature_sunlight, clean_feature_type, add_new_features


def create_data_processing_pipeline() -> Pipeline:
    pipeline_feature_selection = Pipeline([
        node(func=select_relevant_features,
             inputs=dict(dataset="raw_dataset",
                         relevant_features="params:RELEVANT_FEATURES"),
             outputs="filtered_raw_dataset",
             name="load_raw_dataset_node"
             )
    ])

    pipeline_feature_cleaning = Pipeline([
        node(func=clean_several_features,
             inputs=dict(dataset="filtered_raw_dataset",
                         features_to_lower="params:FEATURES_TO_LOWER",
                         boolean_features="params:BOOLEAN_FEATURES",
                         list_features="params:FEATURES_WITH_LISTS",
                         id_col="params:ID_COL"
                         ),
             outputs="cleaned_dataset_step1",
             name="normalize_node"
             ),

        node(func=clean_feature_maintenance,
             inputs=dict(dataset="cleaned_dataset_step1",
                         maintenance_col="params:MAINTENANCE_COL",
                         imputation_features="params:MAINTENANCE_IMPUTATION_FEATURES",
                         maintenance_levels="params:MAINTENANCE_LEVELS",
                         care_levels="params:CARE_LEVELS",
                         care_level_col="params:CARE_LEVEL_COL",
                         watering_col="params:WATERING_COL"
                         ),
             outputs="cleaned_dataset_step2",
             name="clean_feature_maintenance_node"
             ),

        node(func=clean_feature_type,
             inputs=dict(dataset="cleaned_dataset_step2",
                         type_col="params:TYPE_COL",
                         type_to_plant="params:TYPE_TO_PLANT",
                         imputation_file="type_imputation_file",
                         id_col="params:ID_COL",
                         ),
             outputs="cleaned_dataset_step3",
             name="clean_feature_type_node"
             ),

        node(func=clean_feature_sunlight,
             inputs=dict(dataset="cleaned_dataset_step3",
                         sunlight_col="params:SUNLIGHT_COL",
                         full_sun="params:FULL_SUN_LIST",
                         full_shade="params:FULL_SHADE_LIST",
                         ),
             outputs="cleaned_dataset_step4",
             name="clean_feature_sunlight_node"
             ),

        node(func=clean_feature_hardiness,
             inputs=dict(dataset="cleaned_dataset_step4",
                         imputation_file="hardiness_imputation_file",
                         rename_dict="params:FEATURES_TO_RENAME",
                         min_col="params:HARDINESS_MIN_COL",
                         max_col="params:HARDINESS_MAX_COL",
                         hardiness_levels="params:HARDINESS_LEVELS",
                         id_col="params:ID_COL"
                         ),
             outputs="cleaned_dataset_step5",
             name="clean_feature_hardiness_node"
             )
    ])

    pipeline_feature_engineering = Pipeline([
        node(func=add_new_features,
             inputs=dict(dataset="cleaned_dataset_step5",
                         new_features="params:NEW_FEATURES",
                         cycle_col="params:CYCLE_COL",
                         attracts_col="params:ATTRACTS_COL",
                         features_to_drop="params:FEATURES_TO_DROP"
                         ),
             outputs="clean_dataset",
             name="add_features_node"
             ),
    ])

    return (pipeline_feature_selection + pipeline_feature_cleaning + pipeline_feature_engineering)
