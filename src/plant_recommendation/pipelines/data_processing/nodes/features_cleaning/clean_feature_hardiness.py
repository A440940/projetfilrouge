# CLEAN FEATURE 'HARDINESS'

import pandas as pd
from .clean_features import CleanFeatures
from typing import List, Dict


class CleanFeatureHardiness(CleanFeatures):
    """
    A class used to clean the 'hardiness' feature in the plant dataset.

    Attributes:
        min_col (str): The name of the column representing the minimum hardiness.
        max_col (str): The name of the column representing the maximum hardiness.
        levels (List[str]): The levels of hardiness.
        new_names (Dict[str, str]): A dictionary for renaming columns.
    """

    def __init__(self, rename_dict: Dict[str, str], hardiness_min_col: str, hardiness_max_col: str,
                 hardiness_levels: List[str], id_col: str = None, imputation_file: str = None):
        """
        Initialize the CleanFeatureHardiness class.

        Args:
            rename_dict (Dict[str, str]): A dictionary for renaming columns.
            hardiness_min_col (str): The name of the column representing the minimum hardiness.
            hardiness_max_col (str): The name of the column representing the maximum hardiness.
            hardiness_levels (List[str]): The levels of hardiness.
        """
        super().__init__(id_col=id_col, imputation_file=imputation_file)
        self.min_col = hardiness_min_col
        self.max_col = hardiness_max_col
        self.levels = hardiness_levels
        self.new_names = rename_dict

    def clean(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the 'hardiness' feature in the dataset.

        Args:
            dataset (pd.DataFrame): The plant dataset to be cleaned.

        Returns:
            pd.DataFrame: The cleaned dataset.
        """
        cleaned_dataset = dataset.copy()
        cleaned_dataset = cleaned_dataset.rename(columns=self.new_names)

        cleaned_dataset = self.replace_outliers_with_nan(
            cleaned_dataset, self.max_col, self.levels)
        
        cleaned_dataset[self.max_col] = cleaned_dataset[self.max_col].fillna(cleaned_dataset[self.min_col])

        cleaned_dataset.loc[:, self.max_col] = pd.to_numeric(
            cleaned_dataset[self.max_col])

        for feature in [self.max_col, self.min_col]:
            cleaned_dataset = self.impute_with_file(cleaned_dataset, self.imputation_file, feature)

        return cleaned_dataset
