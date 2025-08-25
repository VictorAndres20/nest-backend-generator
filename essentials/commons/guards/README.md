# Custom JWT AuthGuard

This is a custom AuthGuard to use as same AuthGuard('jwt'), but with this one you can play with @PublicEndpoint decorator to set a controller method as public endpoint. So you can do something like:

```Javascript
@Controller('employee')
@UseGuards(JwtAuthGuard) // Just like AuthGuard('jwt') but with the ability to set an endpoint public
export class EmployeeController extends BasicRestController<Employee, string, EmployeeDTO>{

    constructor(protected override service: EmployeeBusiness){super();}

    @Get('enterprise/:enterprise')
    async findAllByEnterprise(@Res() res: express.Response, @Param("enterprise") enterprise: number): Promise<void>{
        ...
    }

    @Get('enterprise/:enterprise/state/:state')
    async findAllByEnterpriseAndState(@Res() res: express.Response, @Param("enterprise") enterprise: number, @Param("state") state: number): Promise<void>{
        ...
    }

    @Get('identification/:identification')
    @PublicEndpoint() // THIS IS PUBLIC ENDPOINT            <------------------------------------------------------------
    async findByIdentification(@Res() res: express.Response, @Param("identification") identification: string): Promise<void>{
        ...
    }
}
```
