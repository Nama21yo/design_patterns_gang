import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getEmoji(index?: number): string {
    if (index !== undefined) {
      return this.getRandomEmoji(index);
    }
    return this.getRandomEmoji();
  }

  // I want to generate random emoji
  getRandomEmoji(index?: number): string {
    const emojis = ['😀', '😂', '😍', '🤔', '😎', '😭', '😡', '👍', '🙏', '🎉'];
    if (index !== undefined) {
      return emojis[index % emojis.length];
    }
    const randomIndex = Math.floor(Math.random() * emojis.length);
    return emojis[randomIndex];
  }
}
