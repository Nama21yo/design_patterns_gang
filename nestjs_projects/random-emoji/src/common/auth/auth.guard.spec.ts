import { ExecutionContext } from '@nestjs/common';
import { AuthGuard } from './auth.guard';
import { createMock } from '@golevelup/ts-jest';

describe('AuthGuard', () => {
  it('should be defined', () => {
    expect(new AuthGuard()).toBeDefined();
  });

  // Add more tests for apikey == SECRET
  it('should allow access when API key is correct', () => {
    const context = createMock<ExecutionContext>({
      switchToHttp: () => ({
        getRequest: () => ({
          header: () => 'SECRET',
          headers: {
            'x-api-key': 'SECRET',
          },
        }),
      }),
    });
    const result = new AuthGuard().canActivate(context);
    expect(result).toBe(true);
  });
  // if apikey is wrong, should return false
  it('should deny access when API key is incorrect', () => {
    const context = createMock<ExecutionContext>({
      switchToHttp: () => ({
        getRequest: () => ({
          header: () => undefined,
          headers: {
            'x-api-key': undefined,
          },
        }),
      }),
    });
    const result = new AuthGuard().canActivate(context);
    expect(result).toBe(false);
  });
});
