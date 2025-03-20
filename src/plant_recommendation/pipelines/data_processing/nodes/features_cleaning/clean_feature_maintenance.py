# CLEAN FEATURE 'MAINTENANCE'

import numpy as np
import pandas as pd

from typing import List, Any
from .clean_features import CleanFeatures


class CleanFeatureMaintenance(CleanFeatures):
    """
    A class used to clean the 'maintenance' feature in the plant dataset.

    Attributes:
        maintenance_col (str): The name of the column representing the maintenance level.
        imputation_features (List[str]): List of features used for imputation.
        maintenance_levels (List[str]): The levels of maintenance.
        care_levels (List[str]): The levels of care.
        care_level_col (str): The name of the column representing the care level.
        watering_col (str): The name of the column representing the watering frequency.
    """

    def __init__(self, maintenance_col: str, imputation_features: List[str],
                 maintenance_levels: List[str], care_levels: List[str], care_level_col: str, watering_col: str, **kwargs):
        """
        Initialize the CleanFeatureMaintenance class.

        Args:
            maintenance_col (str): The name of the column representing the maintenance level.
            imputation_features (List[str]): List of features used for imputation.
            maintenance_levels (List[str]): The levels of maintenance.
            care_levels (List[str]): The levels of care.
            care_level_col (str): The name of the column representing the care level.
            watering_col (str): The name of the column representing the watering frequency.
        """
        super().__init__(**kwargs)
        self.maintenance_col = maintenance_col
        self.imputation_features = imputation_features
        self.maintenance_levels = maintenance_levels
        self.care_levels = care_levels
        self.care_level_col = care_level_col
        self.watering_col = watering_col

    def impute_with_care_level(self, care_level: str) -> str:
        """
        Impute the maintenance level based on the care level.

        Args:
            care_level (str): The care level.

        Returns:
            str: The imputed maintenance level.
        """
        match care_level:
            case "medium":
                return "moderate"
            case "easy":
                return "low"
            case _:
                return care_level

    def impute_with_watering_frequency(self, watering_frequency: str) -> str:
        """
        Impute the maintenance level based on the watering frequency.

        Args:
            watering_frequency (str): The watering frequency.

        Returns:
            str: The imputed maintenance level.
        """
        match watering_frequency:
            case "average":
                return "moderate"
            case "minimum":
                return "low"
            case "frequent":
                return "high"
            case _:
                return watering_frequency

    def impute_with_feature(self, value_to_impute: Any, feature: str) -> Any:
        """
        Impute the maintenance level based on a given feature.

        Args:
            value_to_impute (Any): The value to impute.
            feature (str): The feature used for imputation.

        Returns:
            Any: The imputed value.
        """
        if feature == self.care_level_col:
            return self.impute_with_care_level(value_to_impute)
        elif feature == self.watering_col:
            return self.impute_with_watering_frequency(value_to_impute)
        else:
            return value_to_impute

    def impute(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Impute missing values in the maintenance column.

        Args:
            dataset (pd.DataFrame): The plant dataset to be imputed.

        Returns:
            pd.DataFrame: The dataset with imputed values.
        """
        cleaned_dataset = dataset.copy()

        for feature in self.imputation_features:
            maintenance_null = (cleaned_dataset[self.maintenance_col].isnull())
            feature_not_null = (~cleaned_dataset[feature].isnull())

            mask = maintenance_null & feature_not_null
            cleaned_dataset.loc[mask, self.maintenance_col] = cleaned_dataset.loc[mask, feature].apply(
                lambda x: self.impute_with_feature(x, feature))

        return cleaned_dataset

    def clean(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the 'maintenance' feature in the dataset.

        Args:
            dataset (pd.DataFrame): The plant dataset to be cleaned.

        Returns:
            pd.DataFrame: The cleaned dataset.
        """
        cleaned_dataset = dataset.copy()
        cleaned_dataset = self.replace_outliers_with_nan(
            cleaned_dataset, self.maintenance_col, self.maintenance_levels)
        cleaned_dataset = self.replace_outliers_with_nan(
            cleaned_dataset, self.care_level_col, self.care_levels)
        cleaned_dataset = self.impute(cleaned_dataset)

        return cleaned_dataset
