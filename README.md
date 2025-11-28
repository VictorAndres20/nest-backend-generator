# Database, Backend NestJS and Frontend React generator
------------------------------------------------------------------------------------------------------------------------------------------------

- Use [drawDB.io](https://github.com/drawdb-io/drawdb) JSON file as database representation to generate files

- In  a `.env` file update variable paths
See `env-example` file

- Generate src folder for NestJS executing main.py

- Create NestJS project with nest cli 

- Replace default src folder in NestJS project with generated one (`nest/src`)

- Install npm packages
```bash
npm install --save @nestjs/typeorm typeorm reflect-metadata
# npm install --save dotenv # No needed since new Node JS versions
npm install --save @nestjs/passport passport @nestjs/jwt passport-jwt
npm install --save-dev @types/passport-jwt
npm install bcrypt
npm install --save body-parser
```

- Install DB npm packages

MySQL
```bash
npm install --save mysql2
```

PostgreSQL
```bash
npm install --save pg
```

Oracle
```bash
npm install --save oracledb
```

- OPTIONAL
```bash
npm install --save exceljs
```

- Create React project with vite.
```
npm create vite@latest front-my-app
```

- Paste `react/src` generated folder inside your React app folder

- Create root `.env` following `env-example`

- Install `react-router-dom`

```bash
npm install --save react-router-dom
```

-----------------------------------------------

## JSON file model

> [!NOTE]
> You need to use a [drawDB.io](https://github.com/drawdb-io/drawdb) json file
> Export a [drawDB.io](https://github.com/drawdb-io/drawdb) model as JSON and use it as input file for this project 
