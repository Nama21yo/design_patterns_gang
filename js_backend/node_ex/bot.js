const TelegramBot = require("node-telegram-bot-api");

// Replace with your bot token from BotFather
const token = "YOUR_BOT_TOKEN_HERE";
// https://publicapis.io/jokes-api
// Create bot
const bot = new TelegramBot(token, { polling: true });

// Handle /joke command
bot.onText(/\/joke/, async (msg) => {
  const chatId = msg.chat.id;
  try {
    const response = await fetch(
      "https://official-joke-api.appspot.com/random_joke"
    );
    const joke = await response.json();
    bot.sendMessage(chatId, `${joke.setup}\n\n${joke.punchline}`);
  } catch (error) {
    bot.sendMessage(chatId, "Sorry, could not get a joke right now!");
  }
});

// Handle all other messages
bot.on("message", (msg) => {
  if (!msg.text || msg.text.startsWith("/joke")) return;
  bot.sendMessage(msg.chat.id, "Type /joke to get a random joke! 😄");
});

console.log("Bot is running...");
