from numpy import True_
import pandas as pd
from typing import Tuple
from network_wrangler import ProjectCard


def add_cards_to_registry(
    card_file_list: list, input_df: pd.DataFrame, config: dict, write_to_disk: bool
) -> pd.DataFrame:
    """
    Returns an updated registry dataframe.

    Args:
        card_file_list: a list of project cards and their filenames
        input_df: input registry DataFrame. See the format in `registry.csv`.
        config: input configuration
        write_to_disk: a boolean indicating whether project card updates should be written
            to disk. If True, the input project cards will be overwritten.

    Returns:
        Registry DataFrame updated

    """

    nodes_in_use = _make_available("nodes", config)
    links_in_use = _make_available("links", config)
    out_df = input_df

    for card, filename in card_file_list:
        card_dict = card.__dict__
        if "project" in card_dict:
            project_name = card_dict.get("project", "Missing")
            if project_name not in input_df["project_added"].values:
                if "changes" in card_dict:
                    card_needs_updating = False
                    for change_index, change_dict in enumerate(card_dict["changes"]):
                        if "nodes" in change_dict:
                            (
                                node_df,
                                node_update,
                                updated_change_dict,
                            ) = _update_registry(
                                "nodes",
                                out_df,
                                change_dict,
                                project_name,
                                nodes_in_use,
                            )
                        else:
                            node_df = None
                            node_update = False

                        link_df, link_update, updated_change_dict = _update_registry(
                            "links",
                            out_df,
                            change_dict,
                            project_name,
                            links_in_use,
                        )

                        if node_df is not None:
                            out_df = out_df.append(node_df, ignore_index=True)

                        out_df = (
                            out_df.append(link_df, ignore_index=True)
                            .drop_duplicates()
                            .reset_index(drop=True)
                        )

                        if node_update or link_update:
                            card_needs_updating = True
                            change_dict.update(updated_change_dict)
                            card_dict[change_index] = updated_change_dict

                    if card_needs_updating:
                        card.__dict__.update(card_dict)
                        if write_to_disk:
                            card.write(filename=filename)

                if "category" in card_dict:
                    if "nodes" in card_dict:
                        node_df, node_update, updated_card_dict = _update_registry(
                            "nodes",
                            out_df,
                            card_dict,
                            project_name,
                            nodes_in_use,
                        )
                    else:
                        node_df = None
                        node_update = False

                    link_df, link_update, updated_card_dict = _update_registry(
                        "links",
                        out_df,
                        card_dict,
                        project_name,
                        links_in_use,
                    )

                    if node_df is not None:
                        out_df = out_df.append(node_df, ignore_index=True)

                    out_df = (
                        out_df.append(link_df, ignore_index=True)
                        .drop_duplicates()
                        .reset_index(drop=True)
                    )

                    if link_update or node_update:
                        card.__dict__.update(updated_card_dict)
                        if write_to_disk:
                            card.write(filename=filename)

    return out_df


def _make_available(nodes_or_links: str, config: dict) -> list:
    """
    Converts dictionary of available nodes and links to list of available nodes
    Args:
        nodes_or_links: string, either 'nodes' or 'links'
        config: input configuration
    Returns:
        list of available nodes
    """
    if nodes_or_links == "nodes":
        key_word = "nodes_used_by_geography"
        min_id = config.get("minimum_allowable_node_id")
        max_id = config.get("maximum_allowable_node_id")
    else:
        key_word = "links_used_by_geography"
        min_id = config.get("minimum_allowable_link_id")
        max_id = config.get("maximum_allowable_link_id")

    subject_dict = config.get(key_word)

    ids_in_use = {n: False for n in range(min_id, max_id + 1)}
    for entry in subject_dict:
        temp_start = entry.get("start")
        temp_end = entry.get("end")
        for id in range(temp_start, temp_end + 1):
            ids_in_use[id] = True

    return ids_in_use


def _is_id_in_allowable_range(
    nodes_or_links: str,
    project_name: str,
    subject_id: int,
    range_in_use: dict,
):
    """
    Checks if the new node or link id is in the allowable range defined in the config file

    Args:
        nodes_or_links (str): "node" or "link", which is used in error message
        project_name (str): project name, which is used in error message
        subject_id (int): the proposed new node or link id number
        range_in_use (dict): a dictionary defining the id range with a bool indicating if the id number is used in the base network

    Raises:
        ValueError: informs the user of the disconnect between config file and the Project Card
    """
    if subject_id not in range_in_use:
        msg = (
            "New {} id ({}) in project '{}' is not in the base networks allowable range"
            "({} to {}) as defined in the configuration file.".format(
                nodes_or_links,
                project_name,
                min(range_in_use.keys()),
                max(range_in_use.keys()),
            )
        )
        raise ValueError(msg)


