import pandas as pd
from typing import List, Dict, Any


def add_perennial_col(dataset: pd.DataFrame, cycle_col: str, new_features: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """
    Add a column indicating whether the plant is perennial based on the cycle column.

    Args:
        dataset (pd.DataFrame): The plant dataset.
        cycle_col (str): The name of the column representing the plant cycle.
        new_features (Dict[str, Dict[str, Any]]): A dictionary mapping new feature names to their corresponding values to test.

    Returns:
        pd.DataFrame: The dataset with the new perennial column added.
    """
    cleaned_dataset = dataset.copy()
    for new_feature, tested_value in new_features[cycle_col].items():
        cleaned_dataset.loc[:, new_feature] = cleaned_dataset[cycle_col].apply(
            lambda x: False if x == tested_value else True)
    return cleaned_dataset


def attracts(x: List[str], animals: List[str]) -> bool:
    """
    Check if the plant attracts certain animals.

    Args:
        x (List[str]): The list of animals the plant attracts.
        animals (List[str]): The list of animals to check.

    Returns:
        bool: True if the plant attracts any of the specified animals, False otherwise.
    """
    for attracted_being in x:
        if attracted_being in animals:
            return True
    return False


def add_attracts_col(dataset: pd.DataFrame, attracts_col: str, new_features: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """
    Add columns indicating whether the plant attracts certain animals.

    Args:
        dataset (pd.DataFrame): The plant dataset.
        attracts_col (str): The name of the column representing the animals the plant attracts.
        new_features (Dict[str, Dict[str, Any]]): A dictionary mapping new feature names to their corresponding animals to check.
    Returns:
        pd.DataFrame: The dataset with the new attracts columns added.
    """
    new_dataset = dataset.copy()
    for new_feature, tested_values in new_features[attracts_col].items():
        new_dataset.loc[:, new_feature] = new_dataset[attracts_col].apply(
            lambda x: attracts(x, tested_values))

    return new_dataset
