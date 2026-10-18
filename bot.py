import os
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

DROP_CH = 1561325772587925514       # Kanał dropu
WELCOME_CH = 1557150071177347152   
VERIFY_ROLE_ID = 1456459830494630102  # Rola weryfikacji

# ID KATEGORII TICKETÓW
CAT_OWNER = 1561333304131715112
CAT_SUPPORT = 1539002224007712911

BANNER = "http://googleusercontent.com/generated_animated_image/15959043500870823950"

# EMOTKI / NAKLEJKI SERWEROWE
E_IPVANISH = "<:ipvanish:1561340558314709082>"
E_FIVEM = "<:fivem:1561340614828621906>"
E_CS2 = "<:cs2:1561340401523363892>"
E_DISCORD = "<:discord:1551370496199761942>"
E_STEAM = "<:steam:1561340474349068338>"
E_NEXHUB = "<:nexhub:1561341038441013368>"

PE_IPVANISH = discord.PartialEmoji(name="ipvanish", id=1561340558314709082)
PE_FIVEM = discord.PartialEmoji(name="fivem", id=1561340614828621906)
PE_CS2 = discord.PartialEmoji(name="cs2", id=1561340401523363892)
PE_DISCORD = discord.PartialEmoji(name="discord", id=1551370496199761942)
PE_STEAM = discord.PartialEmoji(name="steam", id=1561340474349068338)
PE_NEXHUB = discord.PartialEmoji(name="nexhub", id=1561341038441013368)

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

# --- WIDOKI I SYSTEM TICKETÓW ---
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
        await inter.followup.send(f"✅ Stworzono ticket: {ch.mention}", ephemeral=True