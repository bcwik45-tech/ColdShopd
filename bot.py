import os
import random
import asyncio
from datetime import datetime, time, timezone
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
TICKET_BANNER = "https://cdn.discordapp.com/attachments/1541276042788864080/1561439203697631332/veloxshopbanner.jpg"

PE_REDENGINE = discord.PartialEmoji(name="redengine", id=1561388842852814998)
PE_KEYSER = discord.PartialEmoji(name="keyser", id=1561427299461758997)
PE_ECHO = discord.PartialEmoji(name="echofun", id=1561389082775388365)
PE_WORM = discord.PartialEmoji(name="worm", id=1561389638088790108)
PE_MEMESENSE = discord.PartialEmoji(name="memesense", id=1561433435057164490)

PE_DISCORD = discord.PartialEmoji(name="discord", id=1561442072001777694)
PE_CS = discord.PartialEmoji(name="cs", id=1561340401523363892)
PE_STEAM = discord.PartialEmoji(name="steam", id=1561340474349068338)
PE_IPVANISH = discord.PartialEmoji(name="ipvanish", id=1561340558314709082)
PE_FIVEM = discord.PartialEmoji(name="fivem", id=1561441938798805113)
PE_NEXHUB = discord.PartialEmoji(name="nexhub", id=1561341038441013368)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

drop_cooldowns = {}

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
    await bot.change_presence(activity=discord.CustomActivity(name="completed"))

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

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Ticket Owner", description="Open if you have a demand to the owners.", emoji="👑"),
            discord.SelectOption(label="Ticket Shop", description="Open if you want to buy something.", emoji="🛒"),
            discord.SelectOption(label="Ticket Support", description="Open if you need any help.", emoji="🎫"),
            discord.SelectOption(label="Ticket Partner", description="Open if you want to collaborate with us.", emoji="🤝")
        ]
        super().__init__(placeholder="Select category...", min_values=1, max_values=1, options=options)

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=True)
        guild = inter.guild
        user = inter.user
        ticket_type = self.values[0].replace("Ticket ", "")

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

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

