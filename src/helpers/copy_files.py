import shutil


def copy_essential_files(destination_dir: str):
    base_path = "essentials/"
    app_module_file = "app.module.ts"
    main_file = "main.ts"
    copy_file(base_path + app_module_file, destination_dir + app_module_file)
    copy_file(base_path + main_file, destination_dir + main_file)


def copy_file(source_file: str, destination_file: str):
    shutil.copy(source_file, destination_file)
