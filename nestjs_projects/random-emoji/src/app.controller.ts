import { Controller, Get, Query, Req } from '@nestjs/common';
import { AppService } from './app.service';
import { EmojiValidationPipe } from './common/emoji-validation/emoji-validation.pipe';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(
    @Req() request: Request,
    @Query(`index`, EmojiValidationPipe) index?: number,
  ): any {
    console.log(`Controller log Query para index ${index}`);
    return {
      emoji: this.appService.getEmoji(index),
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      browser: request.headers || 'Unknown',
    };
  }
}
