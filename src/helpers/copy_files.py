import shutil


def copy_essential_files(destination_dir: str):
    base_path = "essentials/"
    app_module_file = "app.module.ts"
    main_file = "main.ts"
    env_example = "env-example"
    env_production_example = "env.production-example"

    copy_file(base_path + app_module_file, destination_dir + app_module_file)
    copy_file(base_path + main_file, destination_dir + main_file)
    copy_file(base_path + env_example, destination_dir + env_example)
    copy_file(base_path + env_production_example, destination_dir + env_production_example)


def copy_react_essential_files(destination_dir: str):
    base_path = "react/"
    base_service_file = "base.service.js"
    copy_file(base_path + base_service_file, destination_dir + base_service_file)


def copy_react_essential_appjs_files(destination_dir: str):
    base_path = "react/"
    app_jsx_file = "App.jsx"
    index_css_file = "index.css"
    main_jsx_file = "main.jsx"
    env_example_file = "env-example"
    copy_file(base_path + app_jsx_file, destination_dir + app_jsx_file)
    copy_file(base_path + index_css_file, destination_dir + index_css_file)
    copy_file(base_path + main_jsx_file, destination_dir + main_jsx_file)
    copy_file(base_path + env_example_file, destination_dir + env_example_file)


def copy_file(source_file: str, destination_file: str):
    shutil.copy(source_file, destination_file)
