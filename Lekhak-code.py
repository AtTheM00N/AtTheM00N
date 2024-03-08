import discord
from discord.ext import commands
import openai
import os
import requests

# Set up Discord bot
intents = discord.Intents.all()
intents.messages = True
intents.typing = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Set up OpenAI API key
openai.api_key = os.getenv("openai")


# Event handler for when the bot is ready
@bot.event
async def on_ready():
  print(f"We have logged in as {bot.user}")


@bot.event
async def on_command(ctx):
  print(f"Command invoked: {ctx.command} with args: {ctx.args}")


# Command to generate a story
@bot.command(name="generate_story", help="Generate a story based on a prompt.")
async def generate_story(ctx, *, prompt):
  response = generate_text(prompt, engine="text-davinci-003", max_tokens=150)
  await ctx.send(f"Generated Story:\n```\n{response}\n```")


# Command to generate a concept
@bot.command(name="generate_concept",
             help="Generate a concept based on a prompt.")
async def generate_concept(ctx, *, prompt):
  response = generate_text(prompt, engine="davinci-codex", max_tokens=50)
  await ctx.send(f"Generated Concept:\n```\n{response}\n```")


def generate_text(prompt, engine, max_tokens):
  url = "https://api.openai.com/v1/engines/" + engine + "/completions"
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {openai.api_key}",
  }

  data = {
      "prompt": prompt,
      "max_tokens": max_tokens,
  }

  response = requests.post(url, json=data, headers=headers)
  return response.json()["choices"][0]["text"].strip()


# Run the bot
discord_bot_token = os.getenv("Botkey")

if discord_bot_token:
  bot.run(discord_bot_token)
else:
  print("Error: Discord bot token not found in environment variables.")
