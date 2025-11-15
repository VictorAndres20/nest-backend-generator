# Database, Backend NestJS and Frontend React generator
------------------------------------------------------------------------------------------------------------------------------------------------

- Use [drawDB.io](https://github.com/drawdb-io/drawdb) JSON file as database representation to generate files

- In  a `.env` file update variable paths
See `env-example` file

- Generate src folder for NestJS executing main.py

- Create NestJS project with nest cli 

- Replace default src folder in NestJS project with generated one (`nest/src`)

- Install npm packages
```
npm install --save @nestjs/typeorm typeorm
npm install --save reflect-metadata
npm install --save dotenv
npm install --save @nestjs/passport passport @nestjs/jwt passport-jwt
npm install --save-dev @types/passport-jwt
npm install bcrypt
```
MySQL
```
npm install --save mysql2
```

PostgreSQL
```
npm install --save pg
```

Oracle
```
npm install --save oracledb
```

- OPTIONAL
```
npm install --save exceljs
npm install --save body-parser
```

- Create React project with vite.
```
npm create vite@latest front-my-app
```

- Paste `react/src` generated folder inside your React app folder

- Create root `.env` following `src/env-example`

- Install `react-router-dom`

-----------------------------------------------

## JSON file model

> [!NOTE]
> You need to use a [drawDB.io](https://github.com/drawdb-io/drawdb) json file
> Export a [drawDB.io](https://github.com/drawdb-io/drawdb) model as JSON and use it as input file for this project 
