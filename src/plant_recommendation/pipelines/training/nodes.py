import pandas as pd
import numpy as np

from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import RobustScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import make_column_transformer, ColumnTransformer
from typing import List, Tuple


def remove_poisonous_plants(dataset: pd.DataFrame, poisonous_col: List[str]) -> pd.DataFrame:
    """
    Remove plants poisonous for humans and/or pets from dataset.

    Args:
        dataset (pd.DataFrame): plant dataset.
        poisonous_col (List[str]): list of columns name 

    Returns:
        pd.DataFrame: dataset without toxic plants.
    """
    mask_safe = np.logical_and.reduce(
        [(dataset[feature] == False) for feature in poisonous_col])
    new_dataset = dataset.loc[mask_safe].copy()
    
    return new_dataset.drop(columns=poisonous_col)


def prepare_data(dataset: pd.DataFrame, col_to_drop: List[str], poisonous_col: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare the dataset by removing poisonous plants and dropping specified columns.

    Args:
        dataset (pd.DataFrame): The original plant dataset.
        col_to_drop (List[str]): List of column names to drop from the dataset.
        poisonous_col (List[str]): List of column names indicating poisonous plants.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: A tuple containing the feature matrix (X) and the filtered dataset.
    """
    filtered_dataset = remove_poisonous_plants(dataset, poisonous_col)
    X = filtered_dataset.drop(columns=col_to_drop)

    return X, filtered_dataset


def fit_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """
    Fit a preprocessor to the feature matrix.

    Args:
        X (pd.DataFrame): The feature matrix.

    Returns:
        ColumnTransformer: The fitted column transformer.
    """
    preprocessor = make_column_transformer((OneHotEncoder(), ['type']),
                                           (RobustScaler(), [
                                            'hardiness_max', 'hardiness_min']),
                                           (OrdinalEncoder(categories=[
                                            ['low', 'moderate', 'high']]), ['maintenance']),
                                           (OrdinalEncoder(categories=[
                                            ['full_shade', 'part_shade', 'full_sun']]), ['sunlight']),
                                           remainder="passthrough", force_int_remainder_cols=False)
    preprocessor.fit(X)

    return preprocessor


def fit_nn(X: pd.DataFrame, fitted_preprocessor: ColumnTransformer, n_neighbors: int) -> NearestNeighbors:
    """
    Fit a Nearest Neighbors model to the preprocessed feature matrix.

    Args:
        X (pd.DataFrame): The feature matrix.
        fitted_preprocessor (ColumnTransformer): The fitted column transformer.
        n_neighbors (int): The number of neighbors to use.

    Returns:
        NearestNeighbors: The fitted Nearest Neighbors model.
    """
    nn = NearestNeighbors(n_neighbors=n_neighbors)
    nn.fit(fitted_preprocessor.transform(X))

    return nn
