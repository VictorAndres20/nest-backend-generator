# Auth module Implementation

- Copy Paste Auth folder in Api folder
- Add module in api.module or main.module
- Add Auth module in import module section where login is implemented
- Generate JWT
- Protect Routes. (see 'guards' folder)
- Login in your login service
  **UserService**

```typescript
    constructor(
        @InjectRepository(User)
        protected override repo: Repository<User>,
        private authService: AuthService,
    ) {super();}

    async login(userDTO: UserDTO): Promise<AuthDTO>{
        let user = await this.findByLogin(userDTO.login);
        if(! user){
          throw new Error("Error credentials");
        }

        if(! isSameEncrypted(userDTO.password, user.password)){
          throw new Error("Error credentials");
        }

        if(user.active !== 1) throw new Error(`Usuario no está activo`);
        let auth = new AuthDTO();
        auth.uuid = user.uuid;
        auth.login = user.login;
        auth.full_name = user.full_name;
        auth.root = user.root;
        auth.active = user.active
        auth.token = this.authService.generateAccessToken(user.uuid);
        return auth;
    }
```

UserController

```typescript
    @Post('login')
    @HttpCode(200)
    async login(@Body() dto: UserDTO): Promise<HttpResponse<AuthDTO>> {
        try{
            let data = await this.service.login(dto);
            return new HttpResponse<AuthDTO>().setData(data).build(true);
        } catch(err){
            return new HttpResponse<AuthDTO>().setError((err as Error).message).build(false);
        }
    }
```

Protect Routes

```typescript
    @Get('id/:id')
    @UseGuards(AuthGuard('jwt')) //===============> THIS
    async findById(
            @Param('id') uuid: string,
        ): Promise<HttpResponse<Client>> {
        try{
            let list = await this.service.findByUUID(uuid);
            return new HttpResponse<Client>().setData(list).build(true);
        } catch(err){
            throw new HttpException(new HttpResponse<Client>().setError((err as Error).message).build(false), 500);
        }
    }

```

or protect class

```typescript
@Controller('my-controller')
@UseGuards(AuthGuard('jwt')) //===============> THIS
export class MyController {
  @Get('id/:id')
  async findById(@Param('id') uuid: string): Promise<HttpResponse<Client>> {
    try {
      let list = await this.service.findByUUID(uuid);
      return new HttpResponse<Client>().setData(list).build(true);
    } catch (err) {
      throw new HttpException(
        new HttpResponse<Client>()
          .setError((err as Error).message)
          .build(false),
        500,
      );
    }
  }
}
```
