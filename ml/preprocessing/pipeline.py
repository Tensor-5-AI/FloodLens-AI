"""
Leakage-safe Preprocessing Pipeline.
Ensures that all scalers, median imputers, and normalization parameters
are fitted STRICTLY on the training partition and then applied to test or inference samples.
Prevents data leakage as mandated in project guidelines.
"""

from typing import Dict, Any, Optional, Tuple, List
import joblib
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from ml.features.builder import FeatureBuilder, NUMERIC_FEATURE_NAMES


class LeakageSafePreprocessor:
    """
    Stateful preprocessor for tabular flood features.
    Guarantees zero leakage between train and test splits.
    """

    def __init__(self, feature_names: List[str] = NUMERIC_FEATURE_NAMES) -> None:
        self.feature_names = feature_names
        self.builder = FeatureBuilder(feature_names=self.feature_names)
        self.imputer: Optional[SimpleImputer] = None
        self.scaler: Optional[StandardScaler] = None
        self.fitted_feature_names: List[str] = []
        self.is_fitted: bool = False

    def fit(self, df_train: pd.DataFrame) -> "LeakageSafePreprocessor":
        """
        Fit imputer and scaler using training split ONLY.
        """
        X_train_raw = self.builder.extract_feature_matrix(df_train)
        self.fitted_feature_names = list(X_train_raw.columns)

        # Median imputation for numerical features
        self.imputer = SimpleImputer(strategy="median")
        X_imputed = self.imputer.fit_transform(X_train_raw)

        # Standard normalization
        self.scaler = StandardScaler()
        self.scaler.fit(X_imputed)

        self.is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """
        Transform features using previously fitted statistics.
        """
        if not self.is_fitted or self.imputer is None or self.scaler is None:
            raise RuntimeError("Preprocessor must be fitted on training data before calling transform().")

        X_raw = self.builder.extract_feature_matrix(df)

        # Align columns to match training set
        for col in self.fitted_feature_names:
            if col not in X_raw.columns:
                X_raw[col] = 0.0
        X_raw = X_raw[self.fitted_feature_names]

        X_imputed = self.imputer.transform(X_raw)
        X_scaled = self.scaler.transform(X_imputed)
        return X_scaled

    def fit_transform(self, df_train: pd.DataFrame) -> np.ndarray:
        """
        Fit on training dataframe and return transformed array.
        """
        return self.fit(df_train).transform(df_train)

    def save(self, filepath: str) -> None:
        """
        Persist fitted preprocessor state to disk.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(
            {
                "imputer": self.imputer,
                "scaler": self.scaler,
                "fitted_feature_names": self.fitted_feature_names,
                "is_fitted": self.is_fitted,
            },
            filepath,
        )

    @classmethod
    def load(cls, filepath: str) -> "LeakageSafePreprocessor":
        """
        Load persisted preprocessor state.
        """
        state = joblib.load(filepath)
        instance = cls(feature_names=state["fitted_feature_names"])
        instance.imputer = state["imputer"]
        instance.scaler = state["scaler"]
        instance.fitted_feature_names = state["fitted_feature_names"]
        instance.is_fitted = state["is_fitted"]
        return instance
