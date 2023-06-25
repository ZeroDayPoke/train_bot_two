#!/usr/bin/env python3
""" Bot App Main """
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from console import Bot_Console


def run_bot():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    AUTHOR_ID = int(os.getenv('AUTHOR_ID'))
    GUILD_ID = int(os.getenv('GUILD_ID'))
    CHANNEL_ID_DEV = int(os.getenv('CHANNEL_ID_DEV'))
    CHANNEL_ID_PROD = int(os.getenv('CHANNEL_ID_PROD'))

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents)
    console = Bot_Console()

    async def send_message(message, user_message, is_private):
        try:
            response = str(user_message)
            await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as e:
            print(e)

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')

        """
        channel_id = CHANNEL_ID
        if channel_id is not None:
            try:
                channel_id = int(channel_id)
                channel = bot.get_channel(channel_id)
                if channel is not None:
                    await channel.send(f'{bot.user} mk 2 is online! Mission: the liberation of Anchorage, Alaska.')
                else:
                    print(f'Channel with ID {channel_id} not found.')
            except ValueError:
                print(f'Invalid channel ID: {channel_id}')

        cohort = discord.utils.get(bot.guilds, id=GUILD_ID)
        if cohort is None:
            print(f'Guild with ID {GUILD_ID} not found.')
            return
        for member in cohort.members:
            console.onecmd(f"create User username={member.name} discord_id={member.id} email={member.name}@llc19.us password={member.name}")
        """
    @bot.command(name='whoami')
    async def whoami(ctx):
        """Responds with the Discord username of the user who invoked the command."""
        await ctx.send(f'You are {ctx.author.name}')

    @bot.command(name='canhasgui')
    async def canhasgui(ctx):
        """Responds to user requesting GUI."""
        await ctx.send(f"GUI: https://llc19.us")

    @bot.command(name='canhasaccount')
    async def canhasaccount(ctx):
        """Checks if the user has an account, if not creates one."""
        # Get the user's Discord username
        username = ctx.author.name
        # Use the console to check if a User with that username exists
        if console.user_exists(username):
            # If the user exists, send them their login email
            await ctx.send(f'You already have an account. Your login email is {username}@llc19.us.')
        else:
            # If the user doesn't exist, use the console to create a new User
            console.onecmd(f"create User username={username} discord_id={ctx.author.id} email={username}@llc19.us password={username}")
            await ctx.send(f'New account created. Your login email is {username}@llc19.us.')


    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if not (message.channel.id == CHANNEL_ID_PROD or message.author.id == AUTHOR_ID or message.channel.id == CHANNEL_ID_DEV):
            return

        message_content = str(message.content)

        if message_content.startswith("tb "):
            console.onecmd(message_content[3:])
            console_response = console.get_output()
            print(console_response)
            if console_response == 'HCF':
                await send_message(message, 'Better dead than red...', False)
                await bot.close()
            privacy_flag = isinstance(message.channel, discord.DMChannel)
            await send_message(message, console_response, privacy_flag)

        await bot.process_commands(message)

    bot.run(TOKEN)
