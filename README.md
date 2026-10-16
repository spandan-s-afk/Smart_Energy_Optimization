# Smart Energy Consumption Prediction and Optimization

A Data Science project that explores household electricity consumption forecasting and peak-load optimization using Python, machine learning, and numerical optimization.

## Overview

This project analyzes electricity consumption patterns, evaluates predicted power usage, and explores how flexible appliance loads can be scheduled to reduce peak monitored demand while maintaining daily energy requirements.

## Objectives

- Analyze historical electricity consumption.
- Predict power usage using machine learning.
- Identify peak-demand periods.
- Explore appliance scheduling through numerical optimization.
- Compare energy profiles before and after optimization.

## Technologies Used

- Python
- Pandas
- NumPy
- scikit-learn
- SciPy
- Matplotlib

## Project Results

Reported results from the project evaluation:

| Metric | Result |
|---|---:|
| Peak monitored load before optimization | 5.4532 kW |
| Peak monitored load after optimization | 4.6354 kW |
| Peak-load reduction | 15.00% |
| Daily energy consumption | 68.8273 kWh before and after |
| Mean Absolute Error (MAE) | 0.302053 kW |
| Root Mean Squared Error (RMSE) | 0.425657 kW |
| R² score | 0.610869 |

These figures represent project evaluation results and do not establish real-world household energy savings. The optimization assumes that 30% of flexible load can be shifted, subject to the project's scheduling constraints.

## Project Structure

```text
.
├── app.py
├── src/
├── results/
├── graphs/
└── README.md
```

The exact structure may vary depending on the files included in the repository.

## Dataset

The application expects a processed dataset at:

`data/homec_processed.csv`

The dataset source, access instructions, and any applicable usage restrictions should be documented here before running the project.

## How to Run

1. Install Python 3 and Git.
2. Clone this repository.
3. Install the dependencies listed in `requirements.txt`, if provided.
4. Obtain the required dataset and place it at `data/homec_processed.csv`.
5. Run the application:

```bash
python app.py
```

Additional setup steps may be required depending on the application's dependencies.

## Limitations

- Model performance depends on the dataset and evaluation methodology.
- Optimization results depend on the assumed flexible-load proportion and scheduling constraints.
- Evaluation results should not be interpreted as guaranteed real-world savings.

## Author

Spandan

## Disclaimer

This project is intended for academic and educational purposes.
