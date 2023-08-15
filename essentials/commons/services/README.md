# Basic CRUD service framework

## BasicCrudService
This asbtract Class provides methods to create a service with 4 CRUD operations
- FindById
- FindAll
- CreateOne
- EditOne
- FindAllPaged
**This works with TypeORM**

#### Implementation
Extends your service class from BasicCrudService<T, ID, D>.
Generics are:
- T: Nest Entity class (Class with @Entity decorator)
- ID: Primary key type for entity
- D: Entity DTO Class. 
```
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
// Imports

@Injectable()
export class MyExampleService extends BasicCrudService<Example, string, ExampleDTO>{

    //Constructor

    //Methods
}
```

Then, inject your Entity for TypeORM repository in constructor
```
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
// Imports

@Injectable()
export class MyExampleService extends BasicCrudService<Example, string, ExampleDTO>{

    constructor(
    @InjectRepository(Calendar)
    protected repo: Repository<Calendar>,
    ) {
        super();
    }

    //Methods
}
```

Then implement methods:
- findById(T: ID): Promise<T>
- buildBaseCreation(dto: D): T
- dataValidationBeforeCreate(dto: D): Promise<void>
- buildBaseEdition(entity: T, dto: D): T
- dataValidationBeforeEdit(dto: D): Promise<void>
```
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
// Imports

@Injectable()
export class MyExampleService extends BasicCrudService<MyExample, string, MyExampleDTO>{
  
  constructor(
    @InjectRepository(MyExample)
    protected repo: Repository<MyExample>,
  ) {
    super();
  }

  findById(id: string): Promise<MyExample>{
    try{
      return this.findOne({where: {uuid:id}});
    } catch(err){
      throw new Error(err.message);
    }
  }

  buildBaseCreation(dto: CalendarDTO): MyExample {
    //Validations data
    if(! dto) throw new Error('DTO empty');

    //Assign data
    let entity = new Calendar()
    entity.name = dto.name;
    // ...

    return entity;
  }

  async dataValidationBeforeCreate(dto: CalendarDTO): Promise<void> {
    // Input validations for null values that are required
    // For example validate if not exists for specific(s) properties
    // Example same login, same email, same COD, same NIT
  }

  buildBaseEdition(entity: Calendar, dto: CalendarDTO): Calendar {
    //Validations data
    if(! dto) throw new Error('Entity null');
    if(! dto.uuid) throw new Error('Entity id null');

    //Assign data
    entity.name = dto.name ? dto.name : entity.name;
    // ...

    return entity;
  }

  async dataValidationBeforeEdit(dto: CalendarDTO): Promise<void> {
    // Input validations for null values that are required
    // For example validate if not exists for specific(s) properties
    // Example same login, same email, same COD, same NIT
  }

}
```