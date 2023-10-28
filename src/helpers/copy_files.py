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
    app_js_file = "App.js"
    app_js_test_file = "App.test.js"
    index_css_file = "index.css"
    index_js_file = "index.js"
    web_vitals_file = "reportWebVitals.js"
    set_up_test_file = "setupTests.js"
    copy_file(base_path + app_js_file, destination_dir + app_js_file)
    copy_file(base_path + app_js_test_file, destination_dir + app_js_test_file)
    copy_file(base_path + index_css_file, destination_dir + index_css_file)
    copy_file(base_path + index_js_file, destination_dir + index_js_file)
    copy_file(base_path + web_vitals_file, destination_dir + web_vitals_file)
    copy_file(base_path + set_up_test_file, destination_dir + set_up_test_file)


def copy_file(source_file: str, destination_file: str):
    shutil.copy(source_file, destination_file)
