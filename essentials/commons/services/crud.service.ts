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

  abstract buildBaseCreation(dto: D): T;

  abstract dataValidationBeforeCreate(dto: D): Promise<void>;

  abstract buildBaseEdition(entity: T, dto: D): T;

  abstract dataValidationBeforeEdit(entity: T, dto: D): Promise<void>;

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
      await this.dataValidationBeforeCreate(dto);
      return this.repo.save(this.buildBaseCreation(dto));
    } catch (err) {
      throw new Error((err as Error).message);
    }
  }

  async editOne(dto: D, id: ID): Promise<T> {
    try {
      const entity = await this.findById(id);
      if (entity == null) {
        throw new Error('Entity not found for edition');
      }
      await this.dataValidationBeforeEdit(entity, dto);
      return this.repo.save(this.buildBaseEdition(entity, dto));
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
