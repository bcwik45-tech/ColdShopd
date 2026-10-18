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
    async def no(self, inter: discord.Interaction, btn: discord.ui.Button):
        self.n += 1
        btn.label = str(self.n)
        await inter.response.edit_message(view=self)
        await inter.followup.send("Dzięki za głos!", ephemeral=True)

# --- KOMENDY SETUPU ---

@bot.tree.command(name="setup_legitchecks", description="Panel legit check")
@app_commands.checks.has_permissions(administrator=True)
async def sl(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    embed = discord.Embed(title="⭐ COLDSHOP × LEGIT CHECK", description="Kliknij ✅ lub ❌", color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=LegitView())
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_bundle", description="Panel Bundle")
@app_commands.checks.has_permissions(administrator=True)
async def sb(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    options = [
        discord.SelectOption(label="Steam Account", value="Steam Account", emoji=discord.PartialEmoji(name="steam", id=1561307761617281165)),
        discord.SelectOption(label="Discord Account", value="Discord Account", emoji=discord.PartialEmoji(name="discord", id=1561307671397929001)),
        discord.SelectOption(label="Rockstar Account", value="Rockstar Account", emoji=discord.PartialEmoji(name="rockstar", id=1561308861636542524)),
        discord.SelectOption(label="FiveM Bundle", value="FiveM Bundle", description="Cały pakiet: Discord + Steam + Rockstar", emoji=discord.PartialEmoji(name="fivem", id=1561307556360749086))
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="Wybierz konto / pakiet Bundle", options=options))
    embed = discord.Embed(title="📦 COLDSHOP × BUNDLE", description="Wybierz konto lub pakiet z listy poniżej:", color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=v)
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_vpn", description="Panel VPN")
@app_commands.checks.has_permissions(administrator=True)
async def svpn(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    options = [
        discord.SelectOption(label="IP Vanish", value="IP Vanish VPN", emoji=discord.PartialEmoji(name="ipvanish", id=1561307428643930152)),
        discord.SelectOption(label="NexHub", value="NexHub VPN", emoji=discord.PartialEmoji(name="nexhub", id=1561308489933127810))
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="Wybierz usługę VPN", options=options))
    embed = discord.Embed(title="🛡️ COLDSHOP × VPN", description="Wybierz dostawcę VPN z listy poniżej:", color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=v)
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_cs", description="Panel Counter-Strike 2")
@app_commands.checks.has_permissions(administrator=True)
async def scs(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    options = [
        discord.SelectOption(label="Account Prime", value="CS2 Account Prime", description="Konto z widocznym statusem Prime", emoji=discord.PartialEmoji(name="csprime", id=1561307515067834428))
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="Wybierz ofertę CS2", options=options))
    embed = discord.Embed(title="🎯 COLDSHOP × COUNTER-STRIKE 2", description="Wybierz ofertę z listy poniżej:", color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=v)
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_shop", description="Sklep")
@app_commands.checks.has_permissions(administrator=True)
async def sshop(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    options = [
        discord.SelectOption(label="Citizen", value="Citizen Custom", emoji="🌅"),
        discord.SelectOption(label="Soundpacks", value="Soundpacks", emoji="🔊")
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="Wybierz dodatek", options=options))
    embed = discord.Embed(title="🛒 COLDSHOP × ADDONS", description="Wybierz dodatek z listy poniżej:", color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=v)
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="feedback", description="Opinia")
@app_commands.checks.has_permissions(administrator=True)
async def fb(inter: discord.Interaction):
    await inter.response.send_message("⭐ Dziękujemy za zakupy w COLDSHOP!", ephemeral=True)

@bot.tree.command(name="drop", description="Drop")
async def dp(inter: discord.Interaction):
    if inter.channel_id != DROP_CH:
        await inter.response.send_message("❌ Zły kanał!", ephemeral=True)
        return
    if random.randint(1, 100) <= 5:
        await inter.response.send_message(f"🎉 {inter.user.mention} wygrał 20% zniżki w COLDSHOP!")
    else:
        await inter.response.send_message(f"❄️ Niestety {inter.user.mention}, spróbuj ponownie.")

bot.run(TOKEN)