import pandas as pd

from typing import List, Dict, Any
from .features_engineering import add_attracts_col, add_perennial_col

from .features_cleaning.clean_features import CleanFeatures
from .features_cleaning.clean_feature_maintenance import CleanFeatureMaintenance
from .features_cleaning.clean_feature_type import CleanFeatureType
from .features_cleaning.clean_feature_sunlight import CleanFeatureSunlight
from .features_cleaning.clean_feature_hardiness import CleanFeatureHardiness


def select_relevant_features(dataset: pd.DataFrame, relevant_features: List[str]) -> pd.DataFrame:
    """
    Select relevant features from the dataset.

    Args:
        dataset (pd.DataFrame): The plant dataset.
        relevant_features (List[str]): List of relevant feature names to select.

    Returns:
        pd.DataFrame: The dataset with only the relevant features.
    """
    return dataset[relevant_features]


def clean_several_features(dataset: pd.DataFrame, features_to_lower: List[str], list_features: List[str], boolean_features: Dict[str, bool], id_col: str) -> pd.DataFrame:
    """
    Clean several features in the dataset.

    Args:
        dataset (pd.DataFrame): The plant dataset.
        features_to_lower (List[str]): List of feature names to convert to lowercase.
        list_features (List[str]): List of feature names that are lists.
        boolean_features (Dict[str, bool]): Dictionary mapping feature names to their default boolean values.
        id_col (str): The name of the column representing the ID.

    Returns:
        pd.DataFrame: The cleaned dataset.
    """
    cleaner = CleanFeatures(features_to_lower=features_to_lower,
                            list_features=list_features, boolean_features=boolean_features, id_col=id_col)
    return cleaner.clean(dataset)


def clean_feature_type(dataset: pd.DataFrame, type_col: str, type_to_plant: Dict[str, List[str]], imputation_file: str, id_col: str) -> pd.DataFrame:
    """
    Clean the 'type' feature in the dataset.

    Args:
        dataset (pd.DataFrame): The plant dataset.
        type_col (str): The name of the column representing the type information.
        type_to_plant (Dict[str, List[str]]): A dictionary mapping types to lists of plants.
        imputation_file (str): The path to the file used for imputation.
        id_col (str): The name of the column representing the ID.

    Returns:
        pd.DataFrame: The cleaned dataset.
    """
    cleaner = CleanFeatureType(type_col=type_col, type_to_plant=type_to_plant,
                               imputation_file=imputation_file, id_col=id_col)
    return cleaner.clean(dataset)


def clean_feature_sunlight(dataset: pd.DataFrame, sunlight_col: str, full_sun: List[str], full_shade: List[str]) -> pd.DataFrame:
    """
    Clean the 'sunlight' feature in the dataset.

    Args:
        dataset (pd.DataFrame): The plant dataset.
        sunlight_col (str): The name of the column representing the sunlight information.
        full_sun (List[str]): List of values representing full sun conditions.
        full_shade (List[str]): List of values representing full shade conditions.

    Returns:
        pd.DataFrame: The cleaned dataset.
    """
    cleaner = CleanFeatureSunlight(
        sunlight_col=sunlight_col, full_sun=full_sun, full_shade=full_shade)
    return cleaner.clean(dataset)


def clean_feature_hardiness(dataset: pd.DataFrame, imputation_file: str, rename_dict: Dict[str, str], min_col: str, max_col: str, hardiness_levels: List[str], id_col: str) -> pd.DataFrame:
    """
    Clean the 'hardiness' feature in the dataset.

    Args:
        dataset (pd.DataFrame): The plant dataset.
        imputation_file (str): The path to the file used for imputation.
        rename_dict (Dict[str, str]): A dictionary for renaming columns.
        min_col (str): The name of the column representing the minimum hardiness.
        max_col (str): The name of the column representing the maximum hardiness.
        hardiness_levels (List[str]): The levels of hardiness.
        id_col (str): The name of the column representing the ID.

    Returns:
        pd.DataFrame: The cleaned dataset.
    """
    cleaner = CleanFeatureHardiness(imputation_file=imputation_file, rename_dict=rename_dict, hardiness_min_col=min_col, hardiness_max_col=max_col,
                                    hardiness_levels=hardiness_levels, id_col=id_col)
    return cleaner.clean(dataset)


def clean_feature_maintenance(dataset: pd.DataFrame, maintenance_col: str, imputation_features: List[str], maintenance_levels: List[str],
                              care_levels: List[str], care_level_col: str, watering_col: str) -> pd.DataFrame:
    """
    Clean the 'maintenance' feature in the dataset.

    Args:
        dataset (pd.DataFrame): The plant dataset.
        maintenance_col (str): The name of the column representing the maintenance level.
        imputation_features (List[str]): List of features used for imputation.
        maintenance_levels (List[str]): The levels of maintenance.
        care_levels (List[str]): The levels of care.
        care_level_col (str): The name of the column representing the care level.
        watering_col (str): The name of the column representing the watering frequency.

    Returns:
        pd.DataFrame: The cleaned dataset.
    """
    cleaner = CleanFeatureMaintenance(maintenance_col=maintenance_col, imputation_features=imputation_features,
                                      maintenance_levels=maintenance_levels, care_levels=care_levels, care_level_col=care_level_col,
                                      watering_col=watering_col)
    return cleaner.clean(dataset)


def add_new_features(dataset: pd.DataFrame, new_features: Dict[str, Dict[str, Any]], cycle_col: str, attracts_col: str, features_to_drop: List[str]) -> pd.DataFrame:
    """
    Add new features to the dataset.

    Args:
        dataset (pd.DataFrame): The plant dataset.
        new_features (Dict[str, Dict[str, Any]]): A dictionary mapping new feature names to their corresponding values to test.
        cycle_col (str): The name of the column representing the plant cycle.
        attracts_col (str): The name of the column representing the animals the plant attracts.
        features_to_drop (List[str]): List of feature names to drop.

    Returns:
        pd.DataFrame: The dataset with the new features added.
    """
    new_dataset = add_perennial_col(dataset, cycle_col, new_features)
    new_dataset = add_attracts_col(new_dataset, attracts_col, new_features)

    return new_dataset.drop(columns=features_to_drop)