def _is_id_used_in_base_network(
    nodes_or_links: str,
    project_name: str,
    subject_id: int,
    range_in_use: dict,
):
    """
    Checks if new node or link id is used in the base network as defined in the config file

    Args:
        nodes_or_links (str): "node" or "link", which is used in error message
        project_name (str): project name, which is used in error message
        subject_id (int): the proposed new node or link id number
        range_in_use (dict): a dictionary defining the id range with a bool indicating if the id number is used in the base network

    Raises:
        ValueError: informs the user of the disconnect between the config file and the Project Card
    """
    if subject_id in range_in_use:
        if range_in_use[subject_id] == True:
            msg = (
                "New {} id ({}) in project '{}' is in use in the base network. "
                "Please check that the base network {}s are defined correctly in "
                "the config file.".format(
                    nodes_or_links,
                    subject_id,
                    project_name,
                    nodes_or_links,
                )
            )
            raise ValueError(msg)


def _find_available_id(
    nodes_or_links: str,
    project_name: str,
    subject_id: str,
    range_in_use: dict,
    subject_df: pd.DataFrame,
) -> int:
    """
    If the node or link id is already in the registry and we need to find a new number, this method iterates up from
    the proposed node number to find the next available id, which it returns.

    Args:
        nodes_or_links (str): "node" or "link", which is used in error message
        project_name (str): project name, which is used in error message
        subject_id (int): the proposed new node or link id number
        range_in_use (dict): a dictionary defining the id range with a bool indicating if the id number is used in the base network
        subject_df (pd.DataFrame): node or link registry dataframe

    Returns:
        int: available node or link id
    """

    number = subject_id
    for i in range(subject_id, max(range_in_use.keys())):
        if i not in subject_df["id"].values:
            if range_in_use[i] == False:
                number = i
                break

    if number == subject_id:
        msg = "Software failed to find an available number for {} id ({}) in project '{}'. " "Please check that the base network {}s are defined correctly in the config file.".format(
            nodes_or_links,
            subject_id,
            project_name,
            nodes_or_links,
        )

    return number


def _update_registry(
    nodes_or_links: str,
    input_df: pd.DataFrame,
    change_dict: dict,
    project_name: str,
    range_in_use: dict,
) -> Tuple[pd.DataFrame, bool, dict]:
    """
    Updates node or link entries in the registry database

    Args:
        nodes_or_links: input string, 'nodes' or 'links'
        input_df: input registry DataFrame
        change_dict: input dictionary of a project card change
        project_name: string name of the project
        start: largest node number in the existing network

    Returns:
        An updated registry database with new node entries
        A flag as to whether the card needs to be modified
        An updated dictionary of the card entries
    """
    write_updated_card = False

    if nodes_or_links == "nodes":
        subject_word = "node"
        subject_id_word = "model_node_id"
    else:
        subject_word = "link"
        subject_id_word = "model_link_id"

    subject_df = input_df[input_df["type"] == subject_word]

    if change_dict["category"] == "Add New Roadway":
        for subject_index, subject in enumerate(change_dict[nodes_or_links]):
            new_id = subject[subject_id_word]

            _is_id_in_allowable_range(subject_word, project_name, new_id, range_in_use)
            _is_id_used_in_base_network(
                subject_word, project_name, new_id, range_in_use
            )
            if new_id not in subject_df["id"].values:
                updates_df = pd.DataFrame(
                    {
                        "type": subject_word,
                        "id": [new_id],
                        "project_added": [project_name],
                    }
                )
                subject_df = subject_df.append(updates_df)
            else:
                number = _find_available_id(
                    subject_word,
                    project_name,
                    new_id,
                    range_in_use,
                    subject_df,
                )
                change_dict[nodes_or_links][subject_index][subject_id_word] = number
                if nodes_or_links == "nodes":
                    for i in range(0, len(change_dict["links"])):
                        if change_dict["links"][i]["A"] == new_id:
                            change_dict["links"][i]["A"] = number
                        if change_dict["links"][i]["B"] == new_id:
                            change_dict["links"][i]["B"] = number
                updates_df = pd.DataFrame(
                    {
                        "type": subject_word,
                        "id": [number],
                        "project_added": [project_name],
                    }
                )
                subject_df = subject_df.append(updates_df)
                write_updated_card = True

    return subject_df, write_updated_card, change_dict
