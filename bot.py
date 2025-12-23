import discord
import random
import os
from discord.ext import commands
import requests
import time
import asyncio

from tipspolusi import tipschoosing
from polutionfacts import factchoosing
from climate import TRASH_ITEMS
from climate import SHOP_ITEMS
from climate import UNIQUE_ITEMS
from climate import WATER_TRASH
from climate import EXPLORE_LOCATIONS

ALL_TRASH_PRICES = {
    **TRASH_ITEMS, 
    **WATER_TRASH 
}

try:
    from climate import ClimateGames
except ImportError:
    class ClimateGames:
        def __init__(self, bot):
            print("PERINGATAN: Modul ClimateGames tidak ditemukan. Fungsi game tidak akan bekerja.")
        def get_inventory(self, user_id):
            return []

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

GAME_SYSTEM = ClimateGames(bot)

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
        "- '!meme' - Dapatkan meme lingkungan yang lucu! \n\n"
        "- '!gamemenu' - Mainkan game edukasi lingkungan yang seru!"
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

@bot.command()
async def gamemenu(ctx):
    await ctx.send("Inilah menu permainan edukasi lingkungan yang bisa kamu mainkan:\n\n"
                   "- '!inventory' - Cek item lingkungan yang kamu miliki.\n" 
                   "- '!shop' - Beli item lingkungan untuk membantu misimu.\n"
                   "- '!explore' - Jelajahi lingkungan virtual untuk menemukan item baru.\n"
                   "- '!collect' - Kumpulkan item lingkungan dari sekitarmu.\n" 
                   "- '!plantree' - Tanam pohon virtual untuk membantu lingkungan.\n" 
                   "- '!cleanwater' - Bersihkan sumber air dari polusi.\n"
                   "- '!recycle' - Daur ulang item yang sudah kamu kumpulkan.\n"
                   "- '!reuse' - Gunakan kembali item untuk mengurangi limbah.\n\n")

@bot.command()
@commands.is_owner()
async def givepoints(ctx, amount: int):
    """Memberikan poin secara instan untuk testing."""
    user_id = ctx.author.id
    GAME_SYSTEM.update_score(user_id, amount)
    
    new_score = GAME_SYSTEM.get_score(user_id)
    await ctx.send(f"Menambahkan {amount} poin. Total poin kamu sekarang: **{new_score}**.")

@bot.command()
@commands.is_owner() 
async def discard(ctx, *, item_name: str = None):
    """Membuang item dari inventaris."""
    if item_name is None:
        await ctx.send("❓ Item apa yang ingin kamu buang? Contoh: `!discard Botol Plastik`.")
        return

    item_name = item_name.strip().title()
    user_id = ctx.author.id

    # Panggil fungsi dari GAME_SYSTEM
    success = GAME_SYSTEM.remove_item_from_inventory(user_id, item_name, quantity=1)

    if success:
        await ctx.send(f"🗑️ Berhasil membuang **{item_name}** dari inventaris kamu.")
    else:
        await ctx.send(f"❌ Kamu tidak memiliki **{item_name}** di dalam inventaris.")

