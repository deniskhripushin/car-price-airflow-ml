import glob
import logging
import os
from datetime import datetime

import dill
import pandas as pd

path = os.environ.get("PROJECT_PATH", ".")


def _latest_model_path(models_dir: str) -> str:
    candidates = sorted(glob.glob(os.path.join(models_dir, "*.pkl")))
    if not candidates:
        raise FileNotFoundError(f"No .pkl models found in: {models_dir}")
    return candidates[-1]


def _load_test_data(test_dir: str) -> pd.DataFrame:
    json_files = sorted(glob.glob(os.path.join(test_dir, "*.json")))
    if not json_files:
        raise FileNotFoundError(f"No .json files found in: {test_dir}")

    rows = []
    for fp in json_files:
        try:
            obj = pd.read_json(fp, typ="series")
            row = obj.to_dict()
            rows.append(row)
        except ValueError:
            df_one = pd.read_json(fp)
            if isinstance(df_one, pd.DataFrame) and len(df_one) == 1:
                rows.append(df_one.iloc[0].to_dict())
            else:
                rows.extend(df_one.to_dict(orient="records"))

    df = pd.DataFrame(rows)
    if df.empty:
        raise ValueError("Test dataframe is empty after loading JSON files.")
    return df


def predict() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    models_dir = os.path.join(path, "data", "models")
    test_dir = os.path.join(path, "data", "test")
    preds_dir = os.path.join(path, "data", "predictions")
    os.makedirs(preds_dir, exist_ok=True)

    model_path = _latest_model_path(models_dir)
    logging.info(f"Using model: {model_path}")

    with open(model_path, "rb") as f:
        model = dill.load(f)

    df_test = _load_test_data(test_dir)
    if "id" not in df_test.columns:
        raise KeyError('Column "id" not found in test data. Cannot create car_id.')
    car_ids = df_test["id"].astype(str)

    preds = model.predict(df_test)

    out = pd.DataFrame({"car_id": car_ids, "pred": preds})

    out_file = os.path.join(preds_dir, f"preds_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    out.to_csv(out_file, index=False, encoding="utf-8")
    logging.info(f"Predictions saved to: {out_file}")


if __name__ == "__main__":
    predict()
