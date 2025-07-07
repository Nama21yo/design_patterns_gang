Here's a detailed guide to building a **Telegram Bot** that fetches and displays random jokes using the `node-telegram-bot-api` library in Node.js, incorporating the provided Jokes API example. The bot will respond to commands like `/start` and `/joke`, fetching jokes from the Official Joke API (`https://official-joke-api.appspot.com/random_joke`).

---

### Project: Telegram Joke Bot

#### Description
This project creates a Telegram bot that:
- Responds to `/start` with a welcome message.
- Responds to `/joke` by fetching a random joke from the Official Joke API and sending the setup and punchline.
- Uses `node-telegram-bot-api` for Telegram integration and `fetch` for API calls (adapting the provided example).

#### Prerequisites
- Node.js (v14 or higher)
- A Telegram account
- Basic JavaScript/Node.js knowledge

#### Steps to Build the Bot

1. **Get a Bot Token**
   - Open Telegram, search for `@BotFather`, and start a chat.
   - Send `/newbot`, follow prompts to name your bot (e.g., `@JokeBot`), and receive a **Bot Token** (e.g., `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`).
   - Save the token securely.

2. **Set Up the Project**
   - Create a project directory:
     ```bash
     mkdir telegram-joke-bot
     cd telegram-joke-bot
     ```
   - Initialize a Node.js project:
     ```bash
     npm init -y
     ```
   - Install the `node-telegram-bot-api` library:
     ```bash
     npm install node-telegram-bot-api
     ```

3. **Write the Bot Code**
   - Create a file named `bot.js` and add the following code, adapting the provided Jokes API example:

   ```javascript
   const TelegramBot = require('node-telegram-bot-api');

   // Replace with your bot token from BotFather
   const token = 'YOUR_BOT_TOKEN_HERE';

   // Create a bot that uses 'polling' to fetch new updates
   const bot = new TelegramBot(token, { polling: true });

   // Handle /start command
   bot.onText(/\/start/, (msg) => {
     const chatId = msg.chat.id;
     bot.sendMessage(chatId, 'Welcome to the Joke Bot! Send /joke to hear a random joke.');
   });

   // Handle /joke command
   bot.onText(/\/joke/, async (msg) => {
     const chatId = msg.chat.id;
     try {
       const response = await fetch('https://official-joke-api.appspot.com/random_joke', {
         method: 'GET',
         headers: {
           'Content-Type': 'application/json'
         }
       });

       const data = await response.json();
       // Send the joke setup and punchline
       bot.sendMessage(chatId, `${data.setup}\n\n${data.punchline}`);
     } catch (error) {
       bot.sendMessage(chatId, 'Oops, couldn’t fetch a joke! Try again later.');
       console.error('Error fetching joke:', error);
     }
   });

   // Log any polling errors
   bot.on('polling_error', (error) => {
     console.error('Polling error:', error);
   });

   console.log('Joke Bot is running...');
   ```

   - Replace `'YOUR_BOT_TOKEN_HERE'` with your actual bot token.
   - The code uses the `fetch` API as shown in your example to get a random joke from `https://official-joke-api.appspot.com/random_joke`.

4. **Run the Bot**
   - Start the bot:
     ```bash
     node bot.js
     ```
   - You should see `Joke Bot is running...` in the console.

5. **Test the Bot**
   - In Telegram, find your bot (e.g., `@JokeBot`) and send:
     - `/start` → Bot replies: "Welcome to the Joke Bot! Send /joke to hear a random joke."
     - `/joke` → Bot fetches a joke (e.g., "Why did the scarecrow become a motivational speaker? Because he was outstanding in his field!").

6. **Deploy (Optional)**
   - To run the bot 24/7, deploy to a cloud platform:
     - **Heroku** or **Render**: Free tiers available for Node.js apps.
     - **VPS**: Use DigitalOcean or AWS for more control.
     - For production, consider switching from polling to webhooks (see `node-telegram-bot-api` docs).
   - Ensure your bot token is stored securely (e.g., in environment variables).

7. **Extend the Bot (Optional Ideas)**
   - Add a `/category` command to fetch jokes by type (e.g., programming, general) using the API’s `/jokes/<type>/random` endpoint.
   - Implement a button interface with `reply_markup` for users to request another joke.
   - Store favorite jokes in a JSON file or database when users send a `/save` command.
   - Add error retry logic for failed API calls.

---

#### Notes
- **API Details**: The Official Joke API (`https://official-joke-api.appspot.com/random_joke`) returns a JSON object with `setup` and `punchline`. No API key is needed.
- **Security**: Keep your bot token private. Use environment variables (e.g., `process.env.BOT_TOKEN`) for deployment.
- **Error Handling**: The code includes basic error handling for failed API requests. Enhance it for robustness in production.
- **Resources**:
  - [node-telegram-bot-api GitHub](https://github.com/yagop/node-telegram-bot-api)
  - [Official Joke API](https://github.com/15Dkatz/official_joke_api)
  - [Telegram Bot API Docs](https://core.telegram.org/bots/api)

This project is simple, leverages the provided API example, and is a great way to learn Node.js, Telegram bots, and API integration. Let me know if you need help with setup, extensions, or debugging!
