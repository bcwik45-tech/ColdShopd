import os
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

DROP_CH = 1557163203740438628       
WELCOME_CH = 1557150071177347152   
VERIFY_ROLE_ID = 0                 
BANNER = "http://googleusercontent.com/generated_animated_image/15959043500870823950"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class ColdShopBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Synchronizacja globalna (bezpieczna, bez błędów 403 na gildię)
        try:
            await self.tree.sync()
            print("✅ [COLDSHOP] Komendy zsynchronizowane globalnie!")
        except Exception as e:
            print(f"⚠️ Błąd synchronizacji komend: {e}")

bot = ColdShopBot()

# --- AUTOMATYCZNE POWITANIA ---
@bot.event
async def on_member_join(member: discord.Member):
    ch = bot.get_channel(WELCOME_CH)
    if not ch:
        return
    
    member_count = member.guild.member_count
    created_at = member.created_at.strftime("%d.%m.%Y %H:%M:%S")
    joined_at = member.joined_at.strftime("%d.%m.%Y %H:%M:%S") if member.joined_at else "Brak"

    desc = (
        f"🎉 Hi {member.mention}\n"
        "Welcome to the best cfg in Poland!\n"
        "Go check out our stuff!\n\n"
        f"**You're our {member_count} member!**\n\n"
        "**Member Info:**\n"
        f"🪪 **Discord account created:**\n`{created_at}`\n"
        f"👤 **Username:** {member.name}\n"
        f"📅 **Joined at:** `{joined_at}`"
    )

    embed = discord.Embed(title="New member!", description=desc, color=discord.Color.dark_embed())
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    embed.set_image(url=BANNER)

    await ch.send(embed=embed)

# --- WIDOKI I TICKET SYSTEM ---
class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Zamknij", style=discord.ButtonStyle.danger, custom_id="close_t")
    async def close(self, inter: discord.Interaction, btn: discord.ui.Button):
        await inter.response.send_message("Usuwanie ticketa za 3 sekundy...", ephemeral=True)
        await asyncio.sleep(3)
        await inter.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, inter: discord.Interaction, ticket_type: str):
        await inter.response.defer(ephemeral=True)
        ch = await inter.guild.create_text_channel(
            name=f"ticket-{ticket_type.lower()}-{inter.user.name.lower()}",
            overwrites={
                inter.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                inter.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                inter.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )
        embed = discord.Embed(
            title=f"🎟️ Ticket: {ticket_type}",
            description=f"Witaj {inter.user.mention}!\nOtworzyłeś ticket typu: **{ticket_type}**.",
            color=discord.Color.blue()
        )
        await ch.send(content=f"{inter.user.mention}", embed=embed, view=CloseView())
        await inter.followup.send(f"✅ Stworzono ticket: {ch.mention}", ephemeral=True)

    @discord.ui.button(label="Shop", emoji="🛒", style=discord.ButtonStyle.success, custom_id="t_shop")
    async def shop_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Shop")

    @discord.ui.button(label="Owner", emoji="👑", style=discord.ButtonStyle.secondary, custom_id="t_owner")
    async def owner_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Owner")

    @discord.ui.button(label="Support", emoji="❓", style=discord.ButtonStyle.primary, custom_id="t_support")
    async def support_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Support")

    @discord.ui.button(label="Recruitment", emoji="📄", style=discord.ButtonStyle.danger, custom_id="t_recruitment")
    async def recruit_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Recruitment")

    @discord.ui.button(label="Partnership", emoji="🤝", style=discord.ButtonStyle.secondary, custom_id="t_partnership")
    async def partner_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Partnership")

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", emoji="✅", style=discord.ButtonStyle.success, custom_id="verify_btn")
    async def verify(self, inter: discord.Interaction, btn: discord.ui.Button):
        if VERIFY_ROLE_ID != 0:
            role = inter.guild.get_role(VERIFY_ROLE_ID)
            if role:
                try:
                    await inter.user.add_roles(role)
                except Exception:
                    pass
        await inter.response.send_message("✅ Pomyślnie zweryfikowano konto!", ephemeral=True)

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
            title=f"💎 COLDSHOP Ticket: {product_name}",
            description=f"Witaj {inter.user.mention}!\nOtworzyłeś ticket zakupowy dla: **{product_name}**.",
            color=discord.Color.blue()
        )
        await ch.send(content=f"{inter.user.mention}", embed=embed, view=CloseView())
        await inter.followup.send(f"✅ Stworzono ticket: {ch.mention}", ephemeral=True)

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

