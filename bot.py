import discord
import random
import os
from discord.ext import commands
import requests

from passgen import gen_pass
botlist = []

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def generatepassword(ctx, count_letters = 10):
    await ctx.send(gen_pass(count_letters))

@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

@bot.command()
async def subtract(ctx, left: int, right: int):
    await ctx.send(left - right)

@bot.command()
async def multiply(ctx, left: int, right: int):
    await ctx.send(left * right)

@bot.command()
async def divide(ctx, left: int, right: int):
    await ctx.send(left / right)

@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def openlist(ctx):
    if botlist:
        items = "\n".join(f"- {item}" for item in botlist)
        await ctx.send(f"Your list:\n{items}")
    else:
        await ctx.send("Your list is empty!")

@bot.command()
async def addlist(ctx, *, item: str):
    botlist.append(item)
    await ctx.send(f"Added '{item}' to the list!")

@bot.command()
async def removelist(ctx, *, item: str):
    try:
        botlist.remove(item)
        await ctx.send(f" Removed '{item}' from the list!")
    except ValueError:
        await ctx.send(f"'{item}' was not found in the list.")
    
@bot.command()
async def meme(ctx):
    rarity = random.randint(1,1000)
    if rarity <= 500:
        img_name = random.choice(os.listdir('commonmeme'))
        with open(f'commonmeme/{img_name}', 'rb') as f:
            picture = discord.File(f)
        await ctx.send(f"Common Meme! :thumbsup: ", file=picture)
        
    
    elif 501 <= rarity <= 900:
        img_name = random.choice(os.listdir('rarememe'))
        with open(f'rarememe/{img_name}', 'rb') as f:
            picture = discord.File(f)
        await ctx.send(f"Rare Meme! :fire: ", file=picture)
    
    
    elif rarity >= 901:
        img_name = random.choice(os.listdir('legendarymeme'))
        with open(f'legendarymeme/{img_name}', 'rb') as f:
            picture = discord.File(f)
        await ctx.send(f"Legendary Meme! :star: ", file=picture)
        

    

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def plshelp(ctx):
    help_text = """
**Available Commands:**
- `$generatepassword [count_letters]` — Generates a random password (default 10 characters).
- `$add <num1> <num2>` — Adds two numbers.
- `$subtract <num1> <num2>` — Subtracts second number from the first.
- `$multiply <num1> <num2>` — Multiplies two numbers.
- `$divide <num1> <num2>` — Divides first number by the second.
- `$roll NdN` — Rolls dice (e.g., `!roll 2d6`).
- `$addlist <item>` — Adds an item to the list.
- `$openlist` — Shows your list.
- `$removelist <item>` — Removes an item from the list.
- `$meme` — Shows a meme.
"""
    await ctx.send(help_text)


bot.run("-")