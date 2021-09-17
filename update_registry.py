import os
import yaml
import pytest
import pandas as pd

from methods_io import read_project_cards
from methods_add_cards import add_cards_to_registry

CARD_DIR = os.path.join(".", "projects")
REGISTRY_FILE = "registry.csv"
CONFIG_FILE = "registry_config.yml"


def update_registry(
    config_file: str = CONFIG_FILE,
    input_reg_file: str = REGISTRY_FILE,
    output_reg_file: str = REGISTRY_FILE,
    card_dir: str = CARD_DIR,
    write_card_updates: bool = True,
):

    input_reg_df = pd.read_csv(input_reg_file)
    with open(config_file, "r") as file:
        config_dict = yaml.safe_load(file)

    card_file_list = read_project_cards(card_dir)
    df = add_cards_to_registry(
        card_file_list, input_reg_df, config_dict, write_card_updates
    )
    df.to_csv(output_reg_file, index=False)


if __name__ == "__main__":
    update_registry()
