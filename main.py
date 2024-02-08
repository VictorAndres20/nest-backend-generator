from src.controllers.generate_module_code import generate_module

models_path = "/home/viti/Documents/KoalaSoftwareSAS/projects/advances/1.Design/models/"
excel_path = models_path + "models.xlsx"

# db_schema = None
db_schema = 'ks'
generate_foreign_keys = True


def execute():
    generate_module(models_path, excel_path, db_schema, generate_foreign_keys)


if __name__ == '__main__':
    execute()
