import { Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { JWTPayload } from './jwt.payload';

@Injectable()
export class AuthService {
  constructor(private jwtService: JwtService) {}

  generateAccessToken(id: string): string {
    const payload: JWTPayload = { userId: id };
    return this.jwtService.sign(payload);
  }
}
