import { Get, Post, HttpCode, Body, Param, Put } from '@nestjs/common';
import { BasicCrudService } from '../services/crud.service';
import { HttpResponse } from '../responses/http_response';

export abstract class BasicRestController<T, ID, D> {

    protected service: BasicCrudService<T, ID, D>

    // Do not forguet constructor in implememtation class to initialize service with specific ModuleService

    @Get('all')
    async findAll(): Promise<HttpResponse<T>> {
        try{
            let list = await this.service.findAll();
            return new HttpResponse<T>().setList(list).build(true);
        } catch(err){
            return new HttpResponse<T>().setError(err.message).build(false);
        }
    }

    @Get('id/:id')
    async findById(@Param('id') id: ID): Promise<HttpResponse<T>> {
        try{
            let data = await this.service.findById(id);
            return new HttpResponse<T>().setData(data).build(true);
        } catch(err){
            return new HttpResponse<T>().setError(err.message).build(false);
        }
    }

    @Post('create')
    @HttpCode(201)
    async createOne(@Body() dto: D): Promise<HttpResponse<T>> {
        try{
            let data = await this.service.createOne(dto);
            return new HttpResponse<T>().setData(data).build(true);
        } catch(err){
            return new HttpResponse<T>().setError(err.message).build(false);
        }
    }

    @Put('edit/:id')
    @HttpCode(201)
    async editOne(@Body() dto: D, @Param('id') id: ID): Promise<HttpResponse<T>> {
        try{
            let data = await this.service.editOne(dto, id);
            return new HttpResponse<T>().setData(data).build(true);
        } catch(err){
            return new HttpResponse<T>().setError(err.message).build(false);
        }
    }
}
