import os
from network_wrangler import ProjectCard

CARD_DIR = os.path.join(".", "projects")


def read_project_cards(card_dir: str = CARD_DIR) -> list:
    """
    Returns a list of project cards from a directory.

    Args:
        card_dir: a folder location storing project cards

    Returns:
        List of tuples, with the ProjectCard and card filename

    """

    card_file_list = []
    for (dirpath, dirnames, filenames) in os.walk(card_dir):
        for filename in filenames:
            name, extension = os.path.splitext(filename)
            if extension in [".yml", ".yaml"]:
                card_file = os.path.join(dirpath, filename)
                card = ProjectCard.read(card_file, validate=False)
                card_file_list.append((card, card_file))

    return card_file_list
