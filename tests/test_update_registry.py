import os
import sys
import inspect
import pytest
import pandas as pd

c_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
p_dir = os.path.dirname(c_dir)
sys.path.insert(0, p_dir)

from update_registry import update_registry

"""
Run tests from bash/shell
Run just the tests labeled project using `pytest -m update_registry`
To run with print statments, use `pytest -s -m update_registry`
"""


@pytest.mark.ci
@pytest.mark.update_registry
def test_update_registry(request):

    input_file = "test_input_registry.csv"
    output_file = "test_update_registry.csv"

    data = []
    input_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    input_df.to_csv(input_file, index=False)

    update_registry(
        config_file="registry_config.yml",
        input_reg_file=input_file,
        output_reg_file=output_file,
        card_dir=os.path.join(".", "tests", "projects", "project_AB"),
        write_card_updates=False,
    )

    data = [
        ["node", 1001, "Project B"],
        ["node", 1002, "Project B"],
        ["node", 1003, "Project A"],
        ["node", 1004, "Project A"],
        ["link", 501, "Project B"],
        ["link", 502, "Project A"],
    ]
    target_i_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    target_i_df = target_i_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    data = [
        ["node", 1001, "Project A"],
        ["node", 1002, "Project A"],
        ["node", 1003, "Project B"],
        ["node", 1004, "Project B"],
        ["link", 501, "Project A"],
        ["link", 502, "Project B"],
    ]
    target_ii_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    target_ii_df = target_ii_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    outcome_df = pd.read_csv(output_file)
    outcome_df = outcome_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    os.remove(input_file)
    os.remove(output_file)

    assert (
        target_i_df.equals(outcome_df) is True
        or target_ii_df.equals(outcome_df) is True
    )


@pytest.mark.ci
@pytest.mark.update_registry
def test_update_registry_existing(request):

    input_file = "test_input_registry.csv"
    output_file = "test_update_registry.csv"
    data = [
        ["node", 1001, "Project Z"],
        ["node", 1002, "Project Z"],
        ["link", 501, "Project Z"],
    ]
    input_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    input_df.to_csv(input_file, index=False)

    update_registry(
        config_file="registry_config.yml",
        input_reg_file=input_file,
        output_reg_file=output_file,
        card_dir=os.path.join(".", "tests", "projects", "project_AB"),
        write_card_updates=False,
    )

    data = [
        ["node", 1001, "Project Z"],
        ["node", 1002, "Project Z"],
        ["link", 501, "Project Z"],
        ["node", 1003, "Project B"],
        ["node", 1004, "Project B"],
        ["node", 1005, "Project A"],
        ["node", 1006, "Project A"],
        ["link", 502, "Project B"],
        ["link", 503, "Project A"],
    ]
    target_i_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    target_i_df = target_i_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    data = [
        ["node", 1001, "Project Z"],
        ["node", 1002, "Project Z"],
        ["link", 501, "Project Z"],
        ["node", 1003, "Project A"],
        ["node", 1004, "Project A"],
        ["node", 1005, "Project B"],
        ["node", 1006, "Project B"],
        ["link", 502, "Project A"],
        ["link", 503, "Project B"],
    ]
    target_ii_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    target_ii_df = target_ii_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    outcome_df = pd.read_csv(output_file)
    outcome_df = outcome_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    os.remove(input_file)
    os.remove(output_file)

    assert (
        target_i_df.equals(outcome_df) is True
        or target_ii_df.equals(outcome_df) is True
    )


@pytest.mark.ci
@pytest.mark.update_registry
def test_update_registry_no_new_projects(request):

    input_file = "test_input_registry.csv"
    output_file = "test_update_registry.csv"

    data = [
        ["node", 1001, "Project B"],
        ["node", 1002, "Project B"],
        ["node", 1003, "Project A"],
        ["node", 1004, "Project A"],
        ["link", 501, "Project B"],
        ["link", 502, "Project A"],
    ]
    input_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    input_df.to_csv(input_file, index=False)

    update_registry(
        config_file="registry_config.yml",
        input_reg_file=input_file,
        output_reg_file=output_file,
        card_dir=os.path.join(".", "tests", "projects", "project_AB"),
        write_card_updates=False,
    )

    data = [
        ["node", 1001, "Project B"],
        ["node", 1002, "Project B"],
        ["node", 1003, "Project A"],
        ["node", 1004, "Project A"],
        ["link", 501, "Project B"],
        ["link", 502, "Project A"],
    ]
    target_i_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    target_i_df = target_i_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    data = [
        ["node", 1001, "Project A"],
        ["node", 1002, "Project A"],
        ["node", 1003, "Project B"],
        ["node", 1004, "Project B"],
        ["link", 501, "Project A"],
        ["link", 502, "Project B"],
    ]
    target_ii_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    target_ii_df = target_ii_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    outcome_df = pd.read_csv(output_file)
    outcome_df = outcome_df.sort_values(by=["type", "id"]).reset_index(drop=True)

    os.remove(input_file)
    os.remove(output_file)

    assert (
        target_i_df.equals(outcome_df) is True
        or target_ii_df.equals(outcome_df) is True
    )


@pytest.mark.ci
@pytest.mark.update_registry
def test_update_registry_no_new_nodes(request):

    input_file = "test_input_registry.csv"
    output_file = "test_update_registry.csv"

    data = []
    input_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    input_df.to_csv(input_file, index=False)

    update_registry(
        config_file="registry_config.yml",
        input_reg_file=input_file,
        output_reg_file=output_file,
        card_dir=os.path.join(".", "tests", "projects", "project_C"),
        write_card_updates=False,
    )

    data = [
        ["link", 501, "Project C"],
    ]
    
    target_df = pd.DataFrame(data, columns=["type", "id", "project_added"])
    target_df = target_df.sort_values(by=["type", "id"]).reset_index(drop=True)
    
    outcome_df = pd.read_csv(output_file)
    outcome_df = outcome_df.sort_values(by=["type", "id"]).reset_index(drop=True)
    
    os.remove(input_file)
    os.remove(output_file)
    
    assert (target_df.equals(outcome_df) is True)