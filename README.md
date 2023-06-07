# Backend generator for NodeJS
------------------------------------------------------------------------------------------------------------------------------------------------

- Use models_template.xlsx
Models for database representation for ORM

- In main.py change variables

- Create src folder for NestJS executing main

- Replace default src folder

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
        - Foreign Key(ManyToOne): foreign=[EntityRef,EntityRef property plural,EntityRef primary key type,EntityRef module name,EntityRef primary key property]
        - Foreign Key Reference(OneToMany): foreign_ref=[EntityForeign,EntityForeign property for join,empty,EntityForeign module name]