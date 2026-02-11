import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { JWTPayload } from './jwt.payload';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  // If you need to fetch entity data, inject your repository inside constructor params, like the code commented in the validate function
  // @InjectRepository(User)
  // private userRepo: Repository<User>
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: true,
      secretOrKey: process.env.JWT_SECRET ?? 'mock-secret',
    });
  }

  validate(payload: JWTPayload): boolean {
    return payload.userId !== undefined;
    /*
    const user = await this.userRepo.findOne({ where: { uuid: payload.userId }});
    if (!user) {
      throw new UnauthorizedException();
    }
    return user;
    */
  }
}
