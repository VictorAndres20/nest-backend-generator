import shutil
import os


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
    copy_folder(base_path + utils_path, destination_dir + utils_path)
    copy_folder(base_path + hoc_path, destination_dir + hoc_path)
    copy_folder(base_path + config_path, destination_dir + config_path)
    copy_folder(base_path + pages_path, destination_dir + pages_path)
    copy_folder(base_path + hooks_path, destination_dir + hooks_path)


def copy_folder(source_dir: str, destination_dir: str):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    shutil.copytree(source_dir, destination_dir)
