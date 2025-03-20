# CLEAN FEATURE 'SUNLIGHT'

import pandas as pd
from typing import List
from .clean_features import CleanFeatures


class CleanFeatureSunlight(CleanFeatures):
    """
    A class used to clean the 'sunlight' feature in the plant dataset.

    Attributes:
        sunlight_col (str): The name of the column representing the sunlight information.
        full_sun (List[str]): List of values representing full sun conditions.
        full_shade (List[str]): List of values representing full shade conditions.
    """

    def __init__(self, sunlight_col: str, full_sun: List[str], full_shade: List[str]):
        """
        Initialize the CleanFeatureSunlight class.

        Args:
            sunlight_col (str): The name of the column representing the sunlight information.
            full_sun (List[str]): List of values representing full sun conditions.
            full_shade (List[str]): List of values representing full shade conditions.
        """
        super().__init__()
        self.sunlight_col = sunlight_col
        self.full_sun = full_sun
        self.full_shade = full_shade

    def categorize_sunlight(self, x: List[str]) -> str:
        """
        Categorize the sunlight information.

        Args:
            x (List[str]): A list of sunlight information.

        Returns:
            str: The categorized sunlight information ('full_shade', 'full_sun', or 'part_shade').
        """
        for sunlight_info in x:
            if sunlight_info in self.full_shade:
                return "full_shade"
        for sunlight_info in x:
            if sunlight_info in self.full_sun:
                return "full_sun"
        return "part_shade"

    def clean(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the 'sunlight' feature in the dataset.

        Args:
            dataset (pd.DataFrame): The plant dataset to be cleaned.

        Returns:
            pd.DataFrame: The cleaned dataset.
        """
        cleaned_dataset = dataset.copy()
        cleaned_dataset.loc[:, self.sunlight_col] = cleaned_dataset[self.sunlight_col].apply(
            lambda x: self.categorize_sunlight(x))

        return cleaned_dataset
