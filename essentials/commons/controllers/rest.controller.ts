import { Get, Post, HttpCode, Body, Param, Put, Res, HttpStatus } from '@nestjs/common';
import { BasicCrudService } from '../services/crud.service';
import { HttpResponse } from '../responses/http_response';
import { Response } from 'express';

export abstract class BasicRestController<T, ID, D> {

    protected service: BasicCrudService<T, ID, D>

    // Do not forguet constructor in implememtation class to initialize service with specific ModuleService

    @Get('all')
    async findAll(@Res() res: Response): Promise<void> {
        try{
            let list = await this.service.findAll();
            res.status(HttpStatus.OK).json(new HttpResponse<T>().setList(list).build(true));
        } catch(err){
            res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(new HttpResponse<T>().setError(err.message).build(false));
        }
    }

    @Get('all-paged/:page/:limit')
    async findAllPaged(@Res() res: Response, @Param("page") page: number, @Param("limit") limit: number): Promise<void>{
        try{
            let list = await this.service.findAllPaged(page, limit);
            res.status(HttpStatus.OK).json(new HttpResponse<T>().setPaged(list).build(true));
        } catch(err){
            res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(new HttpResponse<T>().setError(err.message).build(false));
        }
    }

    @Get('id/:id')
    async findById(@Res() res: Response, @Param('id') id: ID): Promise<void> {
        try{
            let data = await this.service.findById(id);
            res.status(HttpStatus.OK).json(new HttpResponse<T>().setData(data).build(true));
        } catch(err){
            res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(new HttpResponse<T>().setError(err.message).build(false));
        }
    }

    @Post('create')
    async createOne(@Res() res: Response, @Body() dto: D): Promise<void> {
        try{
            let data = await this.service.createOne(dto);
            res.status(HttpStatus.CREATED).json(new HttpResponse<T>().setData(data).build(true));
        } catch(err){
            res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(new HttpResponse<T>().setError(err.message).build(false));
        }
    }

    @Put('edit/:id')
    async editOne(@Res() res: Response, @Body() dto: D, @Param('id') id: ID): Promise<void> {
        try{
            let data = await this.service.editOne(dto, id);
            res.status(HttpStatus.OK).json(new HttpResponse<T>().setData(data).build(true));
        } catch(err){
            res.status(HttpStatus.INTERNAL_SERVER_ERROR).json(new HttpResponse<T>().setError(err.message).build(false));
        }
    }
}
