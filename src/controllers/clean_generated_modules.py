import os

from src.controllers.generate_module_code import GENERATED_FOLDERS
from src.helpers.folder_handler import remove_folder


def clean_generated_modules(output_dir: str):
    for folder in GENERATED_FOLDERS:
        generated_module_path = os.path.join(output_dir, folder)
        remove_folder(generated_module_path)
