import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { AuthService } from './service/auth.service';
import { JwtStrategy } from './service/jwt.strategy';

@Module({
  imports: [
    // If you need to fetch entity data uncomment the line below and replace your entity as needed
    //TypeOrmModule.forFeature([User]),
    JwtModule.register({
      secret: process.env.JWT_SECRET,
      signOptions: { expiresIn: '60d' },
    }),
  ],
  controllers: [],
  providers: [AuthService, JwtStrategy],
  exports: [AuthService],
})
export class AuthModule {}
