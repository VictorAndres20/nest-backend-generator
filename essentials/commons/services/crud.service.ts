/**
 * OPTIONS https://orkhan.gitbook.io/typeorm/docs/find-options
 */

import {
  FindManyOptions,
  FindOneOptions,
  ObjectLiteral,
  Repository,
} from 'typeorm';

export abstract class BasicCrudService<T extends ObjectLiteral, ID, D> {
  protected repo!: Repository<T>;

  // Do not forget constructor to inject repo with T entity

  abstract findById(id?: ID | null): Promise<T | null>;

  abstract dtoTransformBeforeCreate(dto: D): D;

  abstract buildBaseEntityToCreate(dto: D): T;

  abstract dataValidationBeforeCreate(dto: D): Promise<void>;

  abstract dtoTransformBeforeEdit(dto: D): D;

  abstract buildBaseEntityToUpdate(entity: T, dto: D): T;

  abstract dataValidationBeforeUpdate(entity: T, dto: D): Promise<void>;

  findAll(): Promise<T[]> {
    try {
      return this.repo.find();
    } catch (err) {
      throw new Error((err as Error).message);
    }
  }

  findOne(options: FindOneOptions<T>): Promise<T | null> {
    try {
      return this.repo.findOne(options);
    } catch (err) {
      throw new Error((err as Error).message);
    }
  }

  findMany(options: FindManyOptions<T>): Promise<T[]> {
    try {
      return this.repo.find(options);
    } catch (err) {
      throw new Error((err as Error).message);
    }
  }

  async createOne(dto: D): Promise<T> {
    try {
      const dtoToCreate = this.dtoTransformBeforeCreate(dto);
      await this.dataValidationBeforeCreate(dtoToCreate);
      return this.repo.save(this.buildBaseEntityToCreate(dtoToCreate));
    } catch (err) {
      throw new Error((err as Error).message);
    }
  }

  async updateOne(dto: D, id: ID): Promise<T> {
    try {
      const entity = await this.findById(id);
      if (entity == null) {
        throw new Error('Entity not found for edition');
      }
      const dtoToUpdate = this.dtoTransformBeforeEdit(dto);
      await this.dataValidationBeforeUpdate(entity, dtoToUpdate);
      return this.repo.save(this.buildBaseEntityToUpdate(entity, dtoToUpdate));
    } catch (err) {
      throw new Error((err as Error).message);
    }
  }

  async findAllPaged(page = 0, limit = 8): Promise<[T[], number]> {
    return await this.repo.findAndCount({ skip: page, take: limit });
  }

  protected _buildForeignEntityFromIdCallback<FT>(
    dto: D,
    fn: (dto: D) => FT | null
  ): FT | null {
    return fn(dto);
  }
}
