import {
  Get,
  Post,
  /*HttpCode,*/ Body,
  Param,
  Put,
  Res,
  HttpStatus,
  Logger,
} from '@nestjs/common';
import { BasicCrudService } from '../services/crud.service';
import { HttpResponse } from '../responses/http-response';
import express from 'express';
import { ObjectLiteral } from 'typeorm';

export abstract class BasicRestController<T extends ObjectLiteral, ID, D> {
  protected readonly logger = new Logger(BasicRestController.name);
  protected service!: BasicCrudService<T, ID, D>;

  // Do not forget constructor in implementation class to initialize service with specific ModuleService

  @Get('all')
  async findAll(@Res() res: express.Response): Promise<void> {
    try {
      const list = await this.service.findAll();
      res
        .status(HttpStatus.OK)
        .json(new HttpResponse<T>().setList(list).build(true));
    } catch (err) {
      this.logger.error('Error in findAll', (err as Error).message);
      res
        .status(HttpStatus.INTERNAL_SERVER_ERROR)
        .json(
          new HttpResponse<T>().setError((err as Error).message).build(false),
        );
    }
  }

  @Get('all-paged/:page/:limit')
  async findAllPaged(
    @Res() res: express.Response,
    @Param('page') page: number,
    @Param('limit') limit: number,
  ): Promise<void> {
    try {
      const list = await this.service.findAllPaged(page, limit);
      res
        .status(HttpStatus.OK)
        .json(new HttpResponse<T>().setPaged(list).build(true));
    } catch (err) {
      this.logger.error('Error in findAllPaged', (err as Error).message);
      res
        .status(HttpStatus.INTERNAL_SERVER_ERROR)
        .json(
          new HttpResponse<T>().setError((err as Error).message).build(false),
        );
    }
  }

  @Get('id/:id')
  async findById(
    @Res() res: express.Response,
    @Param('id') id: ID,
  ): Promise<void> {
    try {
      const data = await this.service.findById(id);
      res
        .status(HttpStatus.OK)
        .json(new HttpResponse<T>().setData(data).build(true));
    } catch (err) {
      this.logger.error('Error in findById', (err as Error).message);
      res
        .status(HttpStatus.INTERNAL_SERVER_ERROR)
        .json(
          new HttpResponse<T>().setError((err as Error).message).build(false),
        );
    }
  }

  @Post('create')
  async createOne(@Res() res: express.Response, @Body() dto: D): Promise<void> {
    try {
      const data = await this.service.createOne(dto);
      res
        .status(HttpStatus.CREATED)
        .json(new HttpResponse<T>().setData(data).build(true));
    } catch (err) {
      this.logger.error('Error in createOne', (err as Error).message);
      res
        .status(HttpStatus.INTERNAL_SERVER_ERROR)
        .json(
          new HttpResponse<T>().setError((err as Error).message).build(false),
        );
    }
  }

  @Put('edit/:id')
  async updateOne(
    @Res() res: express.Response,
    @Body() dto: D,
    @Param('id') id: ID,
  ): Promise<void> {
    try {
      const data = await this.service.updateOne(dto, id);
      res
        .status(HttpStatus.OK)
        .json(new HttpResponse<T>().setData(data).build(true));
    } catch (err) {
      this.logger.error('Error in updateOne', (err as Error).message);
      res
        .status(HttpStatus.INTERNAL_SERVER_ERROR)
        .json(
          new HttpResponse<T>().setError((err as Error).message).build(false),
        );
    }
  }
}
