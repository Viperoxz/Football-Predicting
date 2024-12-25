# Football-predicting

## Data

The data directory is organized as follows:

- **raw/**: Contains raw data files.
- **preprocessed/**: Contains preprocessed data files.
- **transformed/**: Contains transformed data files.
- **team_map.json**: JSON file mapping team names.

## Models

The models directory contains the following:

- **GRU_Layer1**: Directory containing the GRU model for layer 1.
- **GRUconfig.py**: Configuration file for the GRU model.
- **inputs*.npy**: Input data files for different seasons.
- **outputs*.npy**: Output data files for different seasons.

## Notebooks

The notebooks directory contains Jupyter notebooks for various tasks:

- **preprocessing/**: Notebooks for data preprocessing.
- **crawl_data/**: Notebooks for crawling data from various sources.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Viperoxz/Football-Predicting.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Football-Predicting
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. Preprocess the data:
    ```sh
    jupyter notebook notebooks/preprocessing/prepare_layer1.ipynb
    ```
2. Train the model:
    ```sh
    jupyter notebook notebooks/train_model.ipynb
    ```
3. Evaluate the model:
    ```sh
    jupyter notebook notebooks/evaluate_model.ipynb
    ```
