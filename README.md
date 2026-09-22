# Car Price Category ML Pipeline with Airflow

An automated machine learning pipeline that classifies used cars into price
categories. Apache Airflow orchestrates model training and batch prediction.

## Workflow

```text
Training data
    -> preprocessing and feature engineering
    -> cross-validation of three classifiers
    -> best model selection and serialization
    -> batch prediction for JSON records
    -> CSV predictions
```

The Airflow DAG runs the following tasks sequentially:

```text
pipeline -> predict
```

The DAG is scheduled for Fridays at 21:00 and has catchup disabled.

## Modeling

The training pipeline:

- removes identifiers, URLs, free text, coordinates and other unused columns;
- caps outliers in the vehicle year using the IQR rule;
- creates `short_model` and `age_category` features;
- imputes missing numerical and categorical values;
- standardizes numerical features;
- one-hot encodes categorical features;
- compares Logistic Regression, Random Forest and SVC;
- selects the model with the highest mean accuracy from 4-fold cross-validation.

The target is `price_category`, so this project solves a classification problem
rather than predicting an exact monetary price.

## Project Structure

```text
car-price-airflow-ml/
|-- dags/
|   `-- hw_dag.py
|-- modules/
|   |-- pipeline.py
|   `-- predict.py
|-- data/
|   |-- train/
|   |   `-- homework.csv
|   |-- test/
|   |   `-- *.json
|   |-- models/          # generated locally
|   `-- predictions/     # generated locally
`-- .gitignore
```

## Local Run

Create and activate a virtual environment, then install the required Python
packages:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install pandas scikit-learn dill
```

Create output directories if they do not exist:

```bash
mkdir -p data/models data/predictions
```

Train and select the best model:

```bash
python modules/pipeline.py
```

Generate predictions from JSON files in `data/test/`:

```bash
python modules/predict.py
```

The trained pipeline is written to `data/models/`. Predictions are written to
`data/predictions/` as a CSV file with `car_id` and `pred` columns.

## Airflow Run

1. Install and configure Apache Airflow for your environment.
2. Set `PROJECT_PATH` in `dags/hw_dag.py` to the absolute project directory.
3. Make `hw_dag.py` available in the Airflow DAGs directory.
4. Enable the `car_price_prediction` DAG in the Airflow UI.

## Technology Stack

- Python
- pandas
- scikit-learn
- Apache Airflow
- dill

