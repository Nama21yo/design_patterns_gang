import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';
import { Observable } from 'rxjs';

@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(
    context: ExecutionContext,
  ): boolean | Promise<boolean> | Observable<boolean> {
    const request = context.switchToHttp().getRequest<{
      url: any;
      header: any;
    }>();
    console.log(`AuthGuard: Checking authentication `);
    const apiKey = request.header(`x-api-key`);
    console.log(`API Key: ${apiKey}`);
    if (apiKey !== 'SECRET') {
      console.log('AuthGuard: Authentication failed');
      return false;
    }
    console.log('AuthGuard: Authentication successful');
    return true;
  }
}