@bot.command()
@commands.is_owner()
async def cleartrash(ctx):
    """Removes all collected trash from the inventory while keeping tools."""
    user_id = ctx.author.id
    
    # Convert your UNIQUE_ITEMS set into a list for the SQL query
    tools_to_keep = list(UNIQUE_ITEMS)
    
    # Ask for a simple confirmation or just execute
    try:
        GAME_SYSTEM.clear_trash_data(user_id, tools_to_keep)
        
        embed = discord.Embed(
            title="🧹 Inventoris telah dibersihkan",
            description=f"{ctx.author.mention}, semua item anda dihapus. Tetapi alat anda tetap aman!",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        print(f"Eror ketika membersih item: {e}")
        await ctx.send("❌ An error occurred while trying to clear your inventory.")

@bot.command()
async def inventory(ctx):
    """Displays user inventory categorized by Tools and Collected Items."""
    user_id = ctx.author.id
    inventory_list = GAME_SYSTEM.get_inventory(user_id)
    current_score = GAME_SYSTEM.get_score(user_id)

    if not inventory_list:
        await ctx.send("🎒 Inventaris kamu kosong. Coba gunakan `!collect`!")
        return

    # Categories
    tools = []
    collected_items = []

    # UNIQUE_ITEMS should be defined in your code (from our previous step)
    # UNIQUE_ITEMS = {"Sekop", "Tepung Tulang", "Sarung Tangan", etc.}

    for name, quantity in inventory_list:
        if name in UNIQUE_ITEMS:
            tools.append(f" - **{name}**")
        else:
            collected_items.append(f"- {name}: x{quantity}")

    # Create Embed for better look
    embed = discord.Embed(
        title=f"🎒 Inventaris {ctx.author.name}\n",
        description=f"♻️ Total Eco-Score kamu saat ini: **{current_score}** poin.\n",
        color=discord.Color.blue()
    )

    if tools:
        embed.add_field(name="🧰 Peralatan (Tools)", value="\n".join(tools), inline=False)
    else:
        embed.add_field(name="🧰 Peralatan (Tools)", value="Belum ada alat.", inline=False)

    if collected_items:
        embed.add_field(name="📦 Barang Terkumpul", value="\n".join(collected_items), inline=False)

    embed.set_footer(text="Gunakan !shop untuk membeli peralatan baru!")
    
    await ctx.send(embed=embed)

@bot.command()
async def shop(ctx):
    user_id = ctx.author.id

    embed = discord.Embed(
        title="🏪 Toko Alat Lingkungan",
        description=f"Selamat datang di toko, {ctx.author.mention}! Gunakan `!shopbuy [Nama Item]` untuk membeli.",
        color=discord.Color.green()
    )
    embed.add_field(
        name="1. Sekop (200 Eco-Points)",
        value="**Fungsi:** Untuk mempercepat proses menanam pohon. *(Mempercepat aksi game `!plantree`.)*",
        inline=False
    )

    embed.add_field(
        name="2. Tepung Tulang (300 Eco-Points)",
        value="**Fungsi:** Meningkatkan kualitas pohon yang ditanam. *(Meningkatkan Eco-Points yang didapat dari `!plantree`.)*",
        inline=False
    )

    embed.add_field(
        name="3. Sarung Tangan (500 Eco-Points)",
        value="**Fungsi:** Melindungi tanganmu saat mengumpulkan sampah. *(Mempercepat proses pengumpulan sampah `!collect`.)*",
        inline=False
    )

    embed.add_field(
        name="4. Tas Daur Ulang (250 Eco-Points)",
        value="**Fungsi:** Memungkinkan kamu mengumpulkan lebih banyak item sekaligus. *(Memberi kesempatan mengumpulkan lebih dari satu sampah saat `!collect`.)*",
        inline=False
    )

    embed.add_field(
        name="5. Jaring Pengumpul (530 Eco-Points)",
        value="**Fungsi:** Memudahkan pengumpulan sampah di air. *(Memberi kesempatan mengumpulkan lebih dari satu sampah di air saat `!cleanwater`.)*",
        inline=False
    )

    embed.add_field(
        name="6. Alat Pengambil (600 Eco-Points)",
        value="**Fungsi:** Memudahkan pengambilan sampah berbahaya. *(Mempercepat proses pengambilan sampah di air saat `!cleanwater`.)*",
        inline=False
    )

    embed.add_field(
        name="7. Teropong (1000 Eco-Points)",
        value="**Fungsi:** Memperluas pandanganmu saat menjelajahi lingkungan. *(Memberi kesempatan melihat lebih banyak item saat `!explore`.)*",
        inline=False
    )

    embed.add_field(
        name="8. Ransel (1500 Eco-Points)",
        value="**Fungsi:** Membawa lebih banyak item saat menjelajah. *(Meningkatkan kapasitas inventaris saat `!explore`.)*",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command()
async def shopbuy(ctx, *, item_name: str = None):
    """Membeli item dari toko menggunakan Eco-Points."""
    user_id = ctx.author.id

    if item_name is None:
        await ctx.send(f"{ctx.author.mention}, Mohon sebutkan item yang ingin dibeli! Coba `!shop` untuk melihat daftarnya.")
        return

    item_name = item_name.strip().title()
    
    if item_name not in SHOP_ITEMS:
        await ctx.send(f"{ctx.author.mention}, Item **'{item_name}'** tidak ditemukan di toko. Pastikan ejaan item sudah benar.")
        return

    price = SHOP_ITEMS[item_name]
    
    try:
        current_score = GAME_SYSTEM.get_score(user_id)
        inventory_list = GAME_SYSTEM.get_inventory(user_id)
    except Exception as e:
        print(f"Database error during buy command: {e}")
        await ctx.send("❌ Terjadi kesalahan saat mencoba mengakses data game. Mohon coba lagi nanti.")
        return
    
    if item_name in UNIQUE_ITEMS:
        is_owned = any(name == item_name for name, quantity in inventory_list)
        
        if is_owned:
            await ctx.send(
                f"🚫 {ctx.author.mention}, kamu sudah memiliki item **{item_name}** ini. "
                "Item ini adalah *peralatan unik* dan tidak bisa dibeli berulang kali."
            )
            return

    if current_score < price:
        await ctx.send(
            f"💰 Maaf, {ctx.author.mention}. Eco-Points kamu (**{current_score}**) tidak cukup untuk membeli **{item_name}** (**{price}**)."
        )
        return

    GAME_SYSTEM.update_score(user_id, -price)

    GAME_SYSTEM.add_item_to_inventory(user_id, item_name, quantity=1)
    
    new_score = GAME_SYSTEM.get_score(user_id)
    
    embed = discord.Embed(
        title="✅ Pembelian Berhasil!",
        description=f"{ctx.author.mention} berhasil membeli **{item_name}**!",
        color=discord.Color.blue()
    )
    embed.add_field(name="Harga", value=f"-{price} Eco-Points", inline=True)
    embed.add_field(name="Sisa Poin", value=f"{new_score} Eco-Points", inline=True)
    embed.set_footer(text="Cek inventaris kamu dengan !inventory.")

    await ctx.send(embed=embed)

@bot.command()
async def collect(ctx):
    user_id = ctx.author.id

    if GAME_SYSTEM.owns_item(user_id, "Sarung Tangan"):
        collection_time = 2  # Reduced time (e.g., from 5s to 2s)
        time_text = f"Tunggu **{collection_time} detik** sampai sampah terkumpul..."
    else:
        collection_time = 5
        time_text = f"Tunggu **{collection_time} detik** sampai sampah terkumpul..."

    if GAME_SYSTEM.owns_item(user_id, "Tas Daur Ulang"):
        quantity_collected = 2 if random.random() < 0.5 else 1 
        if quantity_collected == 2:
            quantity_text = f" dan membawa **{quantity_collected} item** sekaligus!"
        else:
            quantity_text = "."
    else:
        quantity_collected = 1
        quantity_text = "."

    initial_embed = discord.Embed(
        title="♻️ Sedang Mengumpulkan Sampah...",
        description=f"{ctx.author.mention} {time_text}{quantity_text}",
        color=discord.Color.green())

    status_message =await ctx.send(embed=initial_embed)

    await asyncio.sleep(collection_time)

    total_points = 0
    collected_items = []

    for _ in range(quantity_collected):
        collected_item = random.choice(list(TRASH_ITEMS.keys()))
        points_awarded = TRASH_ITEMS[collected_item]
        
        # Add item and update score (use your existing methods)
        GAME_SYSTEM.add_item_to_inventory(user_id, collected_item, quantity=1)
        GAME_SYSTEM.update_score(user_id, points_awarded)
        
        total_points += points_awarded
        collected_items.append(collected_item)
        
    current_score = GAME_SYSTEM.get_score(user_id)

    collected_list_text = "\n".join([f"- **{item}**" for item in collected_items])

    result_embed = discord.Embed(
        title=f"♻️ Pengumpulan Sampah Berhasil! (x{quantity_collected})",
        description=(
            f"{ctx.author.mention} berhasil mengumpulkan item berikut:\n"
            f"{collected_list_text}"
        ),
        color=discord.Color.green()
    )
    
    result_embed.add_field(name="Total Poin Diterima", value=f"**+{total_points}** Eco-Points", inline=False)
    result_embed.add_field(name="Total Eco-Score", value=f"Kamu sekarang memiliki **{current_score}** Eco-Points.", inline=False)
    result_embed.set_footer(text="Gunakan !inventory untuk melihat item yang kamu kumpulkan!")

    await status_message.edit(embed=result_embed)

@bot.command()
async def planttree(ctx):
    user_id = ctx.author.id

    if GAME_SYSTEM.owns_item(user_id, "Sekop"):
        plant_time = 5  
        time_text = f"Tunggu **{plant_time} detik** sampai sampah terkumpul..."
    else:
        plant_time = 10
        time_text = f"Tunggu **{plant_time} detik** sampai sampah terkumpul..."

    if GAME_SYSTEM.owns_item(user_id, "Tepung Tulang"): 
        extra_text = f"Eco-Points yang telah di berikan dari penanaman pohon ini **dikalikan 2** berkat penggunaan Tepung Tulang!"
    else:
        extra_text = f""

    embed = discord.Embed(
        title="🌲 Menanamkan Pohon...",
        description=f"{ctx.author.mention} {time_text}",
        color=discord.Color.green())
    
    await ctx.send(embed=embed)

    await asyncio.sleep(plant_time)  # Simulasi waktu menanam pohon

    work_quality = random.randint(1,10)
    points_awarded = work_quality * 5 * (2 if GAME_SYSTEM.owns_item(user_id, "Tepung Tulang") else 1)
    
    GAME_SYSTEM.update_score(user_id, points_awarded)
    
    current_score = GAME_SYSTEM.get_score(user_id)

    embed = discord.Embed(
        title=f"🌲 Penanaman Pohon Berhasil! Kualitas Kerja: {work_quality}/10",
        description=f"{ctx.author.mention} berhasil mendapatkan {points_awarded} Eco-Points dari menanam pohon!\n {extra_text}",
        color=discord.Color.green()
    )
    embed.add_field(name="Poin Diterima", value=f"**+{points_awarded}** Eco-Points", inline=False)
    embed.add_field(name="Total Eco-Score", value=f"Kamu sekarang memiliki **{current_score}** Eco-Points.", inline=False)
    embed.set_footer(text="Gunakan !inventory untuk melihat item yang kamu kumpulkan!")

    await ctx.send(embed=embed)

@bot.command()
async def cleanwater(ctx):
    user_id = ctx.author.id

    if GAME_SYSTEM.owns_item(user_id, "Alat Pengambil"):
        wait_time = 3
    else:
        wait_time = 10

    num_items = 1
    if GAME_SYSTEM.owns_item(user_id, "Jaring Pengumpul"):
        if random.random() < 0.5: 
            num_items = 2

    embed = discord.Embed(
        title="🌊 membersihkan air...",
        description=f"{ctx.author.mention} sedang membersihkan sampah dari air.\n"
                    f"Tunggu **{wait_time} detik** sampai sampah terkumpul...",
        color=discord.Color.blue()
    )
    status_msg = await ctx.send(embed=embed)

    await asyncio.sleep(wait_time)

    items = list(WATER_TRASH.keys())
    #Common: 60%, Uncommon: 25%, Rare: 10%, Legendary: 5%)
    weights = [20, 20, 20, 12.5, 12.5, 5, 5, 2.5, 2.5]
    
    found_items = []
    total_points = 0

    for _ in range(num_items):
        item_name = random.choices(items, weights=weights, k=1)[0]
        points = WATER_TRASH[item_name]
        
        GAME_SYSTEM.add_item_to_inventory(user_id, item_name, quantity=1)
        GAME_SYSTEM.update_score(user_id, points)
        
        found_items.append(item_name)
        total_points += points

    current_score = GAME_SYSTEM.get_score(user_id)
    
    result_text = "\n".join([f"• **{item}**" for item in found_items])
    
    result_embed = discord.Embed(
        title=f"🌊 Pengumpulan Sampah Berhasil (x{num_items})",
        description=f"{ctx.author.mention}, berhasil mengumpulkan item berikut:\n{result_text}",
        color=discord.Color.dark_blue()
    )
    result_embed.add_field(name="Total Poin Diterima", value=f"**+{total_points}** Eco-Points", inline=False)
    result_embed.add_field(name="Total Eco-Score", value=f"Kamu sekarang memiliki **{current_score}** Eco-Points.", inline=False)
    result_embed.set_footer(text="Gunakan !inventory untuk melihat item yang kamu kumpulkan!")

    await status_msg.edit(embed=result_embed)

@bot.command()
async def reuse(ctx):
    """Membersihkan inventory dan memberikan bonus Eco-Points setiap Milestone."""
    user_id = ctx.author.id
    tools_to_keep = list(UNIQUE_ITEMS)
    
    # Eksekusi logika upcycle
    amount_added, old_total, new_total = GAME_SYSTEM.upcycle_all_trash(user_id, tools_to_keep)

    if amount_added > 0:
        # Menentukan Title (English)
        if new_total < 50:
            rank = "Scrap Collector 🛠️"
        elif new_total < 200:
            rank = "Upcycle Apprentice ✨"
        elif new_total < 500:
            rank = "Eco-Artist 🎨"
        else:
            rank = "Master of Restoration 👑"

        embed = discord.Embed(
            title="🎨 Eco-Art Project Updated!",
            description=f"{ctx.author.mention}, kamu telah menyumbangkan **{amount_added} item** ke proyek seni komunitas!",
            color=discord.Color.purple()
        )
        embed.add_field(name="Total Items Upcycled", value=f"**{new_total}**", inline=True)
        embed.add_field(name="Current Title", value=f"**{rank}**", inline=True)

        # --- LOGIKA MILESTONE BONUS ---
        # Memberikan 200 poin setiap kelipatan 50 item
        milestone_interval = 50
        points_per_milestone = 200
        
        # Hitung berapa milestone yang dilewati kali ini
        milestones_passed = (new_total // milestone_interval) - (old_total // milestone_interval)
        
        if milestones_passed > 0:
            total_bonus = milestones_passed * points_per_milestone
            GAME_SYSTEM.update_score(user_id, total_bonus)
            
            embed.add_field(
                name="⭐ Milestone Reached!", 
                value=f"Selamat! Kamu melewati **{milestones_passed} Milestone** dan mendapatkan bonus **{total_bonus} Eco-Points**!", 
                inline=False
            )

        await ctx.send(embed=embed)
    else:
        await ctx.send("🎒 Inventarismu kosong atau hanya berisi peralatan (Tools). Ayo kumpulkan sampah terlebih dahulu!")

@bot.command()
async def recycle(ctx):
    user_id = ctx.author.id
    tools_to_keep = list(UNIQUE_ITEMS)

    items_count, points_earned = GAME_SYSTEM.recycle_all_trash(
        user_id, ALL_TRASH_PRICES, tools_to_keep
    )

    if items_count > 0:
        new_score = GAME_SYSTEM.get_score(user_id)
            
        embed = discord.Embed(
            title="♻️ Recycling Center",
            description=f"{ctx.author.mention}, kamu berhasil mendaur ulang **{items_count} item**!",
            color=discord.Color.green()
        )
        embed.add_field(name="Points Earned", value=f"+{points_earned} ⭐", inline=True)
        embed.add_field(name="Total Eco-Score", value=f"{new_score} ⭐", inline=True)
        embed.set_footer(text="Terima kasih telah membantu menjaga kebersihan dunia!")
            
        await ctx.send(embed=embed)
    else:
        await ctx.send("🎒 Kamu tidak memiliki sampah untuk didaur ulang! Kumpulkan sampah dulu dengan `!collect` atau `!cleanwater`.")      
    
@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def explore(ctx):
    user_id = ctx.author.id
    
    location = random.choice(list(EXPLORE_LOCATIONS.keys()))
    items_available = EXPLORE_LOCATIONS[location]
    
    embed = discord.Embed(
        title="🧭 Explorasi Telah Dimulai",
        description=f"{ctx.author.mention}, kamu sedang melakukan perjalanan ke **{location}**...\nMohon tunggu sebentar.",
        color=discord.Color.gold()
    )
    msg = await ctx.send(embed=embed)
    
    await asyncio.sleep(5)

    found = random.sample(items_available, 2)

    for item in found:
        GAME_SYSTEM.add_item_to_inventory(user_id, item, 1)
        
    result_embed = discord.Embed(
        title="🧭 Hasil Explorasi: " + location,
        description=f"Kamu telah kembali dari **{location}** dan menemukan beberapa barang menarik!",
        color=discord.Color.green()
    )
    result_embed.add_field(name="Items Found", value="\n".join([f"• {i}" for i in found]))
    result_embed.set_footer(text="Gunakan !inventory untuk melihat koleksimu.")
    
    await msg.edit(embed=result_embed)

@explore.error
async def explore_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Kamu terlalu lelah untuk menjelajah! Coba lagi dalam **{error.retry_after:.0f} detik**.")
                
bot.run("-")
