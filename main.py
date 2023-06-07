from src.controllers.generate_module_code import generate_module

models_path = "/home/viti/KoalaSoftwareSAS/projects/KS_Platform/2.Develop/modules/"
excel_path = models_path + "models.xlsx"


def execute():
    generate_module(models_path, excel_path)


if __name__ == '__main__':
    execute()
