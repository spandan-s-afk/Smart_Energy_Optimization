# Smart Energy Consumption Prediction and Optimization

A Python project for household electricity-consumption analysis, machine-learning evaluation, peak-load analysis, and appliance scheduling with SciPy's mixed-integer linear optimization solver (MILP), presented through a Streamlit dashboard.

## Overview

The project provides an interactive dashboard for exploring energy data, viewing prediction metrics, inspecting hourly demand, and comparing baseline and optimized load profiles.

## Features

- Streamlit dashboard with dataset, prediction, peak-load, and optimization views
- Random Forest model training and evaluation
- Hourly energy-consumption analysis
- Mixed-integer optimization for appliance scheduling
- CSV results and graph visualizations

## Technologies

- Python 3
- Streamlit
- Pandas and NumPy
- scikit-learn
- SciPy
- Matplotlib
- Joblib

## Reported Project Results

These values are displayed by the current application/project outputs. The exact dataset and model run that produced each metric have not yet been traced and reproduced, so treat them as reported results rather than independently verified benchmarks.

| Metric | Reported value |
|---|---:|
| Peak monitored load before optimization | 5.4532 kW |
| Peak monitored load after optimization | 4.6354 kW |
| Peak-load reduction | 15.00% |
| Daily energy consumption | 68.8273 kWh before and after |
| Mean Absolute Error (MAE) | 0.302053 kW |
| Root Mean Squared Error (RMSE) | 0.425657 kW |
| R² score | 0.610869 |

The optimization implementation in `src/optimization.py` uses `scipy.optimize.milp` to select appliance start times while minimizing the maximum hourly load subject to appliance scheduling constraints. The optimization assumptions and reported results do not guarantee real-world household energy savings.

## Repository Structure

```text
Smart_Energy_Optimization/
├── app.py
├── src/
│   ├── train_model.py
│   └── optimization.py
├── data/                 # Required data files; not included in GitHub
├── models/               # Trained models; large model stored externally
├── graphs/               # Visualization outputs
├── results/              # CSV outputs
├── requirements.txt
└── README.md
```

## Dataset and Model Files

The Streamlit dashboard expects the processed dataset at:

```text
data/homec_processed.csv
```

The training script `src/train_model.py` separately expects:

```text
data/processed_energy_data.csv
```

The large trained model is expected at:

```text
models/random_forest_energy_model.pkl
```

These files are excluded from the GitHub repository because of their size. **The original dataset source and public download location have not yet been verified for this repository.** Do not assume that a similarly named public dataset is the exact source. Before running the project, obtain the correct files from the project owner and ensure you have permission to use them.

- Dataset download: **to be added after source verification**
- Large model download: **to be added after external upload**

The smaller model `models/homec_random_forest_model.pkl` and the graph/result files may be present in the repository.

## Screenshots and Results

The following figures are committed to the repository and provide a preview without requiring the dataset or trained model to run the dashboard.

### Predicted vs. Actual Power

![Predicted vs. actual power](graphs/predicted_vs_actual.png)

### Hourly Peak Load

![Hourly peak load](graphs/hourly_peak_load_homec.png)

### Before and After Optimization

![Before and after optimization](graphs/before_after_comparison.png)

## Installation

1. Install Python 3 and Git.
2. Clone the repository:

   ```bash
   git clone https://github.com/spandan-s-afk/Smart_Energy_Optimization.git
   cd Smart_Energy_Optimization
   ```

3. (Recommended) Create and activate a virtual environment on Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Obtain the required dataset file and place it at `data/homec_processed.csv`. If you intend to run the training script, also provide `data/processed_energy_data.csv`.

## Run the Dashboard

From the repository root, run:

```powershell
streamlit run app.py
```

Streamlit will display a local URL, usually `http://localhost:8501`, to open in your browser.

## Train the Model (Optional)

After placing the expected training dataset at `data/processed_energy_data.csv`, run:

```bash
python src/train_model.py
```

This script writes `models/random_forest_energy_model.pkl`. Training may require substantial memory and processing time depending on dataset size.

## Limitations

- Required datasets and the large trained model are not bundled with the repository.
- The original dataset source and preprocessing provenance still need confirmation.
- Prediction metrics depend on the data, feature engineering, and evaluation methodology.
- Optimization results depend on the model's assumptions and scheduling constraints.

## Author

Spandan

## Disclaimer

This project is intended for academic and educational purposes. Confirm the data license and model provenance before redistribution.
