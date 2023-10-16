import shutil


def copy_essential_files(destination_dir: str):
    base_path = "essentials/"
    app_module_file = "app.module.ts"
    main_file = "main.ts"
    copy_file(base_path + app_module_file, destination_dir + app_module_file)
    copy_file(base_path + main_file, destination_dir + main_file)


def copy_react_essential_files(destination_dir: str):
    base_path = "react/"
    base_service_file = "base.service.js"
    copy_file(base_path + base_service_file, destination_dir + base_service_file)


def copy_react_essential_appjs_files(destination_dir: str):
    base_path = "react/"
    base_service_file = "App.js"
    copy_file(base_path + base_service_file, destination_dir + base_service_file)


def copy_file(source_file: str, destination_file: str):
    shutil.copy(source_file, destination_file)
