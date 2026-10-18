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

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🔒 Zamknij",
        style=discord.ButtonStyle.danger,
        custom_id="close_t"
    )
    async def close(self, it: discord.Interaction, btn: discord.ui.Button):
        await it.response.send_message("Usuwanie ticketa za 3s...", ephemeral=True)
        await asyncio.sleep(3)
        await it.channel.delete()

class ShopSelect(discord.ui.Select):
    def __init__(self, ph: str, opts: list):
        super().__init__(placeholder=ph, min_values=1, max_values=1, options=opts)

    async def callback(self, it: discord.Interaction):
        await it.response.defer(ephemeral=True)
        item = self.values[0]
        ch = await it.guild.create_text_channel(
            name=f"ticket-{it.user.name.lower()}",
            overwrites={
                it.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                it.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                it.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )
        emb = discord.Embed(
            title=f"COLDSHOP Ticket: {item}",
            description=f"Witaj {it.user.mention}!\nTicket dla: **{item}**.",
            color=discord.Color.blue()
        )
        await ch.send(content=f"{it.user.mention}", embed=emb, view=CloseView())
        await it.followup.send(f"✅ Stworzono ticket: {ch.mention}", ephemeral=True)

class LegitView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.y, self.n = 0, 0

    @discord.ui.button(
        label="0",
        emoji="✅",
        style=discord.ButtonStyle.success,
        custom_id="leg_y"
    )
    async def yes(self, it: discord.Interaction, btn: discord.ui.Button):
        self.y += 1
        btn.label = str(self.y)
        await it.response.edit_message(view=self)
        await it.followup.send("Dzięki za głos!", ephemeral=True)

    @discord.ui.button(
        label="0",
        emoji="❌",
        style=discord.ButtonStyle.danger,
        custom_id="leg_n"
    )
    async def no(self, it: discord.Interaction, btn: discord.ui.Button):
        self.n += 1
        btn.label = str(self.n)
        await it.response.edit_message(view=self)
        await it.followup.send("Dzięki za głos!", ephemeral=True)

@bot.tree.command(name="setup_legitchecks", description="Panel legit check")
@app_commands.checks.has_permissions(administrator=True)
async def sl(it: discord.Interaction):
    await it.response.defer(ephemeral=True)
    emb = discord.Embed(
        title="⭐ COLDSHOP × LEGIT CHECK",
        description="Kliknij ✅ lub ❌",
        color=discord.Color.blue()
    )
    emb.set_image(url=BANNER)
    await it.channel.send(embed=emb, view=LegitView())
    await it.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_bundle", description="Panel Bundle")
@app_commands.checks.has_permissions(administrator=True)
async def sb(it: discord.Interaction):
    await it.response.defer(ephemeral=True)
    e_steam = discord.PartialEmoji(name="steam", id=1561307761617281165)
    e_dc = discord.PartialEmoji(name="discord", id=1561307671397929001)
    e_rock = discord.PartialEmoji(name="rockstar", id=1561308861636542524)
    e_fivem = discord.PartialEmoji(name="fivem", id=1561307556360749086)

    opts = [
        discord.SelectOption(label="Steam Account", value="Steam Account", emoji=e_steam),
        discord.SelectOption(label="Discord Account", value="Discord Account", emoji=e_dc),
        discord.SelectOption(label="Rockstar Account", value="Rockstar Account", emoji=e_rock),
        discord.SelectOption(
            label="FiveM Bundle",
            value="FiveM Bundle",
            description="Discord + Steam + Rockstar",
            emoji=e_fivem
        )
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect("Wybierz konto / pakiet", opts))
    emb = discord.Embed(
        title="📦 COLDSHOP × BUNDLE",
        description="Wybierz konto lub pakiet z listy:",
        color=discord.Color.blue()
    )
    emb.set_image(url=BANNER)
    await it.channel.send(embed=emb, view=v)
    await it.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_vpn", description="Panel VPN")
@app_commands.checks.has_permissions(administrator=True)
async def svpn(it: discord.Interaction):
    await it.response.defer(ephemeral=True)
    e_ip = discord.PartialEmoji(name="ipvanish", id=1561307428