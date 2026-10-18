import os
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

DROP_CH = 1561325772587925514
WELCOME_CH = 1557150071177347152   
VERIFY_ROLE_ID = 1456459830494630102

CAT_OWNER = 1561333304131715112
CAT_SUPPORT = 1539002224007712911

BANNER = "http://googleusercontent.com/generated_animated_image/15959043500870823950"
CHEAT_BANNER = "https://cdn.discordapp.com/attachments/1556342431903911966/1561373946010669137/a444a5e8-9b52-4784-a325-e81795221c2d.png"
SPOOFER_BANNER = "https://cdn.discordapp.com/attachments/1541276042788864080/1561390239581339658/Szpiegowski_emblemat_SPOOFER.png"

E_IPVANISH = "<:ipvanish:1561340558314709082>"
E_FIVEM = "<:fivem:1561340614828621906>"
E_CS2 = "<:cs2:1561340401523363892>"
E_DISCORD = "<:discord:1551370496199761942>"
E_STEAM = "<:steam:1561340474349068338>"
E_NEXHUB = "<:nexhub:1561341038441013368>"

E_ECHO = "<:echofun:1561389082775388365>"
E_AMBANI = "<:ambani:1561389373378011207>"
E_WORM = "<:worm:1561389638088790108>"

PE_ECHO = discord.PartialEmoji(name="echofun", id=1561389082775388365)
PE_AMBANI = discord.PartialEmoji(name="ambani", id=1561389373378011207)
PE_WORM = discord.PartialEmoji(name="worm", id=1561389638088790108)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class VeloxShopBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        try:
            await self.tree.sync()
            print("Komendy zsynchronizowane globalnie!")
        except Exception as e:
            print(f"Blad synchronizacji komend: {e}")

bot = VeloxShopBot()

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user} (ID: {bot.user.id})")
    print("Bot jest gotowy do pracy.")

@bot.event
async def on_member_join(member: discord.Member):
    ch = bot.get_channel(WELCOME_CH)
    if not ch:
        return
    
    member_count = member.guild.member_count
    created_at = member.created_at.strftime("%d.%m.%Y %H:%M:%S")
    joined_at = member.joined_at.strftime("%d.%m.%Y %H:%M:%S") if member.joined_at else "Brak"

    desc = f"Hi {member.mention}\nWelcome to Velox Shop!\nYou are our {member_count} member!\n\nDiscord account created: `{created_at}`\nUsername: {member.name}\nJoined at: `{joined_at}`"

    embed = discord.Embed(title="New member!", description=desc, color=discord.Color.dark_embed())
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    embed.set_image(url=BANNER)

    await ch.send(embed=embed)

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Zamknij", style=discord.ButtonStyle.danger, custom_id="close_t")
    async def close(self, inter: discord.Interaction, btn: discord.ui.Button):
        await inter.response.send_message("Usuwanie ticketa za 3 sekundy...", ephemeral=True)
        await asyncio.sleep(3)
        await inter.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, inter: discord.Interaction, ticket_type: str):
        await inter.response.defer(ephemeral=True)
        guild = inter.guild
        user = inter.user

        roles_to_ping = []
        category_id = CAT_SUPPORT
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        if ticket_type == "Owner":
            category_id = CAT_OWNER
            role_ids = [1456459709405204542, 1531428039676792903]
        else:
            role_ids = [1555007565405094030, 1523678008869650575, 1456459709405204542]

        for r_id in role_ids:
            role = guild.get_role(r_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                roles_to_ping.append(role.mention)

        category = guild.get_channel(category_id) if category_id else None
        ch = await guild.create_text_channel(name=f"ticket-{ticket_type.lower()}-{user.name.lower()}", category=category, overwrites=overwrites)

        embed = discord.Embed(title=f"Ticket: {ticket_type.upper()}", description=f"Witaj {user.mention}!\nAdministracja odpowie wkrótce.", color=discord.Color.blue())
        await ch.send(content=f"{user.mention} " + " ".join(roles_to_ping), embed=embed, view=CloseView())
        await inter.followup.send(f"Stworzono ticket: {ch.mention}", ephemeral=True)

    @discord.ui.button(label="Shop", style=discord.ButtonStyle.success, custom_id="t_shop")
    async def shop_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Shop")

    @discord.ui.button(label="Owner", style=discord.ButtonStyle.secondary, custom_id="t_owner")
    async def owner_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Owner")

    @discord.ui.button(label="Support", style=discord.ButtonStyle.primary, custom_id="t_support")
    async def support_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Support")

class PurchaseSelect(discord.ui.Select):
    def __init__(self, options: list):
        super().__init__(placeholder="Zakup Produkt", min_values=1, max_values=1, options=options)

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=True)
        category = inter.guild.get_channel(CAT_SUPPORT)
        ch = await inter.guild.create_text_channel(name=f"ticket-{inter.user.name.lower()}", category=category, overwrites={
            inter.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            inter.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild_me := inter.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        })
        embed = discord.Embed(title="Ticket: SHOP", description=f"Witaj {inter.user.mention}! Wybrałeś: **{self.values[0]}**", color=discord.Color.blue())
        await ch.send(content=f"{inter.user.mention}", embed=embed, view=CloseView())
        await inter.followup.send(f"Stworzono ticket: {ch.mention}", ephemeral=True)

class ShopSelect(discord.ui.Select):
    def __init__(self, options: list):
        super().__init__(placeholder="Kliknij aby wybrac", min_values=1, max_values=1, options=options)

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=True)
        product_name = self.values[0]
        embed = discord.Embed(title=f"Produkt: {product_name}", description="Wybierz opcję poniżej:", color=discord.Color.blue())
        embed.set_image(url=BANNER)
        p_options = [discord.SelectOption(label=f"Kup {product_name}", value=product_name)]
        v = discord.ui.View(timeout=None)
        v.add_item(PurchaseSelect(p_options))
        await inter.followup.send(embed=embed, view=v)

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.success, custom_id="verify_btn")
    async def verify(self, inter: discord.Interaction, btn: discord.ui.Button):
        if VERIFY_ROLE_ID != 0:
            role = inter.guild.get_role(VERIFY_ROLE_ID)
            if role:
                try:
                    await inter.user.add_roles(role)
                except Exception:
                    pass
        await inter.response.send_message("Zweryfikowano pomyślnie!", ephemeral=True)

@bot.tree.command(name="setup_tickets", description="Panel ticketow")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tickets(inter: discord.Interaction):
    embed = discord.Embed(title="Tickets", description="Kliknij przycisk poniżej, aby otworzyć ticket.", color=discord.Color.dark_embed())
    await inter.response.send_message(embed=embed, view=TicketView())

@bot.tree.command(name="setup_verify", description="Panel weryfikacji")
@app_commands.checks.has_permissions(administrator=True)
async def setup_verify(inter: discord.Interaction):
    embed = discord.Embed(title="Verification", description="Zweryfikuj się poniżej.", color=discord.Color.dark_embed())
    await inter.response.send_message(embed=embed, view=VerifyView())

bot.run(TOKEN)