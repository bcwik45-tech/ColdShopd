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
async def on_member_join(member: discord.Member):
    ch = bot.get_channel(WELCOME_CH)
    if not ch:
        return
    
    member_count = member.guild.member_count
    created_at = member.created_at.strftime("%d.%m.%Y %H:%M:%S")
    joined_at = member.joined_at.strftime("%d.%m.%Y %H:%M:%S") if member.joined_at else "Brak"

    desc = (
        f"Hi {member.mention}\n"
        "Welcome to Velox Shop!\n"
        "Go check out our stuff!\n\n"
        f"You are our {member_count} member!\n\n"
        "Member Info:\n"
        f"Discord account created:\n`{created_at}`\n"
        f"Username: {member.name}\n"
        f"Joined at: `{joined_at}`"
    )

    embed = discord.Embed(title="New member!", description=desc, color=discord.Color.dark_embed())
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    embed.set_image(url=BANNER)

    await ch.send(embed=embed)

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Zamknij", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_t")
    async def close(self, inter: discord.Interaction, btn: discord.ui.Button):
        await inter.response.send_message("Usuwanie ticketa za 3 sekundy...", ephemeral=True)
        await asyncio.sleep(3)
        await inter.channel.delete()

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def create_ticket(self, inter: discord.Interaction, ticket_type: str, emoji: str):
        await inter.response.defer(ephemeral=True)
        guild = inter.guild
        user = inter.user

        roles_to_ping = []
        category_id = None
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        if ticket_type == "Owner":
            category_id = CAT_OWNER
            role_ids = [1456459709405204542, 1531428039676792903]
            for r_id in role_ids:
                role = guild.get_role(r_id)
                if role:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    roles_to_ping.append(role.mention)
        
        elif ticket_type == "Support":
            category_id = CAT_SUPPORT
            role_ids = [1555007565405094030, 1523678008869650575, 1555614403540295750, 1531428039676792903, 1456459709405204542]
            for r_id in role_ids:
                role = guild.get_role(r_id)
                if role:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    roles_to_ping.append(role.mention)

        elif ticket_type == "Partnership":
            category_id = CAT_OWNER
            role_ids = [1456459709405204542, 1531428039676792903]
            for r_id in role_ids:
                role = guild.get_role(r_id)
                if role:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    roles_to_ping.append(role.mention)

        elif ticket_type == "Shop":
            category_id = CAT_SUPPORT
            role_ids = [1456459709405204542]
            for r_id in role_ids:
                role = guild.get_role(r_id)
                if role:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    roles_to_ping.append(role.mention)

        elif ticket_type == "Recruitment":
            category_id = CAT_SUPPORT
            role_ids = [1456459709405204542, 1531428039676792903]
            for r_id in role_ids:
                role = guild.get_role(r_id)
                if role:
                    overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
                    roles_to_ping.append(role.mention)

        category = guild.get_channel(category_id) if category_id else None
        ch_name = f"{emoji}-ticket-{ticket_type.lower()}-{user.name.lower()}"

        ch = await guild.create_text_channel(
            name=ch_name,
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title=f"Ticket: {ticket_type.upper()}",
            description=(
                f"Witaj {user.mention}!\n"
                "Administracja wkrotce odpowie na Twoje zgloszenie.\n\n"
                "Aby zamknac ten kanal, kliknij przycisk ponizej."
            ),
            color=discord.Color.blue()
        )
        
        ping_content = f"{user.mention} " + " ".join(roles_to_ping)
        await ch.send(content=ping_content, embed=embed, view=CloseView())
        await inter.followup.send(f"Stworzono ticket: {ch.mention}", ephemeral=True)

    @discord.ui.button(label="Shop", emoji="🛒", style=discord.ButtonStyle.success, custom_id="t_shop")
    async def shop_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Shop", "🛒")

    @discord.ui.button(label="Owner", emoji="👑", style=discord.ButtonStyle.secondary, custom_id="t_owner")
    async def owner_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Owner", "👑")

    @discord.ui.button(label="Support", emoji="❓", style=discord.ButtonStyle.primary, custom_id="t_support")
    async def support_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Support", "❓")

    @discord.ui.button(label="Recruitment", emoji="📄", style=discord.ButtonStyle.danger, custom_id="t_recruitment")
    async def recruit_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Recruitment", "📄")

    @discord.ui.button(label="Partnership", emoji="🤝", style=discord.ButtonStyle.secondary, custom_id="t_partnership")
    async def partner_btn(self, inter: discord.Interaction, btn: discord.ui.Button):
        await self.create_ticket(inter, "Partnership", "🤝")