class PurchaseSelect(discord.ui.Select):
    def __init__(self, options: list):
        super().__init__(placeholder="❌ × Purchase Product | Zakup Produkt", min_values=1, max_values=1, options=options)

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
        product_name = self.values[0]

        if product_name == "Red Engine":
            desc = (
                "» **Ceny:**\n"
                "> 7 Days - €8 / 39zł\n"
                "> 1 Month - €15 / 69zł\n"
                "> Lifetime - €40 / 175zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Jest to Temp Sp00er\n"
                "> ✅ » Unban na wszystkie Serwery\n"
                "> ✅ » Tx/EasyAdmin Unban\n"
                "> ✅ » Sprawdzony oraz Działający"
            )
            embed = discord.Embed(title="REDENGINE", description=desc, color=discord.Color.blue())
            embed.set_image(url=SPOOFER_BANNER)
            p_options = [
                discord.SelectOption(label="Red Engine - €8 / 39 zł", value="Red Engine - 7 Days", emoji=PE_REDENGINE),
                discord.SelectOption(label="Red Engine - €15 / 69 zł", value="Red Engine - 1 Month", emoji=PE_REDENGINE),
                discord.SelectOption(label="Red Engine - €40 / 175 zł", value="Red Engine - Lifetime", emoji=PE_REDENGINE)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "Keyser":
            desc = (
                "» **Ceny:**\n"
                "> 1 Day - €5 / 25zł\n"
                "> 7 Days - €10 / 45zł\n"
                "> 1 Month - €14 / 64zł\n"
                "> Lifetime - €35 / 153zł\n\n"
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
                discord.SelectOption(label="Keyser - €5 / 25 zł", value="Keyser - 1 Day", emoji=PE_KEYSER),
                discord.SelectOption(label="Keyser - €10 / 45 zł", value="Keyser - 7 Days", emoji=PE_KEYSER),
                discord.SelectOption(label="Keyser - €14 / 64 zł", value="Keyser - 1 Month", emoji=PE_KEYSER),
                discord.SelectOption(label="Keyser - €35 / 153 zł", value="Keyser - Lifetime", emoji=PE_KEYSER)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "Echo.fun":
            desc = (
                "» **Ceny:**\n"
                "> 7 Days - €4.3 / 23.5zł\n"
                "> 1 Month - €8 / 40zł\n"
                "> Lifetime - €17 / 78zł\n\n"
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
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "Worm":
            desc = (
                "» **Ceny:**\n"
                "> 7 Days - €7 / 40zł\n"
                "> 1 Month - €13 / 70zł\n"
                "> 3 Months - €32 / 195zł\n"
                "> Lifetime - €45 / 250zł\n\n"
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
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "Memesense":
            desc = (
                "» **Ceny:**\n"
                "> 14 Days - €4 / 23zł\n"
                "> Monthly - €6 / 31zł\n"
                "> 3 Months - €14.4 / 67zł\n"
                "> 6 Months - €24 / 108zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Jest niewykrywalny\n"
                "> ✅ » Aimbot & Silent\n"
                "> ✅ » Ładne Espy\n"
                "> ✅ » Typowo pod Legit/semi rage\n"
                "> ✅ » Gotowy do użycia\n"
                "> ✅ » Prosty do konfiguracji"
            )
            embed = discord.Embed(title="MEMESENSE", description=desc, color=discord.Color.blue())
            embed.set_image(url=CS_BANNER)
            p_options = [
                discord.SelectOption(label="Memesense - €4 / 23zł", value="Memesense 14 Days", emoji=PE_MEMESENSE),
                discord.SelectOption(label="Memesense - €6 / 31zł", value="Memesense Monthly", emoji=PE_MEMESENSE),
                discord.SelectOption(label="Memesense - €14.4 / 67zł", value="Memesense 3 Months", emoji=PE_MEMESENSE),
                discord.SelectOption(label="Memesense - €24 / 108zł", value="Memesense 6 Months", emoji=PE_MEMESENSE)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "FiveM Ready":
            desc = (
                "» **Ceny:**\n"
                f"> {PE_FIVEM} x1 - €0.12 / 5.50zł\n"
                f"> {PE_FIVEM} x5 +1 Gratis - €0.59 / 7.50zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Full Acces\n"
                "> ✅ » Gotowy do użycia\n"
                "> ✅ » Nie ma banów\n"
                "> ✅ » 100% Fresh"
            )
            embed = discord.Embed(title=f"FIVEM READY {PE_FIVEM}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [
                discord.SelectOption(label="FiveM Ready x1 - €0.12 / 5.50 zł", value="FiveM Ready x1", emoji=PE_FIVEM),
                discord.SelectOption(label="FiveM Ready x5+1 - €0.59 / 7.50 zł", value="FiveM Ready x5+1", emoji=PE_FIVEM)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "Steam":
            desc = (
                "» **Ceny:**\n"
                f"> {PE_STEAM} x1 - €0.04 / 1.00zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Full Acces\n"
                "> ✅ » Gotowy do użycia\n"
                "> ✅ » Nie ma banów"
            )
            embed = discord.Embed(title=f"STE$M {PE_STEAM}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [
                discord.SelectOption(label="Steam x1 - €0.04 / 1.00 zł", value="Steam x1", emoji=PE_STEAM)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "D1scörd":
            desc = (
                "» **Ceny:**\n"
                f"> {PE_DISCORD} Acc Email + Phone Verifi3d (For Sp00fing) - €0.2 / 5.90zł\n"
                f"> {PE_DISCORD} TOken Email + Phone Verifi3d (YEAR AG3D) - €0.13 / 5.55zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Full Acces\n"
                "> ✅ » Gotowy do użycia\n"
                "> ✅ » Nie ma banów"
            )
            embed = discord.Embed(title=f"DISC$RD {PE_DISCORD}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [
                discord.SelectOption(label="Acc Verified - €0.2 / 5.90zł", value="Discord Acc", emoji=PE_DISCORD),
                discord.SelectOption(label="Token Aged - €0.13 / 5.55zł", value="Discord Token", emoji=PE_DISCORD)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "CS2 Prime Accounts":
            desc = (
                "» **Ceny:**\n"
                f"> {PE_CS} Prime Ready - €1.4 / 11.00zł\n"
                f"> {PE_CS} Premier Ready (4+ Medals) - €1.85 / 13.00zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Każde konto ma Prime\n"
                "> ✅ » Gotowe do użycia\n"
                "> ✅ » Bez Vac'a\n"
                "> ✅ » Gwarancja 3 godziny"
            )
            embed = discord.Embed(title=f"CS2 PRIME ACCOUNT {PE_CS}", description=desc, color=discord.Color.blue())
            embed.set_image(url=CS_BANNER)
            p_options = [
                discord.SelectOption(label="Prime Ready - €1.4 / 11.00 zł", value="CS2 Prime Ready", emoji=PE_CS),
                discord.SelectOption(label="Premier Ready (4+ Medals) - €1.85 / 13.00 zł", value="CS2 Premier Ready", emoji=PE_CS)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "NexHub":
            desc = (
                "» **Ceny:**\n"
                f"> {PE_NEXHUB} 1 Day - €1.7 / 12.50zł\n"
                f"> {PE_NEXHUB} 7 Days - €4.3 / 23.50zł\n"
                f"> {PE_NEXHUB} Month - €8.6 / 42.00zł\n"
                f"> {PE_NEXHUB} 3 Months - €17.3 / 79.50zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Działa na ShootGG & Clowns.Cool\n"
                "> ✅ » 100+ Kraji\n"
                "> ✅ » Gotowy do użycia\n"
                "> ✅ » Optymalny i szybki"
            )
            embed = discord.Embed(title=f"NEXHUB VPN {PE_NEXHUB}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [
                discord.SelectOption(label="Nexhub - €1.7 / 12.50 zł", value="Nexhub 1 Day", emoji=PE_NEXHUB),
                discord.SelectOption(label="Nexhub - €4.3 / 23.50 zł", value="Nexhub 7 Days", emoji=PE_NEXHUB),
                discord.SelectOption(label="Nexhub - €8.6 / 42.00 zł", value="Nexhub Month", emoji=PE_NEXHUB),
                discord.SelectOption(label="Nexhub - €17.3 / 79.50 zł", value="Nexhub 3 Months", emoji=PE_NEXHUB)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "IP Vanish":
            desc = (
                "» **Ceny:**\n"
                f"> {PE_IPVANISH} Year - €1 / 9.50zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Full Acces\n"
                "> ✅ » Gotowy do użycia"
            )
            embed = discord.Embed(title=f"IPVAN$SH {PE_IPVANISH}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [
                discord.SelectOption(label="IP Vanish - €1 / 9.50 zł", value="IP Vanish Year", emoji=PE_IPVANISH)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "FiveM Bundle":
            desc = (
                "» **Ceny:**\n"
                "> ⁠Zwykłe Bundle × €0.47 / 1.50zł\n"
                "> ⁠Aged Bundle × €0.35 / 2.00zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Pakiet Rockst$r + Dsc + St$am\n"
                "> ✅ » Full Acces\n"
                "> ✅ » Gotowy do użycia\n"
                "> ✅ » Działający"
            )
            embed = discord.Embed(title="FIVEEM BUNDLE", description=desc, color=discord.Color.blue())
            embed.set_image(url=BUNDLE_BANNER)
            p_options = [
                discord.SelectOption(label="Zwykle - €0.47 / 3.99 zł", value="FiveM Bundle Zwykle", emoji=PE_FIVEM),
                discord.SelectOption(label="Aged - €0.35 / 9.99 zł", value="FiveM Bundle Aged", emoji=PE_FIVEM)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        elif product_name == "D1scörd Bundle":
            desc = (
                "» **Ceny:**\n"
                f"> {PE_DISCORD} x3 × €0.70 / 3.99zł\n"
                f"> {PE_DISCORD} x10 × €1.9 / 9.99zł\n\n"
                "» **Krótki Opis:**\n"
                "> ✅ » Full Acces\n"
                "> ✅ » Gotowy do użycia\n"
                "> ✅ » Działające"
            )
            embed = discord.Embed(title=f"DISCORD BUNDLE {PE_DISCORD}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BUNDLE_BANNER)
            p_options = [
                discord.SelectOption(label="Discord Bundle - €0.70 / 3.99 zł", value="Discord Bundle 3 acc", emoji=PE_DISCORD),
                discord.SelectOption(label="Discord Bundle - €1.87 / 9.99 zł", value="Discord Bundle 10 acc", emoji=PE_DISCORD)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

        else:
            embed = discord.Embed(title=f"Produkt: {product_name}", description="Wybierz opcję poniżej:", color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [discord.SelectOption(label=f"Kup {product_name}", value=product_name)]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(p_options))
            await inter.response.send_message(embed=embed, view=v, ephemeral=True)

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.success, emoji="✅", custom_id="verify_btn")
    async def verify(self, inter: discord.Interaction, btn: discord.ui.Button):
        if VERIFY_ROLE_ID != 0:
            role = inter.guild.get_role(VERIFY_ROLE_ID)
            if role:
                try:
                    await inter.user.add_roles(role)
                except Exception:
                    pass
        await inter.response.send_message("Zweryfikowano pomyślnie!", ephemeral=True)

class LegitView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.y, self.n = 0, 0

    @discord.ui.button(label="0", style=discord.ButtonStyle.secondary, custom_id="leg_y")
    async def yes(self, inter: discord.Interaction, btn: discord.ui.Button):
        self.y += 1
        btn.label = str(self.y)
        await inter.response.edit_message(view=self)
        await inter.followup.send("Dzieki za glos!", ephemeral=True)

    @discord.ui.button(label="0", style=discord.ButtonStyle.secondary, custom_id="leg_n")
    async def no(self, inter: discord.Interaction, btn: discord.ui.Button):
        self.n += 1
        btn.label = str(self.n)
        await inter.response.edit_message(view=self)
        await inter.followup.send("Dzieki za glos!", ephemeral=True)

@bot.tree.command(name="setup_tickets", description="Panel ticketow")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tickets(inter: discord.Interaction):
    desc = (
        "Tickets\n\n"
        "**Ticket Owner**\n*Open if you have a demand to the owners.*\n\n"
        "**Ticket Shop**\n*Open if you want to buy something.*\n\n"
        "**Ticket Support**\n*Open if you need any help.*\n\n"
        "**Ticket Partner**\n*Open if you want to collaborate with us.*\n\n"
        "For any issues, text us in #chat."
    )
    embed = discord.Embed(title="", description=desc, color=discord.Color.dark_embed())
    embed.set_image(url=TICKET_BANNER)
    await inter.response.send_message(embed=embed, view=TicketView())

@bot.tree.command(name="setup_verify", description="Panel weryfikacji")
@app_commands.checks.has_permissions(administrator=True)
async def setup_verify(inter: discord.Interaction):
    desc = (
        "Welcome to **Velox Shop**! 🧊\n\n"
        "To gain access to the rest of the server and unlock all channels, please verify your account by clicking the button below.\n\n"
        "🔒 **Security Check:** Automated protection is active.\n"
        "⚡ **Access:** Instant role assignment upon verification.\n\n"
        "Click the button below to verify yourself."
    )
    embed = discord.Embed(title="Verification", description=desc, color=discord.Color.from_rgb(46, 204, 113))
    await inter.response.send_message(embed=embed, view=VerifyView())

@bot.tree.command(name="setup_bundle", description="Panel Bundle & Accounts")
@app_commands.checks.has_permissions(administrator=True)
async def sb(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="FiveM Ready", value="FiveM Ready", emoji=PE_FIVEM),
        discord.SelectOption(label="Steam", value="Steam", emoji=PE_STEAM),
        discord.SelectOption(label="D1scörd", value="D1scörd", emoji=PE_DISCORD),
        discord.SelectOption(label="CS2 Prime Accounts", value="CS2 Prime Accounts", emoji=PE_CS),
        discord.SelectOption(label="IP Vanish", value="IP Vanish", emoji=PE_IPVANISH),
        discord.SelectOption(label="NexHub", value="NexHub", emoji=PE_NEXHUB)
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(options))
    
    desc = (
        "💎 ⁠`Velox Shop × PREMIUM`\n\n"
        "Accounts **available** from us:\n"
        f"> • {PE_FIVEM} x FiveM Ready\n"
        f"> • {PE_STEAM} x Steam\n"
        f"> • {PE_DISCORD} x D1scörd\n"
        f"> • {PE_CS} x CS2 Prime Accounts\n\n"
        "VPN's **available** from us:\n"
        f"> • {PE_IPVANISH} x IP Vanish\n"
        f"> • {PE_NEXHUB} x NexHub\n\n"
        "📢 **Select** the product you are **interested** in.\n"
        "📢 At the **bottom** of the `select menu`, select **duration** and **payment**.\n\n"
        "🌐 **Instant Buy:** [Click here to visit our website](https://google.com)"
    )
    
    embed = discord.Embed(title="", description=desc, color=discord.Color.blue())
    embed.set_image(url=BUNDLE_BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_bundle2", description="Panel Bundle 2")
@app_commands.checks.has_permissions(administrator=True)
async def sb2(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="FiveM Bundle", value="FiveM Bundle", emoji=PE_FIVEM),
        discord.SelectOption(label="D1scörd Bundle", value="D1scörd Bundle", emoji=PE_DISCORD)
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(options))
    
    desc = (
        "💎 ⁠`Velox Shop × Acounts Bundle`\n\n"
        "Bundle **available** from us:\n"
        f"> • {PE_FIVEM} x FiveM Bundle\n"
        f"> • {PE_DISCORD} x D1scörd Bundle\n\n"
        "📢 **Select** the product you are **interested** in.\n"
        "📢 At the **bottom** of the `select menu`, select **duration** and **payment**.\n\n"
        "🌐 **Instant Buy:** [Click here to visit our website](https://google.com)"
    )
    
    embed = discord.Embed(title="", description=desc, color=discord.Color.blue())
    embed.set_image(url=BUNDLE_BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_cheats", description="Panel FiveM Cheats")
@app_commands.checks.has_permissions(administrator=True)
async def scheats(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="Keyser", value="Keyser", description="Keyser Cheat", emoji=PE_KEYSER),
        discord.SelectOption(label="Echo.fun", value="Echo.fun", description="Echo.fun Cheat", emoji=PE_ECHO),
        discord.SelectOption(label="Worm", value="Worm", description="Worm Cheat", emoji=PE_WORM)
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(options))
    desc = (
        "Cheats available from us:\n"
        f"> • {PE_KEYSER} Keyser\n"
        f"> • {PE_ECHO} Echo.fun\n"
        f"> • {PE_WORM} Worm\n\n"
        "Select the cheat you are interested in."
    )
    embed = discord.Embed(title="Velox Products x FiveM Cheats", description=desc, color=discord.Color.blue())
    embed.set_image(url=CHEAT_BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_cheatscs", description="Panel CS2 Cheats")
@app_commands.checks.has_permissions(administrator=True)
async def scheatscs(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="Memesense", value="Memesense", description="Memesense Cheat", emoji=PE_MEMESENSE)
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(options))
    
    desc = (
        "💎 ⁠`Velox Shop × COUNTER STRIKE 2`\n\n"
        "Cs 2 **available** from us:\n"
        f"> • {PE_MEMESENSE} x Memesense\n\n"
        "📢 **Select** the product you are **interested** in.\n"
        "📢 At the **bottom** of the `select menu`, select **duration** and **payment**.\n\n"
        "🌐 **Instant Buy:** [Click here to visit our website](https://google.com)"
    )
    
    embed = discord.Embed(title="", description=desc, color=discord.Color.blue())
    embed.set_image(url=CS_BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_cheats1", description="Panel CS2 Cheats 1")
@app_commands.checks.has_permissions(administrator=True)
async def scheats1(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="Memesense", value="Memesense", description="Memesense Cheat", emoji=PE_MEMESENSE)
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(options))
    
    desc = (
        "💎 ⁠`Velox Shop × COUNTER STRIKE 2`\n\n"
        "Cs 2 **available** from us:\n"
        f"> • {PE_MEMESENSE} x Memesense\n\n"
        "📢 **Select** the product you are **interested** in.\n"
        "📢 At the **bottom** of the `select menu`, select **duration** and **payment**.\n\n"
        "🌐 **Instant Buy:** [Click here to visit our website](https://google.com)"
    )
    
    embed = discord.Embed(title="", description=desc, color=discord.Color.blue())
    embed.set_image(url=CS_BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_spoofer", description="Panel FiveM Spoofer")
@app_commands.checks.has_permissions(administrator=True)
async def sspoof(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="Red Engine", value="Red Engine", description="Red Engine Spoofer", emoji=PE_REDENGINE)
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(options))
    desc = (
        "Spoofers available from us:\n"
        f"> • {PE_REDENGINE} Red Engine\n\n"
        "Select the product you are interested in."
    )
    embed = discord.Embed(title="Velox Products x FiveM Spoofer", description=desc, color=discord.Color.blue())
    embed.set_image(url=SPOOFER_BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_legitchecks", description="Panel legit check")
@app_commands.checks.has_permissions(administrator=True)
async def sl(inter: discord.Interaction):
    desc = "Jeżeli uważasz, że jesteśmy legit, zaznacz reakcję pod wiadomością."
    embed = discord.Embed(title="CZY JESTESMY LEGIT?", description=desc, color=discord.Color.blue())
    embed.set_image(url=LEGIT_BANNER)
    await inter.response.send_message(embed=embed, view=LegitView())

@bot.tree.command(name="say", description="Wysyła wiadomosc")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(message="Tresc wiadomosci")
async def say(inter: discord.Interaction, message: str):
    await inter.channel.send(message)
    await inter.response.send_message("Wyslano wiadomosc!", ephemeral=True)

@bot.tree.command(name="bandc", description="Banowanie uzytkownika")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(user="Uzytkownik", reason="Powod")
async def bandc(inter: discord.Interaction, user: discord.Member, reason: str = "Brak powodu"):
    await inter.guild.ban(user, reason=reason)
    await inter.response.send_message(f"Zbanowano użytkownika {user}.", ephemeral=True)

@bot.tree.command(name="unban", description="Odbanowanie uzytkownika")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(user_id="ID uzytkownika")
async def unban(inter: discord.Interaction, user_id: str):
    user = await bot.fetch_user(int(user_id))
    await inter.guild.unban(user)
    await inter.response.send_message(f"Odbanowano użytkownika `{user}`.", ephemeral=True)

@bot.tree.command(name="feedback", description="Opinia")
@app_commands.checks.has_permissions(administrator=True)
async def fb(inter: discord.Interaction):
    await inter.response.send_message("Dziekujemy za zakupy w Velox Shop!", ephemeral=True)

@bot.tree.command(name="drop", description="Drop")
async def dp(inter: discord.Interaction):
    if inter.channel_id != DROP_CH:
        await inter.response.send_message("Zly kanal!", ephemeral=True)
        return
    
    user_id = inter.user.id
    now = datetime.now(timezone.utc)
    midnight = datetime.combine(now.date(), time(0, 0), tzinfo=timezone.utc)

    if user_id in drop_cooldowns and drop_cooldowns[user_id] > midnight:
        await inter.response.send_message("Już używałeś dropu dzisiaj! Spróbuj ponownie po północy.", ephemeral=True)
        return

    drop_cooldowns[user_id] = now

    if random.randint(1, 100) <= 5:
        desc = (
            f"> • {inter.user.mention} **Gratulacje!**, udało Ci się coś wygrać 🔊\n"
            "> • **Otrzymujesz** kod zniżkowy: **-15%**\n"
            "> • Masz **24 godziny** na jego **wykorzystanie** ⏱️"
        )
    else:
        desc = (
            f"> • {inter.user.mention} **Niestety**, tym razem się **nie udało**.\n"
            "> • **Spróbuj** ponownie za jakiś czas ⏱️\n"
            "> • Może **następnym** razem **trafisz** coś lepszego."
        )

    embed = discord.Embed(title="💎 ⁠ Velox Shop × Drop", description=desc, color=discord.Color.blue())
    embed.set_footer(text=f"Losowanie wykonane przez {inter.user.name}")
    await inter.response.send_message(embed=embed)

bot.run(TOKEN)