# --- KOMENDY SETUPU I MODERACJI ---

@bot.tree.command(name="setup_tickets", description="Panel systemowy ticketów")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tickets(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    desc = (
        "Want to place an order, need to contact the owner or staff for help?\n"
        "Click the appropriate button below to open a private channel with the administration.\n\n"
        "Please don't open the tickets without a proper reason."
    )
    embed = discord.Embed(title="🎟️ Tickets", description=desc, color=discord.Color.dark_embed())
    await inter.channel.send(embed=embed, view=TicketView())
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="bandc", description="Banowanie użytkownika z estetycznym panelem")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(user="Użytkownik do zbanowania", reason="Powód bana")
async def bandc(inter: discord.Interaction, user: discord.Member, reason: str = "Brak powodu"):
    await inter.guild.ban(user, reason=reason)
    desc = (
        f"👤 **User**\n`{user}` (ID: `{user.id}`)\n\n"
        f"🛡️ **Administrator**\n{inter.user.mention}\n\n"
        f"📝 **Reason**\n`{reason}`"
    )
    embed = discord.Embed(title="🔨 User has been banned for life", description=desc, color=discord.Color.red())
    embed.set_image(url=BANNER)
    await inter.response.send_message(embed=embed)

@bot.tree.command(name="unban", description="Odbanowanie użytkownika")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(user_id="ID użytkownika do odbanowania")
async def unban(inter: discord.Interaction, user_id: str):
    user = await bot.fetch_user(int(user_id))
    await inter.guild.unban(user)
    await inter.response.send_message(f"✅ Pomyślnie odbanowano użytkownika `{user}`.", ephemeral=True)

@bot.tree.command(name="setup_verify", description="Panel weryfikacji serwera")
@app_commands.checks.has_permissions(administrator=True)
async def setup_verify(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    desc = (
        "Welcome to **COLDCFG**! 🧊\n\n"
        "To gain access to the rest of the server and unlock all channels, "
        "please verify your account by clicking the button below.\n\n"
        "🔒 **Security Check:** Automated protection is active.\n"
        "⚡ **Access:** Instant role assignment upon verification.\n\n"
        "Click the button below to verify yourself."
    )
    embed = discord.Embed(title="Verification", description=desc, color=discord.Color.dark_embed())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=VerifyView())
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_legitchecks", description="Panel legit check")
@app_commands.checks.has_permissions(administrator=True)
async def sl(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    embed = discord.Embed(title="⭐ COLDSHOP × LEGIT CHECK", description="Kliknij ✅ lub ❌", color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=LegitView())
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_bundle", description="Panel Bundle & Accounts")
@app_commands.checks.has_permissions(administrator=True)
async def sb(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    
    e_fivem = discord.PartialEmoji(name="fivem", id=1561307556360749086)
    e_steam = discord.PartialEmoji(name="steam", id=1561307761617281165)
    e_dc = discord.PartialEmoji(name="discord", id=1561307671397929001)
    e_cs = discord.PartialEmoji(name="csprime", id=1561307515067834428)
    e_ip = discord.PartialEmoji(name="ipvanish", id=1561307428643930152)
    e_nex = discord.PartialEmoji(name="nexhub", id=1561308489933127810)

    options = [
        discord.SelectOption(label="FiveM Ready", value="FiveM Ready", description="See the price and open a ticket FiveM Ready.", emoji=e_fivem),
        discord.SelectOption(label="Steam