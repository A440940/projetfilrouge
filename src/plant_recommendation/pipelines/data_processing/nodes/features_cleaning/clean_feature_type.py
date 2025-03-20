# CLEAN FEATURE 'TYPE'
import pandas as pd

from typing import List, Dict
from .clean_features import CleanFeatures


class CleanFeatureType(CleanFeatures):
    """
    A class used to clean the 'type' feature in the plant dataset.

    Attributes:
        type_col (str): The name of the column representing the type information.
        type_to_plant (Dict[str, List[str]]): A dictionary mapping types to lists of plants.
        plant_to_type (Dict[str, str]): A dictionary mapping plants to their types.
    """

    def __init__(self, type_col: str, type_to_plant: Dict[str, List[str]], id_col: str = None, imputation_file: str = None):
        """
        Initialize the CleanFeatureType class.

        Args:
            type_col (str): The name of the column representing the type information.
            type_to_plant (Dict[str, List[str]]): A dictionary mapping types to lists of plants.
        """
        super().__init__(id_col=id_col, imputation_file=imputation_file)
        self.type_col = type_col
        self.type_to_plant = type_to_plant
        self.plant_to_type = self.build_type_dictionary()

    def build_type_dictionary(self) -> Dict[str, str]:
        """
        Build a dictionary mapping plants to their types.

        Returns:
            Dict[str, str]: A dictionary mapping plants to their types.
        """
        plant_to_type = {}
        for key, value in self.type_to_plant.items():
            plant_to_type.update({plant: key for plant in value})
        return plant_to_type

    def clean(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the 'type' feature in the dataset.

        Args:
            dataset (pd.DataFrame): The plant dataset to be cleaned.

        Returns:
            pd.DataFrame: The cleaned dataset.
        """
        cleaned_dataset = dataset.copy()
        cleaned_dataset.loc[:, self.type_col] = cleaned_dataset[self.type_col].apply(
            lambda x: self.plant_to_type[x] if x in self.plant_to_type.keys() else x)

        cleaned_dataset = self.impute_with_file(
            cleaned_dataset, self.imputation_file, self.type_col)

        return cleaned_dataset
