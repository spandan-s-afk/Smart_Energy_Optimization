# Smart Energy Consumption Prediction and Optimization

A Python project for household electricity-consumption analysis, Random Forest prediction, peak-load analysis, and appliance scheduling with SciPy's mixed-integer linear optimization solver (MILP), presented through a Streamlit dashboard.

## Overview

This project provides an interactive dashboard for exploring energy data, viewing prediction metrics, inspecting hourly demand, and comparing baseline and optimized load profiles.

The project contains two related components:

- **Prediction:** A Random Forest model estimates future appliance power using historical consumption and time-based features.
- **Optimization:** A mixed-integer optimization routine selects appliance start times to reduce peak hourly load while respecting scheduling constraints.

The available evaluation scripts assess these components separately. The current results do not establish that the optimizer directly uses the Random Forest model's predictions.

## Features

- Streamlit dashboard with dataset, prediction, peak-load, and optimization views
- Random Forest model training and evaluation
- Hourly energy-consumption analysis
- Mixed-integer optimization for appliance scheduling
- CSV evaluation outputs and graph visualizations

## Technologies

- Python 3
- Streamlit
- Pandas and NumPy
- scikit-learn
- SciPy
- Matplotlib
- Joblib and Python pickle

## Evaluated Project Results

The following results were reproduced using the project's existing evaluation scripts and saved Random Forest model.

| Metric | Evaluated result |
|---|---:|
| Peak monitored load before optimization | 5.453183 kW |
| Peak monitored load after optimization | 4.635425 kW |
| Peak-load reduction | 15.00% |
| Daily energy consumption before optimization | 68.827259 kWh |
| Daily energy consumption after optimization | 68.827259 kWh |
| Mean Absolute Error (MAE) | 0.302053 kW |
| Root Mean Squared Error (RMSE) | 0.425657 kW |
| R² score | 0.610869 |

### Evaluation Methodology

- **Prediction evaluation:** The existing saved Random Forest model was evaluated on a reconstructed chronological test set containing 6,700 samples. The resulting MAE, RMSE, and R² matched the values displayed in the dashboard.
- **Optimization evaluation:** The evaluation script compared baseline and optimized monitored-load profiles, reporting a 15.00% reduction in peak load while maintaining the same daily energy consumption.
- **Optimization assumptions:** The project assumes that 30% of flexible load can be shifted, subject to the appliance scheduling constraints.

The optimization implementation in `src/optimization.py` uses `scipy.optimize.milp` to select appliance start times while minimizing maximum hourly load subject to scheduling constraints.

These results describe the project's evaluation and modeled optimization scenario; they do not establish real-world household energy savings. The prediction metrics were reproduced using a reconstructed test set. The original dataset provenance and complete evaluation workflow still require documentation.

## Repository Structure

```text
Smart_Energy_Optimization/
├── app.py
├── src/
│   ├── data_preprocessing.py
│   ├── evaluation.py
│   ├── optimization.py
│   ├── optimization_homec.py
│   ├── peak_load_analysis.py
│   ├── peak_load_homec.py
│   ├── preprocess_homec.py
│   ├── train_homec_model.py
│   └── train_model.py
├── data/                 # Required data files; not all are distributed
├── models/               # Saved trained models; some files are large
├── graphs/               # Visualization outputs
├── results/              # Evaluation CSV outputs
├── requirements.txt
└── README.md
```

This is a representative structure; the files available in a particular checkout may differ.

## Dataset and Model Files

The dashboard and scripts use different input files. Obtain the correct files before running them.

The dashboard and HomeC evaluation workflow expect the processed dataset at:

```text
data/homec_processed.csv
```

The separate training script `src/train_model.py` expects:

```text
data/processed_energy_data.csv
```

The HomeC training script `src/train_homec_model.py` saves its model to:

```text
models/homec_random_forest_model.pkl
```

The separate training script `src/train_model.py` saves its model to:

```text
models/random_forest_energy_model.pkl
```

The original dataset source and public download location have not yet been verified for this repository. Do not assume a similarly named public dataset is the exact source. Before running the project, obtain the correct files from the project owner and ensure you have permission to use them.

- Dataset download: to be added after source verification
- Large model download: to be added if an external upload is provided

Some datasets and trained model files may be excluded from GitHub because of their size. Check the repository's actual file list before assuming a particular file is available.

## Screenshots and Results

The following figures are expected to be available in the `graphs/` directory. If a linked image does not render on GitHub, check that the file is committed at the stated path.

### Predicted vs. Actual Power

![Predicted vs. actual power](graphs/predicted_vs_actual.png)

### Hourly Peak Load

![Hourly peak load](graphs/hourly_peak_load_homec.png)

### Before and After Optimization

![Before and after optimization](graphs/before_after_comparison.png)

## Installation

1. Install Python 3 and Git.
2. Clone the repository and enter the project directory:

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
   python -m pip install -r requirements.txt
   ```

5. Obtain the required dataset file and place it at `data/homec_processed.csv`. If you intend to run `src/train_model.py`, also provide `data/processed_energy_data.csv`.

The project may require additional setup depending on which dashboard pages and scripts you use.

## Run the Dashboard

From the repository root, run:

```bash
streamlit run app.py
```

Streamlit will display a local URL, usually `http://localhost:8501`, to open in your browser.

## Train the Models (Optional)

### HomeC Random Forest Model

After placing the required processed dataset at `data/homec_processed.csv`, run:

```bash
python src/train_homec_model.py
```

This script trains a Random Forest model, reports MAE, RMSE, and R² on its chronological test split, saves `models/homec_random_forest_model.pkl`, and generates a prediction graph. Running it retrains the model and overwrites the saved HomeC model.

### Separate Energy Model

After placing the expected dataset at `data/processed_energy_data.csv`, run:

```bash
python src/train_model.py
```

This script writes `models/random_forest_energy_model.pkl`. Training may require substantial memory and processing time depending on dataset size.

## Limitations

- Required datasets and some trained model files may not be bundled with the repository.
- The original dataset source and preprocessing provenance still need confirmation.
- Prediction metrics depend on the data, feature engineering, and evaluation methodology.
- The reported prediction metrics were reproduced using a reconstructed chronological test set; this is not the same as confirming the original historical evaluation run.
- Optimization results depend on the flexible-load assumption and scheduling constraints.
- Results from the modeled scenario should not be interpreted as guaranteed real-world savings.
- The relationship between the prediction output and the optimization inputs should not be assumed unless confirmed by the implementation.

## Author

Spandan

## Disclaimer

This project is intended for academic and educational purposes. Confirm the data license and model provenance before redistribution.