class PurchaseSelect(discord.ui.Select):
    def __init__(self, placeholder: str, options: list):
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=True)
        product_variant = self.values[0]
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
            description=(
                f"Witaj {inter.user.mention}!\n"
                f"Otworzyłeś ticket zakupowy dla: **{product_variant}**.\n"
                "Administracja wkrotce odpowie na Twoje zgloszenie.\n\n"
                "Aby zamknac ten kanal, kliknij przycisk ponizej."
            ),
            color=discord.Color.blue()
        )
        role_shop = inter.guild.get_role(1456459709405204542)
        ping = role_shop.mention if role_shop else ""
        await ch.send(content=f"{inter.user.mention} {ping}", embed=embed, view=CloseView())
        await inter.followup.send(f"Stworzono ticket: {ch.mention}", ephemeral=True)

class ShopSelect(discord.ui.Select):
    def __init__(self, placeholder: str, options: list):
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, inter: discord.Interaction):
        await inter.response.defer(ephemeral=True)
        product_name = self.values[0]

        if product_name in ["IP Vanish", "IP Vanish VPN"]:
            desc = f"Ceny:\n> {E_IPVANISH} **Year** - **€1 / 4.5zl**\n\nKrotki Opis:\n> Full Access\n> Gotowy do uzycia"
            embed = discord.Embed(title=f"IPVANISH {E_IPVANISH}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [discord.SelectOption(label="IP Vanish - €1 / 4.5 zl", value="IP Vanish - Year", description="Year")]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(placeholder="Zakup Produkt", options=p_options))
            await inter.followup.send(embed=embed, view=v)

        elif product_name in ["NexHub", "NexHub VPN"]:
            desc = f"Ceny:\n> {E_NEXHUB} **1 Day** - **€1.7 / 7.5zl**\n> {E_NEXHUB} **7 Days** - **€4.3 / 18.5zl**\n> {E_NEXHUB} **Month** - **€8.6 / 37zl**\n> {E_NEXHUB} **3 Months** - **€17.3 / 74.5zl**\n\nKrotki Opis:\n> Dziala na ShootGG\n> 100+ Krai\n> Gotowy do uzycia"
            embed = discord.Embed(title=f"NEXHUB VPN {E_NEXHUB}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [
                discord.SelectOption(label="Nexhub - €1.7 / 7.5 zl", value="NexHub - 1 Day", description="1 Day"),
                discord.SelectOption(label="Nexhub - €4.3 / 18.5 zl", value="NexHub - 7 Days", description="7 Days"),
                discord.SelectOption(label="Nexhub - €8.6 / 37 zl", value="NexHub - Month", description="Month"),
                discord.SelectOption(label="Nexhub - €17.3 / 74.5 zl", value="NexHub - 3 Months", description="3 Months")
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(placeholder="Zakup Produkt", options=p_options))
            await inter.followup.send(embed=embed, view=v)

        elif product_name in ["FiveM Ready", "FiveM Bundle"]:
            desc = f"Ceny:\n> {E_FIVEM} **Zwykle Bundle** - **€0.24 / 1.00zl**\n> {E_FIVEM} **Aged Bundle** - **€0.35 / 1.50zl**\n\nKrotki Opis:\n> Pakiet Rockstar + Dsc + Steam\n> Full Access\n> Gotowy do uzycia"
            embed = discord.Embed(title=f"FIVEM BUNDLE {E_FIVEM}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [
                discord.SelectOption(label="Zwykle Bundle - €0.24 / 1.00zl", value="FiveM Zwykle Bundle", description="Zwykle Bundle"),
                discord.SelectOption(label="Aged Bundle - €0.35 / 1.50zl", value="FiveM Aged Bundle", description="Aged Bundle")
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(placeholder="Zakup Produkt", options=p_options))
            await inter.followup.send(embed=embed, view=v)

        elif product_name in ["D1scörd", "D1scörd Bundle"]:
            desc = f"Ceny:\n> {E_DISCORD} **x3** - **€0.70 / 3zl**\n> {E_DISCORD} **x10** - **€1.9 / 8zl**\n\nKrotki Opis:\n> Full Access\n> Gotowy do uzycia"
            embed = discord.Embed(title=f"DISCORD BUNDLE {E_DISCORD}", description=desc, color=discord.Color.blue())
            embed.set_image(url=BANNER)
            p_options = [
                discord.SelectOption(label="Discord Bundle - €0.70 / 2.99 zl", value="Discord Bundle x3", description="3 acc Discord"),
                discord.SelectOption(label="Discord Bundle - €1.87 / 7.99 zl", value="Discord Bundle x10", description="10 acc Discord")
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(placeholder="Zakup Produkt", options=p_options))
            await inter.followup.send(embed=embed, view=v)

        elif product_name == "Echo.fun":
            desc = (
                f"Ceny:\n"
                f"> {E_ECHO} **7 Days** - **€4.3 / 23.5zl**\n"
                f"> {E_ECHO} **1 Month** - **€8 / 40zl**\n"
                f"> {E_ECHO} **Lifetime** - **€17 / 78zl**\n\n"
                f"Krotki Opis:\n"
                f"> Niewykrywalny Silent Aim\n"
                f"> Lua Executor"
            )
            embed = discord.Embed(title=f"ECHOFUN {E_ECHO}", description=desc, color=discord.Color.blue())
            embed.set_image(url=CHEAT_BANNER)
            p_options = [
                discord.SelectOption(label="Echo - €4.3 / 23.5 zl", value="Echo Weekly", description="7 Days", emoji=PE_ECHO),
                discord.SelectOption(label="Echo - €8 / 40 zl", value="Echo Monthly", description="1 Month", emoji=PE_ECHO),
                discord.SelectOption(label="Echo - €17 / 78 zl", value="Echo Lifetime", description="Lifetime", emoji=PE_ECHO)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(placeholder="Zakup Produkt", options=p_options))
            await inter.followup.send(embed=embed, view=v)

        elif product_name == "Ambani":
            desc = (
                f"Ceny:\n"
                f"> {E_AMBANI} **7 Days** - **€9.5 / 45zl**\n"
                f"> {E_AMBANI} **1 Month** - **€14 / 65zl**\n"
                f"> {E_AMBANI} **Lifetime** - **€33 / 145zl**\n\n"
                f"Krotki Opis:\n"
                f"> Dobry ESP\n"
                f"> Troll Opcje\n"
                f"> Kill Player\n"
                f"> Kill Everyone i inne\n"
                f"> Event Logger & Executor"
            )
            embed = discord.Embed(title=f"AMBANI {E_AMBANI}", description=desc, color=discord.Color.blue())
            embed.set_image(url=CHEAT_BANNER)
            p_options = [
                discord.SelectOption(label="Ambani - €9.5 / 45 zl", value="Ambani Weekly", description="Weekly", emoji=PE_AMBANI),
                discord.SelectOption(label="Ambani - €14 / 65 zl", value="Ambani Month", description="Month", emoji=PE_AMBANI),
                discord.SelectOption(label="Ambani - €33 / 145 zl", value="Ambani Lifetime", description="Lifetime", emoji=PE_AMBANI)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(placeholder="Zakup Produkt", options=p_options))
            await inter.followup.send(embed=embed, view=v)

        elif product_name == "Worm":
            desc = (
                f"Ceny:\n"
                f"> {E_WORM} **7 Days** - **€7 / 35zl**\n"
                f"> {E_WORM} **1 Month** - **€13 / 65zl**\n"
                f"> {E_WORM} **3 Months** - **€32 / 145zl**\n"
                f"> {E_WORM} **Lifetime** - **€45 / 200zl**\n\n"
                f"Krotki Opis:\n"
                f"> Wbudowany Spoofer\n"
                f"> Idealny pod PVP\n"
                f"> Niewykrywalny Silent Aim\n"
                f"> Lua Executor\n"
                f"> Prosty do konfiguracji"
            )
            embed = discord.Embed(title=f"WORM {E_WORM}", description=desc, color=discord.Color.blue())
            embed.set_image(url=CHEAT_BANNER)
            p_options = [
                discord.SelectOption(label="Worm - €7 / 35 zl", value="Worm 7 Days", description="7 Days", emoji=PE_WORM),
                discord.SelectOption(label="Worm - €13 / 65 zl", value="Worm 1 Month", description="1 Month", emoji=PE_WORM),
                discord.SelectOption(label="Worm - €32 / 145 zl", value="Worm 3 Months", description="3 Months", emoji=PE_WORM),
                discord.SelectOption(label="Worm - €45 / 200 zl", value="Worm Lifetime", description="Lifetime", emoji=PE_WORM)
            ]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(placeholder="Zakup Produkt", options=p_options))
            await inter.followup.send(embed=embed, view=v)

        else:
            p_options = [discord.SelectOption(label=product_name, value=product_name)]
            v = discord.ui.View(timeout=None)
            v.add_item(PurchaseSelect(placeholder="Zakup Produkt", options=p_options))
            await inter.followup.send(f"Wybrałeś {product_name}. Otwórz ticket ponizej:", view=v)

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
        await inter.response.send_message("Zweryfikowano konto pomyślnie!", ephemeral=True)

