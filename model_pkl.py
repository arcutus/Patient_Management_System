# -*- coding: utf-8 -*-
"""Train a simple housing-quality classifier from the California housing dataset.

This script is compatible with a regular Python environment and avoids Colab-only
features such as `display()` and `google.colab` imports.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.datasets import fetch_california_housing
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def house_value_label(median_house_value):
    if median_house_value < 100000:
        return "cheap"
    elif median_house_value < 200000:
        return "medium"
    return "expensive"


def house_condition(housing_median_age):
    if housing_median_age <= 15:
        return "good condition"
    elif housing_median_age <= 35:
        return "medium condition"
    return "bad condition"


def lifestyle(row):
    if row["population_per_household"] > row["rooms_per_household"]:
        return "low"
    return "high"


def load_data():
    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "sample_data" / "california_housing_train.csv"

    if csv_path.exists():
        return pd.read_csv(csv_path)

    try:
        data = fetch_california_housing(as_frame=True)
        df = data.frame.copy()
        df["median_house_value"] = data.target * 100000
        return df
    except Exception as exc:  # pragma: no cover - depends on environment/network access
        raise FileNotFoundError(
            "Dataset not found. Add a California housing CSV at sample_data/california_housing_train.csv "
            "or ensure scikit-learn can download the built-in dataset."
        ) from exc


def prepare_features(df):
    df = df.copy()

    if "housing_median_age" not in df.columns and "HouseAge" in df.columns:
        df["housing_median_age"] = df["HouseAge"]
    if "median_house_value" not in df.columns and "MedHouseVal" in df.columns:
        df["median_house_value"] = df["MedHouseVal"] * 100000

    if "total_rooms" in df.columns and "households" in df.columns:
        df["rooms_per_household"] = df["total_rooms"] / df["households"]
        df["population_per_household"] = df["population"] / df["households"]
        if "total_bedrooms" in df.columns:
            df["bedrooms_per_room"] = df["total_bedrooms"] / df["total_rooms"]
    else:
        df["rooms_per_household"] = df["AveRooms"] / df["AveOccup"]
        df["population_per_household"] = df["Population"] / df["AveOccup"]
        df["bedrooms_per_room"] = df["AveBedrms"] / df["AveRooms"]

    if "latitude" in df.columns and "longitude" in df.columns:
        sf_coord = (37.7749, -122.4194)
        la_coord = (34.0522, -118.2437)
        df["distance_to_sf"] = np.sqrt((df["latitude"] - sf_coord[0]) ** 2 + (df["longitude"] - sf_coord[1]) ** 2)
        df["distance_to_la"] = np.sqrt((df["latitude"] - la_coord[0]) ** 2 + (df["longitude"] - la_coord[1]) ** 2)
    else:
        df["distance_to_sf"] = np.sqrt((df["Latitude"] - 37.7749) ** 2 + (df["Longitude"] + 122.4194) ** 2)
        df["distance_to_la"] = np.sqrt((df["Latitude"] - 34.0522) ** 2 + (df["Longitude"] + 118.2437) ** 2)

    df["house_value"] = df["median_house_value"].apply(house_value_label)
    df["house_condition"] = df["housing_median_age"].apply(house_condition)
    df["lifestyle"] = df.apply(lifestyle, axis=1)

    return df


def main():
    df = prepare_features(load_data())

    feature_columns = [
        "housing_median_age",
        "rooms_per_household",
        "bedrooms_per_room",
        "population_per_household",
        "distance_to_sf",
        "distance_to_la",
    ]
    categorical_features = ["house_condition", "lifestyle"]
    target = "house_value"

    X = df[feature_columns + categorical_features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, feature_columns),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, multi_class="auto")),
        ]
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print(classification_report(y_test, predictions))


if __name__ == "__main__":
    main()