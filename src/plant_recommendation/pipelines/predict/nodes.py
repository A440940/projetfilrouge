import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.compose import ColumnTransformer


def recommand_plant(user_data: pd.DataFrame, nn: NearestNeighbors, preprocessor: ColumnTransformer, plants_dataset: pd.DataFrame):
    """
    Recommend plants based on user data using a Nearest Neighbors model.

    Args:
        user_data (pd.DataFrame): The user data for which to recommend plants.
        nn (NearestNeighbors): The fitted Nearest Neighbors model.
        preprocessor (ColumnTransformer): The fitted preprocessor for transforming the user data.
        plants_dataset (pd.DataFrame): The dataset containing plant information.

    Returns:
        pd.DataFrame: The recommended plants sorted by distance.
    """
    distances, indices = nn.kneighbors(preprocessor.transform(user_data))
    recommanded_plants = plants_dataset.iloc[indices[0]].copy()
    recommanded_plants['_distance'] = distances[0]

    return recommanded_plants.sort_values(by='_distance')