class LegitView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.y, self.n = 0, 0

    @discord.ui.button(label="0", emoji="✅", style=discord.ButtonStyle.secondary, custom_id="leg_y")
    async def yes(self, inter: discord.Interaction, btn: discord.ui.Button):
        self.y += 1
        btn.label = str(self.y)
        await inter.response.edit_message(view=self)
        await inter.followup.send("Dzieki za glos!", ephemeral=True)

    @discord.ui.button(label="0", emoji="🔖", style=discord.ButtonStyle.secondary, custom_id="leg_n")
    async def no(self, inter: discord.Interaction, btn: discord.ui.Button):
        self.n += 1
        btn.label = str(self.n)
        await inter.response.edit_message(view=self)
        await inter.followup.send("Dzieki za glos!", ephemeral=True)

@bot.tree.command(name="say", description="Wysyła wiadomosc")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(message="Tresc wiadomosci")
async def say(inter: discord.Interaction, message: str):
    await inter.channel.send(message)
    await inter.response.send_message("Wyslano wiadomosc!", ephemeral=True)

@bot.tree.command(name="setup_legitchecks", description="Panel legit check")
@app_commands.checks.has_permissions(administrator=True)
async def sl(inter: discord.Interaction):
    desc = (
        "CZY JESTESMY LEGIT?\n"
        "Jezeli uwazasz, ze jestesmy legit, zaznacz reakcje pod wiadomoscia."
    )
    embed = discord.Embed(title="CZY JESTESMY LEGIT?", description=desc, color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.response.send_message(embed=embed, view=LegitView())

@bot.tree.command(name="setup_tickets", description="Panel ticketow")
@app_commands.checks.has_permissions(administrator=True)
async def setup_tickets(inter: discord.Interaction):
    desc = (
        "Want to place an order, need to contact the owner or staff for help?\n"
        "Click the appropriate button below to open a private channel with the administration."
    )
    embed = discord.Embed(title="Tickets", description=desc, color=discord.Color.dark_embed())
    await inter.response.send_message(embed=embed, view=TicketView())

@bot.tree.command(name="setup_bundle", description="Panel Bundle & Accounts")
@app_commands.checks.has_permissions(administrator=True)
async def sb(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="FiveM Ready", value="FiveM Ready", description="See the price and open a ticket FiveM Ready."),
        discord.SelectOption(label="Steam", value="Steam", description="See the price and open a ticket Steam."),
        discord.SelectOption(label="D1scörd", value="D1scörd", description="See the price and open a ticket D1scörd."),
        discord.SelectOption(label="IP Vanish", value="IP Vanish", description="See the price and open a ticket IP Vanish."),
        discord.SelectOption(label="NexHub", value="NexHub", description="See the price and open a ticket NexHub.")
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="Kliknij aby wybrac", options=options))
    desc = (
        "Accounts available from us:\n"
        f"> • {E_FIVEM} FiveM Ready\n"
        f"> • {E_STEAM} Steam\n"
        f"> • {E_DISCORD} D1scörd\n\n"
        "VPN available from us:\n"
        f"> • {E_IPVANISH} IP Vanish\n"
        f"> • {E_NEXHUB} NexHub\n\n"
        "Select the product you are interested in."
    )
    embed = discord.Embed(title="Velox Products x PREMIUM", description=desc, color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_cheats", description="Panel FiveM Cheats")
@app_commands.checks.has_permissions(administrator=True)
async def scheats(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="Echo.fun", value="Echo.fun", description="See the price and open a ticket Echo.fun.", emoji=PE_ECHO),
        discord.SelectOption(label="Ambani", value="Ambani", description="See the price and open a ticket Ambani.", emoji=PE_AMBANI),
        discord.SelectOption(label="Worm", value="Worm", description="See the price and open a ticket Worm.", emoji=PE_WORM)
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="Kliknij aby wybrac", options=options))
    desc = (
        "Cheats available from us:\n"
        f"> • {E_ECHO} Echo.fun\n"
        f"> • {E_AMBANI} Ambani\n"
        f"> • {E_WORM} Worm\n\n"
        "Select the cheat you are interested in."
    )
    embed = discord.Embed(title="Velox Products x FiveM Cheats", description=desc, color=discord.Color.blue())
    embed.set_image(url=CHEAT_BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_spoofer", description="Panel FiveM Spoofer")
@app_commands.checks.has_permissions(administrator=True)
async def sspoof(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="Echo.fun", value="Echo.fun", description="See the price and open a ticket Echo.fun Spoofer.", emoji=PE_ECHO)
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="Kliknij aby wybrac", options=options))
    desc = (
        "Spoofers available from us:\n"
        f"> • {E_ECHO} Echo.fun\n\n"
        "Select the product you are interested in."
    )
    embed = discord.Embed(title="Velox Products x FiveM SpooferS", description=desc, color=discord.Color.blue())
    embed.set_image(url=SPOOFER_BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_vpn", description="Panel VPN")
@app_commands.checks.has_permissions(administrator=True)
async def svpn(inter: discord.Interaction):
    options = [
        discord.SelectOption(label="IP Vanish", value="IP Vanish VPN", description="Year - €1 / 4.5 zl"),
        discord.SelectOption(label="NexHub", value="NexHub VPN", description="See the price and open a ticket NexHub.")
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="Zakup Produkt", options=options))
    desc = (
        "VPN available from us:\n"
        f"> {E_IPVANISH} IP Vanish\n"
        f"> {E_NEXHUB} NexHub\n\n"
        "Ceny:\n"
        f"> {E_IPVANISH} Year - €1 / 4.5 zl"
    )
    embed = discord.Embed(title="VPN", description=desc, color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.response.send_message(embed=embed, view=v)

@bot.tree.command(name="setup_verify", description="Panel weryfikacji")
@app_commands.checks.has_permissions(administrator=True)
async def setup_verify(inter: discord.Interaction):
    desc = (
        "Welcome to Velox Shop!\n\n"
        "To gain access to the rest of the server and unlock all channels, "
        "please verify your account by clicking the button below."
    )
    embed = discord.Embed(title="Verification", description=desc, color=discord.Color.dark_embed())
    embed.set_image(url=BANNER)
    await inter.response.send_message(embed=embed, view=VerifyView())

@bot.tree.command(name="bandc", description="Banowanie uzytkownika")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(user="Uzytkownik", reason="Powod")
async def bandc(inter: discord.Interaction, user: discord.Member, reason: str = "Brak powodu"):
    await inter.guild.ban(user, reason=reason)
    desc = (
        f"User:\n`{user}` (ID: `{user.id}`)\n\n"
        f"Administrator:\n{inter.user.mention}\n\n"
        f"Reason:\n`{reason}`"
    )
    embed = discord.Embed(title="User has been banned for life", description=desc, color=discord.Color.red())
    embed.set_image(url=BANNER)
    await inter.response.send_message(embed=embed)

@bot.tree.command(name="unban", description="Odbanowanie uzytkownika")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.describe(user_id="ID uzytkownika")
async def unban(inter: discord.Interaction, user_id: str):
    user = await bot.fetch_user(int(user_id))
    await inter.guild.unban(user)
    await inter.response.send_message(f"Pomyślnie odbanowano użytkownika `{user}`.", ephemeral=True)