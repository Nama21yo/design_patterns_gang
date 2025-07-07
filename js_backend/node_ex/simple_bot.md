# 🤖 Simple Telegram Joke Bot - Complete Setup Guide

## What the Bot Does

- Type `/joke` → Get a random joke
- Type anything else → Get instructions to use `/joke`

## Step 1: Get Your Bot Token

1. **Open Telegram** on your phone or computer
2. **Search for "BotFather"** (it has a blue checkmark)
3. **Start a chat** with BotFather
4. **Send this message**: `/newbot`
5. **Follow the prompts**:
   - Choose a name for your bot (e.g., "My Joke Bot")
   - Choose a username ending in "bot" (e.g., "myjokenbot")
6. **Copy the token** (looks like: `123456789:ABCdef-GhIjKlMnOpQrStUvWxYz`)

## Step 2: Setup Your Computer

1. **Create a new folder** on your computer called `joke-bot`
2. **Open Terminal/Command Prompt** and navigate to the folder:
   ```bash
   cd joke-bot
   ```
3. **Initialize the project**:
   ```bash
   npm init -y
   ```
4. **Install the Telegram bot library**:
   ```bash
   npm install node-telegram-bot-api
   ```

## Step 3: Create the Bot File

1. **Create a new file** called `bot.js` in your joke-bot folder
2. **Copy the code** from the artifact above
3. **Replace `YOUR_BOT_TOKEN_HERE`** with your actual token from BotFather

## Step 4: Run Your Bot

1. **In Terminal/Command Prompt**, run:
   ```bash
   node bot.js
   ```
2. **You should see**: `Bot is running...`

## Step 5: Test on Telegram

### Testing Steps:

1. **Find your bot** in Telegram:

   - Search for the username you created (e.g., @myjokenbot)
   - Click on your bot

2. **Test the joke command**:

   - Type: `/joke`
   - **Expected result**: You should get a random joke!

3. **Test the guidance message**:
   - Type: `hello`
   - **Expected result**: Bot should say "Type /joke to get a random joke! 😄"

### If It's Working:

✅ **Success!** Your bot is live and working!

### If It's NOT Working:

**Problem**: Bot doesn't respond

- **Check**: Is your terminal still running `node bot.js`?
- **Check**: Did you replace `YOUR_BOT_TOKEN_HERE` with your real token?
- **Check**: Is your internet connection working?

**Problem**: "polling_error" in terminal

- **Check**: Is your bot token correct?
- **Check**: Are you using the token from BotFather?

**Problem**: Bot says "could not get a joke"

- **Check**: Your internet connection
- **Wait**: A few seconds and try again

## Step 6: Stop the Bot

To stop your bot:

- **Press**: `Ctrl + C` in Terminal/Command Prompt
- **You'll see**: The bot stops running

## How to Start Again

1. **Open Terminal/Command Prompt**
2. **Navigate to your folder**: `cd joke-bot`
3. **Run**: `node bot.js`

## 🎉 Congratulations!

You now have a working Telegram bot that tells jokes! The bot is simple but fully functional:

- **15 lines of code** total
- **2 main functions**: Get jokes and give guidance
- **Easy to understand** and modify

### Want to Add More Features Later?

Once you're comfortable, you can:

- Add more joke categories
- Add buttons for "Another joke"
- Save favorite jokes
- Add other fun commands

But for now, enjoy your simple joke bot! 😄
