# Football Prediction Project

This project aims to predict the outcome of English Premier League football matches using machine learning techniques. It involves data crawling, preprocessing, feature engineering, model training, and evaluation.
## Members
- [Vũ Châu Minh Trí](https://github.com/vcmt794)
- [Trương Tiến Đạt](https://github.com/tiendat25052004)
- [Tống Trọng Tâm](https://github.com/monster1909)
- [Phạm Văn Hoàng Nam](https://github.com/Viperoxz)
## Project Structure

The project is organized into the following directories:

-   **`notebooks/`**: Contains Jupyter notebooks for various tasks.
    -   **`preprocessing/`**: Notebooks for data cleaning, transformation, and feature engineering.
    -   **`eda/`**: Notebooks for exploratory data analysis and visualization.
    -   **`crawl_data/`**: Notebooks for web scraping data from different sources.
-   **`data/`**: Stores all data files.
    -   **`raw/`**: Contains the original, unprocessed data.
        -   **`fbdata/`**: Raw match data from fbref.
        -   **`worldfb/`**: Raw data from worldfootball.net.
        -   **`fbref/`**: Raw data from fbref.
        -   **`fantasy/`**: Raw data from the Fantasy Premier League API.
        -   **`sofifa/`**: Raw data from sofifa.com.
    -   **`preprocessed/`**: Contains data after preprocessing steps.
        -   **`layer1/`**: Preprocessed data for the first layer of the model.
        -   **`layer2/`**: Preprocessed data for the second layer of the model.
        -   **`info/`**: Additional information about matches and players.
        -   `note.txt`: Notes about the preprocessed data.
    -   **`transformed/`**: Contains data after transformations.
    -   **`team_map.json`**: JSON file mapping team names to numerical IDs.
-   **`models/`**: Contains notebooks and files related to model training and evaluation.
    -   **`Layer_1/`**: Files for the first layer of the model.
        -   **`Data/`**: Input and output data for the first layer.
        -   **`Model/`**: Trained models for the first layer.
    -   **`Layer_2/`**: Files for the second layer of the model.
        -   **`Data/`**: Input and output data for the second layer.
        -   **`Model/`**: Trained models for the second layer.
    -   **`Both/`**: Files for the combined model.
        -   **`Data/`**: Input and output data for the combined model.
        -   **`Model/`**: Trained models for the combined model.
    -   `prepare_data_for_tf.ipynb`: Notebook for preparing data for TensorFlow models.
    -   `try_both_layer.ipynb`: Notebook for trying both layers of the model.
    -   `try_layer2_H_NH.ipynb`: Notebook for trying the second layer with H/NH classification.
    -   `try_layer1_H_NH.ipynb`: Notebook for trying the first layer with H/NH classification.
    -   `try_layer1.ipynb`: Notebook for trying the first layer of the model.
    -   `try_layer2.ipynb`: Notebook for trying the second layer of the model.
-   **`src/`**: Contains Python source code.
    -   **`data/`**: Python scripts for data crawling and handling.
        -   `fbref.py`: Script for crawling data from fbref.com.
    -   **`features/`**: Python scripts for feature engineering.
        -   `elo.py`: Script for calculating ELO ratings.

## Data

The `data` directory is organized to separate raw, preprocessed, and transformed data.

-   **`raw/`**: Contains the original data files, as downloaded from various sources.
-   **`preprocessed/`**: Contains data that has been cleaned and prepared for model training.
    -   `layer1/` contains match statistics data.
    -   `layer2/` contains player statistics data.
    -   `info/` contains information about matches and players.
-   **`transformed/`**: Contains data that has been further processed for visualization or specific model inputs.
-   **`team_map.json`**: A JSON file that maps team names to numerical IDs, used for model input.

## Models

The `models` directory contains the following:

-   **`Layer_1/`**: Contains data and trained models for the first layer of the prediction model.
-   **`Layer_2/`**: Contains data and trained models for the second layer of the prediction model.
-   **`Both/`**: Contains data and trained models for the combined model.
-   Jupyter notebooks for model training, testing, and evaluation.
-   Pickled (`.pkl`) files containing trained models (SVM, XGBoost, RandomForest).
-   Numpy (`.npy`) files containing input and output data for the models.

The models are trained to predict match outcomes using two approaches:
    -   **H_D_A**: Predicts Home win, Draw, or Away win.
    -   **H_NH**: Predicts Home win or Not Home win.

## Notebooks

The `notebooks` directory contains Jupyter notebooks for various tasks:

-   **`preprocessing/`**: Notebooks for data preprocessing, feature engineering, and data integration.
-   **`crawl_data/`**: Notebooks for crawling data from various sources like fbref, sofifa, worldfootball.net, and Fantasy Premier League.
-   **`eda/`**: Notebooks for exploratory data analysis and visualization of the data.

## Getting Started

### Prerequisites

-   Python 3.x
-   Required Python packages (listed in `requirements.txt`)
-   Web browser (for data crawling)

### Installation

1.  Clone the repository:

    ```sh
    git clone https://github.com/Viperoxz/Football-Predicting.git
    ```
2.  Navigate to the project directory:

    ```sh
    cd Football-Predicting
    ```
3.  Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

### Usage

1.  **Data Crawling**:
    -   Run the notebooks in the `notebooks/crawl_data/` directory to gather data from various sources.
    -   For example:
        ```sh
        jupyter notebook notebooks/crawl_data/fbref.ipynb
        ```
2.  **Data Preprocessing**:
    -   Execute the notebooks in the `notebooks/preprocessing/` directory to clean, transform, and prepare the data.
    -   For example:
        ```sh
        jupyter notebook notebooks/preprocessing/prepare_layer1.ipynb
        ```
3.  **Model Training**:
    -   Use the notebooks in the `models/` directory to train and evaluate the models.
    -   For example:
        ```sh
        jupyter notebook models/try_layer1_H_NH.ipynb
        ```
4.  **Exploratory Data Analysis**:
    -   Explore the data using notebooks in the `notebooks/eda/` directory.
    -   For example:
        ```sh
        jupyter notebook notebooks/eda/explore_data.ipynb
        ```

## Key Files and Scripts

-   **`src/data/fbref.py`**: This script is used to crawl match data from fbref.com. It extracts various statistics for each match, including shooting, goalkeeping, passing, defensive actions, and possession data.
-   **`src/features/elo.py`**: This script contains the logic for calculating ELO ratings for teams based on match results.

## Data Description

### `data/preprocessed/layer1/matches_stats_data.csv`

This file contains match statistics data, scaled between 0 and 1, and includes the following features:

-   `hometeam`, `awayteam`, `date`, `season`, `round`: Match identifiers.
-   `gf`, `ga`: Goals for and against (not scaled, used for ELO calculation).
-   `h_form_gf`, `h_form_ga`, `a_form_gf`, `a_form_ga`: Form of goals for and against for home and away teams.
-   `h_form_xg`, `h_form_xga`, `a_form_xg`, `a_form_xga`: Form of expected goals for and against.
-   `h_form_standard sot`, `a_form_standard sot`: Form of shots on target.
-   `h_form_kp`, `a_form_kp`: Form of key passes.
-   `h_form_xa`, `a_form_xa`: Form of expected assists.
-   `h_form_poss_x`, `a_form_poss_x`: Form of possession percentage.
-   `h_form_touches att pen`, `a_form_touches att pen`: Form of touches in the attacking penalty area.
-   `h_form_carries prgdist`, `a_form_carries prgdist`: Form of progressive carrying distance.
-   `h_form_progressive passing dist`, `a_form_progressive passing dist`: Form of progressive passing distance.
-   `h_form_tackles tklw`, `a_form_tackles tklw`: Form of successful tackles.
-   `h_form_challenges tkl%`, `a_form_challenges tkl%`: Form of tackle success rate.
-   `h_form_saves`, `a_form_saves`: Form of saves by the goalkeeper.
-   `b365h`, `b365d`, `b365a`: Betting odds for home win, draw, and away win.
-   `result_A`, `result_D`, `result_H`: Target variables for prediction (Away win, Draw, Home win).
-   `soh`, `soa`: ELO ratings for home and away teams.

### `data/preprocessed/layer2/`

This directory contains player statistics data extracted from the Fantasy Premier League API.

## Contributing

Contributions to this project are welcome. Please feel free to submit pull requests or open issues for any bugs or feature requests.

## License

This project is licensed under the [MIT License](LICENSE).
