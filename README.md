# Backend generator for NodeJS
------------------------------------------------------------------------------------------------------------------------------------------------

- Use models_template.xlsx
Models for database representation for ORM

- In main.py change variables paths

- Create src folder for NestJS executing main.py

- Create NestJS project with nest cli 

- Replace default src folder in NestJS project with generated one

- Install npm packages

-----------------------------------------------

## models_template.xlsx Usage
- All sheets are models name (tables)

- Sheet columns info:
1ROW: Columns names **(DONT TOUCH IT)**
2ROW: Entity name
2ROW: Primary Key it could be (PrimaryGeneratedColumn() or PrimaryColumn())
nROW: Other properties:
        - Normal Columns: Column() or Column({ select: false })
        - Foreign Key(ManyToOne): foreign
        - Foreign Key Reference(OneToMany): foreign_ref

### FOREIGN COLUMNS EXPLANATION
- FOREIGN_ENTITY: Foreign Key Entity class name
- FE_PROPERTY: Foreign Key Entity property that make the relation
- FE_PK_TYPE: Foreign Key Entity PRIMARY KEY type
- FE_PK: Foreign Key Entity PRIMARY KEY property
- FE_MODULE: Foreign Key Entity module package name