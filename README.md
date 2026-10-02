# Southeastern Australia biodiversity classification

An annotated notebook for predicting species occurrence from TerraClimate raster data sampled at locations in southeastern Australia. The workflow compares Random Forest, LightGBM, XGBoost, and a soft-voting ensemble, then produces a competition-style CSV submission.

> **Project identity:** The supplied notebook and data files concern biodiversity classification. The accompanying request referred to a clinical reasoning challenge, but no clinical dataset or clinical model appears in this project. This README describes the notebook that was supplied.

## Contents

- [`biodiversity.ipynb`](biodiversity.ipynb): data validation, raster sampling, feature aggregation, model evaluation, optional feature selection and tuning, final fitting, and submission export.
- `README.md`: setup and reproducibility guidance.

The original notes proposed LSTM, TSViT, SITSMamba, and derived drought indices. These methods are not implemented here; the notebook focuses on the non-neural models supported by its existing data pipeline. It does **not** claim verified leaderboard performance.

## Data

Provide the competition dataset yourself in a single directory containing:

```text
Training_Data.csv
Test.csv
terraclimate_20171101.tif
...
terraclimate_20191101.tif
```

The notebook expects **25 consecutive monthly GeoTIFFs** from November 2017 through November 2019. Each must have 14 bands in this order: `aet`, `def`, `pdsi`, `pet`, `pr`, `ro`, `soil`, `srad`, `swe`, `tmmn`, `tmmx`, `vap`, `vpd`, `vs`. Confirm that order against the dataset you download.

Both CSVs need `Latitude` and `Longitude` columns with WGS84 decimal-degree coordinates. `Training_Data.csv` additionally needs a binary `Occurrence Status` column containing both 0 and 1. The test CSV's other columns are preserved in the submission, except an existing `Target` column, which is replaced.

Dataset files are not included in this repository. Follow the dataset provider's access and usage terms.

## Setup

Use Python 3.10 or later. Install the notebook's dependencies in your own environment:

```bash
python -m pip install jupyter numpy pandas matplotlib rasterio scikit-learn lightgbm xgboost joblib
```

Set paths if you are not using the notebook's Kaggle defaults:

```bash
export BIODIVERSITY_DATA_DIR="/path/to/dataset"
export BIODIVERSITY_OUTPUT_DIR="/path/to/output"
jupyter notebook biodiversity.ipynb
```

On Kaggle, update `BIODIVERSITY_DATA_DIR` if the mounted dataset path differs from the default in the notebook. No credentials or API tokens are required.

## Run the notebook

1. Confirm the data files and band order, then run cells from top to bottom.
2. Raster samples are cached as `temporal_train.npy` and `temporal_test.npy` in the output directory. The default `REBUILD_FEATURES = True` rebuilds them. If you turn it off, rebuild whenever CSV row order, rasters, or extraction logic changes.
3. Review the stratified holdout comparison using F1, recall, ROC AUC, and confusion matrices. Optional cross-validation, feature selection, and parameter searches are disabled by default.
4. Set `SELECTED_MODEL` to `random_forest`, `lightgbm`, `xgboost`, or `ensemble`. The notebook refits that model on all labeled data, writes `<model>_pipeline.joblib`, and creates `submission_<model>.csv` in the output directory.
5. Check the column names and label encoding against the competition's submission template before uploading a submission.

Missing raster values are imputed within each model pipeline. The random split is useful for a baseline, but geographically nearby or repeated sites can make its metrics optimistic; use a spatial or site-level split when the dataset supports it.

## Reproducibility status

The refactored notebook's code was syntax-checked and its missing-value aggregation was checked with a small synthetic example. End-to-end execution, training metrics, and submission acceptance were **not verified** because the competition dataset and all modeling dependencies were unavailable in the editing environment. Previously displayed exploratory scores are historical notes, not results reproduced by the revised workflow.
