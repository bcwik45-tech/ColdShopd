import os
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

DROP_CH = 1561325772587925514       # Zaktualizowany kanał dropu
WELCOME_CH = 1557150071177347152   
VERIFY_ROLE_ID = 1456459830494630102  

# ID KATEGORII TICKETÓW
CAT_OWNER = 1561333304131715112
CAT_SUPPORT = 1539002224007712911

BANNER = "http://googleusercontent.com/generated_animated_image/15959043500870823950"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class VeloxShopBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        try:
            await self.tree.sync()
            print("✅ [VELOX SHOP] Komendy zsynchronizowane globalnie!")
        except Exception as e:
            print(f"⚠️ Błąd synchronizacji komend: {e}")

bot = VeloxShopBot()

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
        "Welcome to **Velox Shop**!\n"
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

# --- WIDOKI I SYSTEM TICKETÓW (BEZ GIFA, Z IKONKĄ W NAZWIE KANAŁU) ---
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

        # Nazwa kanału z ikonką kategorii (np. 🛒-ticket-shop-nazwa)
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
                "Administracja wkrótce odpowie na Twoje zgłoszenie.\n\n"
                "Aby zamknąć ten kanał, kliknij przycisk poniżej."
            ),
            color=discord.Color.blue()
        )
        
        ping_content = f"{user.mention} " + " ".join(roles_to_ping)
        await ch.send(content=ping_content, embed=embed, view=CloseView())
        await inter.followup.send(f"✅ Stworzono ticket: {ch.mention}", ephemeral=True)

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
        category = inter.guild.get_channel(CAT_SUPPORT)
        ch = await inter.guild.create_text_channel(
            name=f"🛒-ticket-{inter.user.name.lower()}",
            category=category,
            overwrites={
                inter.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                inter.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                inter.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )
        embed = discord.Embed(
            title=f"Ticket: SHOP",
            description=(
                f"Witaj {inter.user.mention}!\n"
                f"Otworzyłeś ticket zakupowy dla: **{product_name}**.\n"
                "Administracja wkrótce odpowie na Twoje zgłoszenie.\n\n"
                "Aby zamknąć ten kanał, kliknij przycisk poniżej."
            ),
            color=discord.Color.blue()
        )
        role_shop = inter.guild.get_role(1456459709405204542)
        ping = role_shop.mention if role_shop else ""
        await ch.send(content=f"{inter.user.mention} {ping}", embed=embed, view=CloseView())
        await inter.followup.send(f"✅ Stworzono ticket: {ch.mention}", ephemeral=True)

class LegitView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.y, self.n = 0, 0

    @discord.ui.button(label="0", emoji="✅", style=discord.ButtonStyle.secondary, custom_id="leg_y")
    async def yes(self, inter: discord.Interaction, btn: discord.ui.Button):
        self.y += 1
        btn.label = str(self.y)
        await inter.response.edit_message(view=self)
        await inter.followup.send("Dzięki za głos!", ephemeral=True)

    @discord.ui.button(label="0", emoji="🔖", style=discord.ButtonStyle.secondary, custom_id="leg_n")
    async def no(self, inter: discord.Interaction, btn: discord.ui.Button):
        self.n += 1
        btn.label = str(self.n)
        await inter.response.edit_message(view=self)
        await inter.followup.send("Dzięki za głos!", ephemeral=True)

# --- KOMENDY SETUPU, SAY I MODERACJI ---

@bot.tree.command(name="say", description="Wysyła podaną wiadomość na kanale")
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(message="Treść wiadomości do wysłania")
async def say(inter: discord.Interaction, message: str):
    await inter.channel.send(message)
    await inter.response.send_message("✅ Wysyłano wiadomość!", ephemeral=True)

@bot.tree.command(name="setup_legitchecks", description="Panel legit check z opcją oceniania")
@app_commands.checks.has_permissions(administrator=True)
async def sl(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    
    desc = (
        "📢 **Jeżeli uważasz, że jesteśmy legit, zaznacz reakcję ✅ pod tą wiadomością.**\n"
        "🔔 **Zaznaczenie reakcji 🔖 będzie skutkować otrzymaniem przerwy na okres 7 dni.**"
    )
    
    embed = discord.Embed(title="🕵️ CZY JESTEŚMY LEGIT?", description=desc, color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=LegitView())
    await inter.followup.send("Gotowe!", ephemeral=True)

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
        "Welcome to **Velox Shop**! ⚡\n\n"
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
        discord.SelectOption(label="Steam", value="Steam", description="See the price and open a ticket Steam.", emoji=e_steam),
        discord.SelectOption(label="D1scörd", value="D1scörd", description="See the price and open a ticket D1scörd.", emoji=e_dc),
        discord.SelectOption(label="CS2 Prime Accounts", value="CS2 Prime Accounts", description="See the price and open a ticket CS2 Prime Accounts.", emoji=e_cs),
        discord.SelectOption(label="IP Vanish", value="IP Vanish", description="See the price and open a ticket IP Vanish.", emoji=e_ip),
        discord.SelectOption(label="NexHub", value="NexHub", description="See the price and open a ticket NexHub.", emoji=e_nex)
    ]
    
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="❌ × Click to select | Kliknij aby wybrać", options=options))
    
    desc = (
        "Accounts **available** from us:\n"
        f"> • {e_fivem} **FiveM Ready**\n"
        f"> • {e_steam} **Steam**\n"
        f"> • {e_dc} **D1scörd**\n"
        f"> • {e_cs} **CS2 Prime Accounts**\n\n"
        "VPN's **available** from us:\n"
        f"> • {e_ip} **IP Vanish**\n"
        f"> • {e_nex} **NexHub**\n\n"
        "🔊 Select the product you are **interested** in.\n"
        "🔊 At the **bottom** of the select menu, select duration and payment.\n\n"
        "🌐 **Instant Buy:** **Click here to visit our website**"
    )
    
    embed = discord.Embed(title="💎 ✖️ Velox Products × PREMIUM", description=desc, color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=v)
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_vpn", description="Panel VPN")
@app_commands.checks.has_permissions(administrator=True)
async def svpn(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    e_ip = discord.PartialEmoji(name="ipvanish", id=1561307428643930152)
    e_nex = discord.PartialEmoji(name="nexhub", id=1561308489933127810)

    options = [
        discord.SelectOption(label="IP Vanish", value="IP Vanish VPN", description="Year - €1 / 4.5 zł", emoji=e_ip),
        discord.SelectOption(label="NexHub", value="NexHub VPN", description="See the price and open a ticket NexHub.", emoji=e_nex)
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="❌ × Purchase Product | Zakup Produkt", options=options))
    
    desc = (
        "VPN's **available** from us:\n"
        f"> {e_ip} **IP Vanish**\n"
        f"> {e_nex} **NexHub**\n\n"
        "» **Ceny:**\n"
        f"> {e_ip} Year ✖️ **€1 / 4.5 zł**\n\n"
        "» **Krótki Opis:**\n"
        "> ✅ » Full Acces\n"
        "> ✅ » Gotowy do użycia"
    )
    embed = discord.Embed(title=f"IPVAN$SH {e_ip}", description=desc, color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=v)
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_cs", description="Panel Counter-Strike 2")
@app_commands.checks.has_permissions(administrator=True)
async def scs(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    e_cs = discord.PartialEmoji(name="csprime", id=1561307515067834428)
    options = [discord.SelectOption(label="Account Prime", value="CS2 Account Prime", description="Konto CS2 ze statusem Prime", emoji=e_cs)]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="❌ × Purchase Product | Zakup Produkt", options=options))
    embed = discord.Embed(title=f"🎯 VELOX SHOP × COUNTER-STRIKE 2 {e_cs}", description="Wybierz ofertę Prime z listy poniżej:", color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=v)
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="setup_shop", description="Sklep / Dodatki")
@app_commands.checks.has_permissions(administrator=True)
async def sshop(inter: discord.Interaction):
    await inter.response.defer(ephemeral=True)
    options = [
        discord.SelectOption(label="Citizen", value="Citizen Custom", emoji="🌅"),
        discord.SelectOption(label="Soundpacks", value="Soundpacks", emoji="🔊")
    ]
    v = discord.ui.View(timeout=None)
    v.add_item(ShopSelect(placeholder="❌ × Purchase Product | Zakup Produkt", options=options))
    embed = discord.Embed(title="🛒 VELOX SHOP × ADDONS", description="Wybierz dodatek z listy poniżej:", color=discord.Color.blue())
    embed.set_image(url=BANNER)
    await inter.channel.send(embed=embed, view=v)
    await inter.followup.send("Gotowe!", ephemeral=True)

@bot.tree.command(name="feedback", description="Opinia")
@app_commands.checks.has_permissions(administrator=True)
async def fb(inter: discord.Interaction):
    await inter.response.send_message("⭐ Dziękujemy za zakupy w Velox Shop!", ephemeral=True)

@bot.tree.command(name="drop", description="Drop")
async def dp(inter: discord.Interaction):
    if inter.channel_id != DROP_CH:
        await inter.response.send_message("❌ Zły kanał!", ephemeral=True)
        return
    if random.randint(1, 100) <= 5:
        await inter.response.send_message(f"🎉 {inter.user.mention} wygrał 20% zniżki w Velox Shop!")
    else:
        await inter.response.send_message(f"⚡ Niestety {inter.user.mention}, spróbuj ponownie.")

bot.run(TOKEN)