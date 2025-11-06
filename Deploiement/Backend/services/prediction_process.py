import pandas as pd
import joblib
import numpy as np

def predict_process(data: dict):
    """
    Perform a stacked ensemble prediction based on input data.

    Args:
        data (dict): Input data from API (single observation).

    Returns:
        dict: Dictionary with predicted credit risk category and probability score.
    """

    # Convert incoming dictionary to a single-row DataFrame
    df_input = pd.DataFrame([data])

    # Load base models and meta-model
    model_lgbm = joblib.load("assets/model_lgbm.pickle")
    model_xgb = joblib.load("assets/model_xgb.pickle", mmap_mode='r')

    model_rdf = joblib.load("assets/model_rdf.pickle")
    meta_model = joblib.load("assets/meta_model.pickle")

    # Base model predictions (probabilities)
    pred_xgb = model_xgb.predict_proba(df_input)[:, 1]
    pred_lgbm = model_lgbm.predict_proba(df_input)[:, 1]
    pred_rdf = model_rdf.predict_proba(df_input)[:, 1]

    # Create meta-features for stacking
    x_meta = pd.DataFrame({
        "pred_xgb": pred_xgb,
        "pred_lgbm": pred_lgbm,
        "pred_rdf": pred_rdf
    })

    # Meta-model prediction
    predict_proba = meta_model.predict_proba(x_meta)[:, 1][0]  # single probability
    predict_val = meta_model.predict(x_meta)[0]  # 0 or 1

    # Convert numeric prediction into text label
    # Adjust labels depending on your business rules
    label_map = {
        0: "Repay",    # Good credit — likely to repay
        1: "Default"    # Bad credit — likely to default
    }
    predicted_label = label_map.get(int(predict_val), "Unknown")

    # Return readable output
    return {
        "credit_status": predicted_label,
        "probability": round(float(predict_proba), 4)
    }
