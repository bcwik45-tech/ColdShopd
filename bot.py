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
LEGIT_BANNER = "https://cdn.discordapp.com/attachments/1556342431903911966/1561423524642562148/3c6b5668-0247-430b-bf68-7c9b66d0d59d.png"
BUNDLE_BANNER = "https://cdn.discordapp.com/attachments/1556342431903911966/1561424557225812079/7ac5534e-a054-4862-96f3-e0c62be3e27d.png"
CS_BANNER = "https://cdn.discordapp.com/attachments/1556342431903911966/1561433087106089070/70185ca5-b4d2-4a3f-8f6a-c9faa3ae48a9.png"
VERIFY_BANNER = "https://cdn.discordapp.com/attachments/1556342431903911966/1561423524642562148/3c6b5668-0247-430b-bf68-7c9b66d0d59d.png"

PE_REDENGINE = discord.PartialEmoji(name="redengine", id=1561388842852814998)
PE_KEYSER = discord.PartialEmoji(name="keyser", id=1561427299461758997)
PE_ECHO = discord.PartialEmoji(name="echofun", id=1561389082775388365)
PE_WORM = discord.PartialEmoji(name="worm", id=1561389638088790108)
PE_MEMESENSE = discord.PartialEmoji(name="memesense", id=1561433435057164490)

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

