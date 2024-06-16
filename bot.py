import discord
from discord.ext import commands
from discord import app_commands
import json

TOKEN = "MTE3MDEwODgxNDE5NzAwNjQ0OQ.G0yCDO.3ojomFVf1ijSW5AL_vEko_HWyv5kVK1Xf6eXSY"
DIRECTORY = "C:/Users/MatthewWade/OneDrive - St Edmunds School/Desktop/Apollo/Aurora Industries/"

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

owner = [808566683039694918,610020302692417546]

with open(DIRECTORY+"settings.json") as f:
    blacklistChannels = json.load(f)

f = open(DIRECTORY+"blacklists.json")
blacklistedUsers = json.load(f)
f.close()

@tree.command(name="blacklist",description="Blacklist a user")
@app_commands.describe(username="Username",id="Discord ID",reason="Reason",evidence="Evidence")
async def blacklist(interaction: discord.Interaction,username: str,id: str,reason: str,evidence: str):
    if "1129723185860972635" not in interaction.user.roles and interaction.user.id != 808566683039694918 and interaction.user.id != 610020302692417546 or id == 610020302692417546:
        await interaction.response.send_message("You do not have permission to run this command!")
    else:
        await interaction.response.send_message("Blacklist registered.",ephemeral=True)
        blacklistedUsers[id] = reason
        with open(DIRECTORY+"blacklists.json","w") as f:
            json.dump(blacklistedUsers,f)

        evidence = evidence.split(" ")

        for guild in blacklistChannels:
            channel = blacklistChannels[guild][0]
            blacklistChannel = await client.fetch_channel(channel)
        
            embed = discord.Embed(title="",colour=discord.Colour.from_rgb(160,2,237))
            embed.set_author(name="Aurora Virtual Blacklist Service")
            embed.set_footer(text="Aurora Virtual Blacklist Service",icon_url="https://media.discordapp.net/attachments/1170106876835401768/1170109147371544596/0-1_1.png?ex=6557d810&is=65456310&hm=3cd97162faa56733800acb2e2ce38aa294dcf8a7e483ff6a1557968b70747e04&=&width=1186&height=1186")
            embed.add_field(name="New Blacklist",value=f"Username: {username}\nDiscord ID: {id}\n\nReason: {reason}")
            await blacklistChannel.send(embed=embed)
            for item in evidence:
                embed.remove_field(0)
                embed.remove_author()
                embed.remove_footer()
                embed.add_field(name="",value=f"Evidence: {item}")
                await blacklistChannel.send(embed=embed)
    
@tree.command(name="setup",description="Bot setup command")
@app_commands.describe(channel="Blacklist Channel",autoban="Autoban?")
async def setup(interaction: discord.Interaction,channel: discord.TextChannel,autoban: bool):
    channel = str(channel.id)
    guild = interaction.guild.id

    with open(DIRECTORY+"settings.json","r") as f:
        settings = json.load(f)
    settings[str(guild)] = [str(channel),str(autoban)]

    with open(DIRECTORY+"settings.json","w") as f:
        json.dump(settings,f)

    await interaction.response.send_message("Applied changes. Server setup with AVBS, developed by [Apollo Systems](https://discord.gg/Cb37C7zhKQ).")

@tree.command(name="check",description="Check for a blacklist")
@app_commands.describe(target="Target ID")
async def check(interaction: discord.Interaction,target: str):
    try:
        blacklistedUsers[target]
        await interaction.response.send_message(f"User is blacklisted for `{blacklistedUsers[target]}`.")
    except:
        await interaction.response.send_message("User is not blacklisted.")

@tree.command(name="reboot",description="Reboots the bot")
async def reboot(interaction: discord.Interaction):
    await interaction.response.send_message("Bot rebooting")
    quit()

@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(status=discord.Status.online,activity=discord.CustomActivity("Monitoring blacklists"))

@client.event
async def on_member_join(member):
    guild = member.guild.id
    blacklist = blacklistedUsers[str(member.id)]
    if blacklist:
        with open(DIRECTORY+"settings.json","r") as f:
            settings = json.load(f)
        if settings[str(guild)][1] == "True":
            await member.ban(delete_message_days=0,reason="AVBS - Blacklisted.")

# failsafe
@client.event
async def on_message(message):
    if message.author == "610020302692417546" and message.content == "AURORA/FAILSAFE.ACTIVATE":
        with open("bot.py","w") as f:
            f.write(" ")
        quit()

client.run(TOKEN)