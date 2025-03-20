import numpy as np
import pandas as pd

from typing import List, Dict


class CleanFeatures:
    """
    A class used to clean various features in the plant dataset.

    Attributes:
        features_to_lower (List[str]): List of feature names to convert to lowercase.
        list_features (List[str]): List of feature names that are lists.
        boolean_features (Dict[str, bool]): Dictionary mapping feature names to their default boolean values.
        id_col (str): The name of the column representing the ID.
        imputation_file (str): The path to the file used for imputation.
    """

    def __init__(self, features_to_lower: List[str] = None, list_features: List[str] = None, boolean_features: Dict[str, bool] = None, id_col: str = None, imputation_file: str = None):
        """
        Initialize the CleanFeatures class.

        Args:
            features_to_lower (List[str], optional): List of feature names to convert to lowercase.
            list_features (List[str], optional): List of feature names that are lists.
            boolean_features (Dict[str, bool], optional): Dictionary mapping feature names to their default boolean values.
            id_col (str, optional): The name of the column representing the ID.
            imputation_file (str, optional): The path to the file used for imputation.
        """
        self.id_col = id_col
        self.features_to_lower = features_to_lower
        self.boolean_features = boolean_features
        self.list_features = list_features
        self.imputation_file = imputation_file

    def lower_str(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Convert specified string features to lowercase.

        Args:
            dataset (pd.DataFrame): The plant dataset to be cleaned.

        Returns:
            pd.DataFrame: The dataset with specified features converted to lowercase.
        """
        new_dataset = dataset.copy()
        for feature in self.features_to_lower:
            new_dataset.loc[:, feature] = new_dataset[feature].str.lower()
        return new_dataset

    def clean_list(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Clean specified list features by evaluating and converting to lowercase.

        Args:
            dataset (pd.DataFrame): The plant dataset to be cleaned.

        Returns:
            pd.DataFrame: The dataset with cleaned list features.
        """
        new_dataset = dataset.copy()
        for feature in self.list_features:
            new_dataset.loc[:, feature] = new_dataset[feature].apply(eval)
            new_dataset.loc[:, feature] = new_dataset[feature].apply(
                lambda x: [' '.join(s.lower().split()) for s in x])
        return new_dataset

    def str_to_boolean(self, x: str, default_value: bool) -> bool:
        """
        Convert a string to a boolean value.

        Args:
            x (str): The string to convert.
            default_value (bool): The default boolean value.

        Returns:
            bool: The converted boolean value.
        """
        if x == "TRUE":
            return True
        elif x == "FALSE":
            return False
        else:
            return default_value

    def clean_boolean(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Clean specified boolean features by converting strings to boolean values.

        Args:
            dataset (pd.DataFrame): The plant dataset to be cleaned.

        Returns:
            pd.DataFrame: The dataset with cleaned boolean features.
        """
        new_dataset = dataset.copy()
        for feature, default_value in self.boolean_features.items():
            new_dataset.loc[:, feature] = new_dataset[feature].apply(
                lambda x: self.str_to_boolean(x, default_value))
        return new_dataset

    def impute_with_file(self, dataset: pd.DataFrame, file: pd.DataFrame, impute_col: str) -> pd.DataFrame:
        """
        Impute missing values in the dataset using values from a file.

        Args:
            dataset (pd.DataFrame): The plant dataset to be imputed.
            file (pd.DataFrame): The file used for imputation.
            impute_col (str): The name of the column to impute.

        Returns:
            pd.DataFrame: The dataset with imputed values.
        """
        new_dataset = dataset.copy()
        new_dataset.loc[new_dataset[impute_col].isnull(), impute_col] = file[impute_col].values
        # for id in file[self.id_col]:
        #     print(id)
        #     new_dataset.loc[new_dataset[self.id_col]==id, impute_col] = file.loc[file[self.id_col]==id, impute_col]
        return new_dataset

    def replace_outliers_with_nan(self, dataset: pd.DataFrame, feature: str, regular_values: List[str]) -> pd.DataFrame:
        """
        Replace outliers in a feature with NaN.

        Args:
            dataset (pd.DataFrame): The plant dataset to be cleaned.
            feature (str): The name of the feature to clean.
            regular_values (List[str]): List of regular values.

        Returns:
            pd.DataFrame: The dataset with outliers replaced by NaN.
        """
        cleaned_dataset = dataset.copy()

        mask_outliers = (~cleaned_dataset[feature].isin(regular_values))
        cleaned_dataset.loc[mask_outliers, feature] = np.nan

        return cleaned_dataset

    def clean(self, dataset: pd.DataFrame):
        """
        Clean the dataset by applying various cleaning methods.

        Args:
            dataset (pd.DataFrame): The plant dataset to be cleaned.

        Returns:
            pd.DataFrame: The cleaned dataset.
        """
        cleaned_dataset = self.lower_str(dataset)
        cleaned_dataset = self.clean_list(cleaned_dataset)
        cleaned_dataset = self.clean_boolean(cleaned_dataset)

        return cleaned_dataset
