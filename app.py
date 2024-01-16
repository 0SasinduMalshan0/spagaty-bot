import discord
from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font
import os

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1161237379139522581)
    background = Editor("ezgif-5-1eb100f9ea.jpg")
    
    profile_image = await load_image_async(str(member.avatar.url))
    profile = Editor(profile_image).resize((450, 450)).circle_image()
    
    poppins = Font.poppins(size=75, variant="bold")
    poppins_small = Font.poppins(size=20, variant="light")

    background.paste(profile, (740, 200))
    background.text((950, 900), f"{member.name}, Welcome to the server", color=(255, 226, 65), font=poppins, align="center")

    file = File(fp=background.image_bytes, filename="ezgif-5-1eb100f9ea.jpg")
    await channel.send(file=file)
    
    role = discord.utils.get(member.guild.roles, name="MEMBERS")
    await member.add_roles(role)

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id

    # Check if the reaction is added to the specified message
    if message_id == 1196312873287286795:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        # Ensure that the guild is found
        if guild:
            print(f"Guild found: {guild.name}")

            member = guild.get_member(payload.user_id)

            # Print the payload information for debugging
            print(f"Payload: {payload}")

            # Ensure that the member is found
            if member:
                print(f"Member found: {member.display_name}")

                # Check if the reaction emoji is '🎮'
                if payload.emoji.name == '🎮':
                    role = discord.utils.get(guild.roles, name='Gamers')

                    # Ensure that the role is found
                    if role:
                        await member.add_roles(role)
                        print(f"Added role {role.name} to {member.display_name}")
                    else:
                        print("Role 'Gamers' not found in the guild.")
                else:
                    print(f"Ignoring reaction with emoji {payload.emoji.name}")
            else:
                print(f"Member with ID {payload.user_id} not found in the guild.")
        else:
            print(f"Guild with ID {guild_id} not found.")

client.run(os.environ["DISCORD_TOKEN"])
