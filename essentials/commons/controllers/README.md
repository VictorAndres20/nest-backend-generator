# Abstract controller framework

## BasicRestController
This controller provide 4 basic CRUD actions with implementation. 
- FindById
- FindAll
- CreateOne
- EditOne

###### Implementation
To implement this controller, extends your Nest Controller from BasicRestController<T, ID, D>
Be carefull with generics, you need:
- T: Nest Entity class (Class with @Entity decorator)
- ID: Primary key type for entity
- D: Entity DTO Class. 
```
// Imports
@Controller('my-example')
export class MyExampleController extends BasicRestController<Example, string, ExampleDTO>{

    //Constructor
    
}
```

Now, is important for this implementation to extends your primary service from BasicCrudService
**See README in commons/services**
And implement contructor
```
// Imports
@Controller('my-example')
export class MyExampleController extends BasicRestController<Example, string, ExampleDTO>{

    constructor(protected service: MyExampleService){
        super();
    }
    
}
```

At this ponit, your controller has already 4 Basic CRUD operations ready to use!

**NOTES** 
- You can write more functions for endpoints.
- You can override any function if you need to.