import shutil
import os
from dotenv import dotenv_values

config = dotenv_values(".env")


def get_module_name(module_name: str):
    separator = config["MODULE_NOMENCLATURE_SEPARATOR"]

    if separator is None or separator == "_":
        return module_name

    return module_name.lower().replace("_", separator)


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def copy_essentials(destination_dir: str):
    base_path = "essentials/"
    commons_path = "commons"
    utils_path = "_utils"
    copy_folder(base_path + commons_path, destination_dir + commons_path)
    copy_folder(base_path + utils_path, destination_dir + utils_path)


def copy_react(destination_dir: str):
    base_path = "react/"
    utils_path = "_utils"
    hoc_path = "hoc"
    pages_path = "pages"
    config_path = "_config"
    hooks_path = "_hooks"
    widgets_path = "widgets"
    copy_folder(base_path + utils_path, destination_dir + utils_path)
    copy_folder(base_path + hoc_path, destination_dir + hoc_path)
    copy_folder(base_path + config_path, destination_dir + config_path)
    copy_folder(base_path + pages_path, destination_dir + pages_path)
    copy_folder(base_path + hooks_path, destination_dir + hooks_path)
    copy_folder(base_path + widgets_path, destination_dir + widgets_path)


def copy_react_ts(destination_dir: str):
    base_path = "react-ts/"
    utils_path = "_utils"
    assets_path = "assets"
    hoc_path = "hoc"
    pages_path = "pages"
    widgets_path = "widgets"
    copy_folder(base_path + utils_path, destination_dir + utils_path)
    copy_folder(base_path + assets_path, destination_dir + assets_path)
    copy_folder(base_path + hoc_path, destination_dir + hoc_path)
    copy_folder(base_path + pages_path, destination_dir + pages_path)
    copy_folder(base_path + widgets_path, destination_dir + widgets_path)


def copy_react_ts_api_client(destination_dir: str):
    base_path = "react-ts/"
    config_path = "_config"
    hooks_path = "_hooks"
    copy_folder(base_path + config_path, destination_dir + config_path)
    copy_folder(base_path + hooks_path, destination_dir + hooks_path)


def copy_folder(source_dir: str, destination_dir: str):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)
