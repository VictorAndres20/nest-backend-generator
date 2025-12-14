# Abstract controller framework

## BasicRestController

This controller provide 4 basic CRUD actions with implementation.

- FindById
- FindAll
- CreateOne
- updateOne

### Implementation

To implement this controller, extends your Nest Controller from BasicRestController<T, ID, D>
Be careful with generics, you need:

- T: Nest Entity class (Class with @Entity decorator, typeORM ObjectLiteral)
- ID: Primary key type for entity
- D: Entity DTO Class.

```typescript
// Imports
@Controller('my-example')
export class MyExampleController extends BasicRestController<
  MyExample,
  string,
  MyExampleDTO
> {
  //Constructor
}
```

Now, is important for this implementation to extends your primary service from BasicCrudService
**See README in commons/services**
And implement contructor

```typescript
// Imports
@Controller('my-example')
export class MyExampleController extends BasicRestController<
  MyExample,
  string,
  MyExampleDTO
> {
  constructor(override readonly service: MyExampleService) {
    super();
  }
}
```

At this point, your controller has already 4 Basic CRUD operations ready to use!
**NOTES**

- You can write more functions for endpoints.
- You can override any function if you need to.