@bot.event
async def on_member_join(member: discord.Member):
    ch = bot.get_channel(WELCOME_CH)
    if not ch:
        return
    
    member_count = member.guild.member_count
    created_at = member.created_at.strftime("%d.%m.%Y %H:%M:%S")
    joined_at = member.joined_at.strftime("%d.%m.%Y %H:%M:%S") if member.joined_at else "Brak"

    desc = (
        f"Hi {member.mention}\nWelcome to Velox Shop!\n"
        f"You are our {member_count} member!\n\n"
        f"Discord account created: `{created_at}`\n"
        f"Username: {member.name}\nJoined at: `{joined_at}`"
    )

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
        ch = await guild.create_text_channel(
            name=f"ticket-{ticket_type.lower()}-{user.name.lower()}", 
            category=category, 
            overwrites=overwrites
        )

        embed = discord.Embed(
            title=f"Ticket: {ticket_type.upper()}", 
            description=f"Witaj {user.mention}!\nAdministracja odpowie wkrótce.", 
            color=discord.Color.blue()
        )
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
        ch = await inter.guild.create_text_channel(
            name=f"ticket-{inter.user.name.lower()}", 
            category=category, 
            overwrites={
                inter.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                inter.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                inter.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )
        embed = discord.Embed(
            title="Ticket: SHOP", 
            description=f"Witaj {inter.user.mention}! Wybrałeś: **{self.values[0]}**", 
            color=discord.Color.blue()
        )
        await ch.send(content=f"{inter.user.mention}", embed=embed, view=CloseView())
        await inter.followup.send(f"Stworzono ticket: {ch.mention}", ephemeral=True)

class ShopSelect(discord.ui.Select):
    def __init__(self, options: list):
        super().__init__(placeholder="Kliknij aby wybrac", min_values=1, max_values=1, options=options)

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=True)
        product_name = self.values[0]

        if product_name == "Red Engine":
            desc = (
                "» **Ceny:**\n"
                "> 7 Days - €8 / 34zł\n"
                "> 1 Month - €15 / 64zł\n"
                "> Lifetime - €40 / 170zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Jest to Temp Sp00er\n"
                "> ✅ » Unban na wszystkie Serwery\n"
                "> ✅ » Tx/EasyAdmin Unban\n"
                "> ✅ » Sprawdzony oraz Działający"
            )
            embed = discord.Embed(title="REDENGINE", description=desc, color=discord.Color.blue())
            embed.set_image(url=SPOOFER_BANNER)
            p_options = [
                discord.SelectOption(label="Red Engine - €8 / 34 zł", value="Red Engine - 7 Days", emoji=PE_REDENGINE),
                discord.SelectOption(label="Red Engine - €15 / 64 zł", value="Red Engine - 1 Month", emoji=PE_REDENGINE),
                discord.SelectOption(label="Red Engine - €40 / 170 zł", value="Red Engine - Lifetime", emoji=PE_REDENGINE)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.followup.send(embed=embed, view=v)

        elif product_name == "Keyser":
            desc = (
                "» **Ceny:**\n"
                "> 1 Day - €5 / 20zł\n"
                "> 7 Days - €10 / 40zł\n"
                "> 1 Month - €14 / 59zł\n"
                "> Lifetime - €35 / 148zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Wbudowany Sp00er\n"
                "> ✅ » Opcje pod Trolling\n"
                "> ✅ » Free Cam z Opcjami\n"
                "> ✅ » Kill Everyone\n"
                "> ✅ » Kill Player\n"
                "> ✅ » Event Executor & Logger"
            )
            embed = discord.Embed(title="KEYSER", description=desc, color=discord.Color.blue())
            embed.set_image(url=CHEAT_BANNER)
            p_options = [
                discord.SelectOption(label="Keyser - €5 / 20 zł", value="Keyser - 1 Day", emoji=PE_KEYSER),
                discord.SelectOption(label="Keyser - €10 / 40 zł", value="Keyser - 7 Days", emoji=PE_KEYSER),
                discord.SelectOption(label="Keyser - €14 / 59 zł", value="Keyser - 1 Month", emoji=PE_KEYSER),
                discord.SelectOption(label="Keyser - €35 / 148 zł", value="Keyser - Lifetime", emoji=PE_KEYSER)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.followup.send(embed=embed, view=v)

        elif product_name == "Echo.fun":
            desc = (
                "» **Ceny:**\n"
                "> 7 Days - €4.3 / 18.5zł\n"
                "> 1 Month - €8 / 35zł\n"
                "> Lifetime - €17 / 73zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » 100% Niewykrywalne Hitboxy (Wszystkie serwery)\n"
                "> ✅ » Niewykrywalny Silent Aim\n"
                "> ✅ » Idealne pod Shootgg & Clowns\n"
                "> ✅ » Idealne ESPY\n"
                "> ✅ » Lua Executor\n"
                "> ✅ » Prosty w konfiguracji"
            )
            embed = discord.Embed(title="ECHOFUN", description=desc, color=discord.Color.blue())
            embed.set_image(url=CHEAT_BANNER)
            p_options = [
                discord.SelectOption(label="Echo - 7 Days", value="Echo Weekly", emoji=PE_ECHO),
                discord.SelectOption(label="Echo - 1 Month", value="Echo Monthly", emoji=PE_ECHO),
                discord.SelectOption(label="Echo - Lifetime", value="Echo Lifetime", emoji=PE_ECHO)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.followup.send(embed=embed, view=v)

        elif product_name == "Worm":
            desc = (
                "» **Ceny:**\n"
                "> 7 Days - €7 / 35zł\n"
                "> 1 Month - €13 / 65zł\n"
                "> 3 Months - €32 / 145zł\n"
                "> Lifetime - €45 / 200zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Wbudowany Sp00er\n"
                "> ✅ » Idealny pod Clowns.cool\n"
                "> ✅ » Niewykrywalny Silent Aim\n"
                "> ✅ » Lua Executor\n"
                "> ✅ » Prosty do konfiguracji\n"
                "> ✅ » Typowo pod PVP"
            )
            embed = discord.Embed(title="WORM", description=desc, color=discord.Color.blue())
            embed.set_image(url=CHEAT_BANNER)
            p_options = [
                discord.SelectOption(label="Worm - 7 Days", value="Worm 7 Days", emoji=PE_WORM),
                discord.SelectOption(label="Worm - 1 Month", value="Worm 1 Month", emoji=PE_WORM),
                discord.SelectOption(label="Worm - 3 Months", value="Worm 3 Months", emoji=PE_WORM),
                discord.SelectOption(label="Worm - Lifetime", value="Worm Lifetime", emoji=PE_WORM)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))