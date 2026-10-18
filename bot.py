import os
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

MY_GUILD = discord.Object(id=1561157589511839898)
DROP_CH = 1561163117726011533
BANNER = "http://googleusercontent.com/generated_animated_image/15959043500870823950"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class ColdShopBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        print("✅ [COLDSHOP] Bot gotowy i zsynchronizowany!")

bot = ColdShopBot()

# --- WSPÓLNA OBSŁUGA ZAMKNIĘCIA TICKETU ---
class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Zamknij", style=discord.ButtonStyle.danger, custom_id="close_t")
    async def close(self, inter: discord.Interaction, btn: discord.ui.Button):
        await inter.response.send_message("Usuwanie ticketa za 3 sekundy...", ephemeral=True)
        await asyncio.sleep(3)
        await inter.channel.delete()

# --- OBSŁUGA TICKETÓW PO WYBORZE Z MENU ---
class ShopSelect(discord.ui.Select):
    def __init__(self, placeholder: str, options: list):
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=True)
        product_name = self.values[0]
        ch = await inter.guild.create_text_channel(
            name=f"ticket-{inter.user.name.lower()}",
            overwrites={
                inter.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                inter.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                inter.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )
        embed = discord.Embed(
            title=f"COLDSHOP Ticket: {product_name}",
            description=f"Witaj {inter.user.mention}!\nOtworzyłeś ticket zakupowy dla: **{product_name}**.",
            color=discord.Color.blue()
        )
        await ch.send(content=f"{inter.user.mention}", embed=embed, view=CloseView())
        await inter.followup.send(f"✅ Stworzono ticket: {ch.mention}", ephemeral=True)

# --- SYSTEM LEGIT CHECK ---
class LegitView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.y, self.n = 0, 0

    @discord.ui.button(label="0", emoji="✅", style=discord.ButtonStyle.success, custom_id="leg_y")
    async def yes(self, inter: discord.Interaction, btn: discord.ui.Button):
        self.y += 1
        btn.label = str(self.y)
        await inter.response.edit_message(view=self)
        await inter.followup.send("Dzięki za głos!", ephemeral=True)

    @discord.ui.button(label="0", emoji="❌", style=discord.ButtonStyle.danger, custom_id="leg_n")
    async def no(self, inter: discord.Interaction, btn: discord.ui.