import discord
import random
import os
from discord.ext import commands
import requests

from tipspolusi import tipschoosing
from polutionfacts import factchoosing

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def perkenalan(ctx):
    await ctx.send("Halo! Aku adalah **EcoBot**. \n\n"
        "Aku bisa membantumu memahami dan mengurangi **polusi lingkungan**, "
        "langsung dari rumahmu!\n\n"
        " Coba perintah-perintah berikut:\n"
        "- `!polusi` — Penjelasan umum tentang polusi\n"
        "- `!polusianudara` — Apa itu pencemaran polusi?\n"
        "- `!polusilaut` — Penjelasan tentang polusi laut\n"
        "- `!sumberpolusi` — Sumber-Sumber polusi di dalam dunia kita\n"
        "- `!faktapolusi` — Sumber-Sumber polusi di dalam dunia kita\n"
        "- `!tipspolusi` — Tips mengurangi polusi dari rumah \n\n"
        "Yuk, bersama-sama kita jaga bumi! \n\n"
        "- '!meme' - Dapatkan meme lingkungan yang lucu!"
    )

@bot.command()
async def polusi(ctx):
    await ctx.send("Masuknya atau dimasukkannya makhluk hidup, zat, energi, atau komponen lain ke dalam lingkungan (air, udara, atau tanah) yang menyebabkan perubahan kualitas lingkungan dan mengganggu fungsi lingkungan tersebut. ")

@bot.command()
async def polusitanah(ctx):
    await ctx.send("Pencemaran tanah terjadi saat tanah tercemar limbah beracun seperti plastik, pestisida, atau logam berat, yang merusak kesuburan tanah dan membahayakan lingkungan serta kesehatan manusia.")

@bot.command()
async def polusianair(ctx):
    await ctx.send("Pencemaran air adalah masuknya zat berbahaya seperti limbah, minyak, atau bahan kimia ke dalam air (sungai, laut, danau), yang merusak kualitas air dan membahayakan makhluk hidup di dalamnya.")

@bot.command()
async def polusiudara(ctx):
    await ctx.send("Kondisi di mana udara terkontaminasi oleh zat-zat berbahaya atau beracun, baik dalam bentuk gas, partikel, maupun bahan kimia, yang dapat membahayakan kesehatan manusia, hewan, tumbuhan, dan lingkungan.")

@bot.command()
async def polusilaut(ctx):
    await ctx.send("masuk atau dimasukkannya makhluk hidup, zat, energi, atau komponen lain ke dalam lingkungan laut oleh kegiatan manusia, sehingga kualitas air laut menurun dan tidak sesuai lagi dengan baku mutu dan/atau fungsinya.")   

@bot.command()
async def sumberpolusi(ctx):
    await ctx.send("Sumber polusi adalah segala sesuatu yang menyebabkan pencemaran lingkungan, baik itu udara, air, maupun tanah. Sumber ini bisa berasal dari aktivitas manusia maupun alam, dan dapat berupa zat padat, cair, atau gas yang merugikan kesehatan dan keseimbangan lingkungan.")
    await ctx.send( "**Sumber Pencemaran Udara**\n"
        "• Asap kendaraan bermotor - melepaskan gas karbon monoksida dan partikel berbahaya ke udara.\n"
        "• Pembakaran sampah - menghasilkan zat kimia beracun yang mencemari udara dan membahayakan kesehatan.\n\n"
        "**Sumber Pencemaran Air**\n"
        "• Limbah rumah tangga - seperti sabun, deterjen, dan minyak yang mencemari saluran air dan sungai.\n"
        "• Limbah industri - bahan kimia dari pabrik yang dibuang tanpa pengolahan ke sungai atau laut.\n\n"
        "**Sumber Pencemaran Tanah**\n"
        "• Sampah plastik - dibuang sembarangan dan sulit terurai, mencemari tanah dalam jangka panjang.\n"
        "• Pestisida berlebihan - merusak kesuburan tanah dan mencemari air tanah di sekitarnya.")
@bot.command()
async def tipspolusi(ctx):
    await ctx.send(tipschoosing())

@bot.command()
async def faktapolusi(ctx):
    await ctx.send(factchoosing())

@bot.command()
async def climatememe(ctx):
    img_name = random.choice(os.listdir('climatememe'))
    with open(f'climatememe/{img_name}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(f"Meme lingkungan! :earth_africa: ", file=picture)

bot.run("-")
