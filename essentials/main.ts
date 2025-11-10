import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import 'dotenv/config';
import * as bodyParser from 'body-parser';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.enableCors({
    origin: '*',
    methods: 'OPTIONS,GET,HEAD,PUT,PATCH,POST,DELETE',
    allowedHeaders: 'Content-Type,Authorization,Accept',
    preflightContinue: false,
    optionsSuccessStatus: 204,
  });

  const bodyParserLimitMb = process.env.BODY_PARSER_LIMIT_MB || '20mb';
  app.use(bodyParser.json({ limit: bodyParserLimitMb }));
  app.use(bodyParser.urlencoded({ limit: bodyParserLimitMb, extended: true }));

  const globalPrefix = process.env.GLOBAL_PREFIX || '';
  app.setGlobalPrefix(globalPrefix);

  await app.listen(Number(process.env.SERVER_PORT));
}
bootstrap();
