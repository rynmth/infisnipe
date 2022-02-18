import discord
import secrets
from discord.ext import commands

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print("Connected.")

snipped:dict = {}

@bot.event
async def on_message_delete(message):
    if not message.guild.id in snipped:
        snipped[message.guild.id] = {'name':[], 'discriminator':[], 'avatar':[], 'message':[], 'attachment':[], 'channel':[], 'data':[]}

    snipped[message.guild.id]['name'].insert(0, message.author.name)
    snipped[message.guild.id]['discriminator'].insert(0, message.author.discriminator)
    snipped[message.guild.id]['avatar'].insert(0, message.author.avatar_url)
    snipped[message.guild.id]['message'].insert(0, message.content)
    snipped[message.guild.id]['channel'].insert(0, message.channel.name)
    snipped[message.guild.id]['data'].insert(0, message.created_at)

    if message.attachments:
        snipped[message.guild.id]['attachment'].insert(0, message.attachments[0])
    
    if not message.attachments:
        snipped[message.guild.id]['attachment'].insert(0, None)

@bot.command()
async def snipe(ctx, num:int = 0):
    try:
        try:
            for type in ['mp4', 'webm', 'mov']:
                if snipped[ctx.guild.id]['attachment'][num].filename[-len(type)-1:]==f'.{type}':
                    embed = discord.Embed(description=snipped[ctx.guild.id]['message'][num], timestamp=snipped[ctx.guild.id]['data'][num], color=discord.Color.random())
                    embed.set_author(name=f"{snipped[ctx.guild.id]['name'][num]}#{snipped[ctx.guild.id]['discriminator'][num]}", icon_url=snipped[ctx.guild.id]['avatar'][num])
                    embed.set_footer(text=f"#{snipped[ctx.guild.id]['channel'][num]}")
                    await ctx.channel.send(embed=embed)
                    await ctx.channel.send(snipped[ctx.guild.id]['attachment'][num])
                    return
        
            embed = discord.Embed(description=snipped[ctx.guild.id]['message'][num], timestamp=snipped[ctx.guild.id]['data'][num], color=discord.Color.random())
            embed.set_author(name=f"{snipped[ctx.guild.id]['name'][num]}#{snipped[ctx.guild.id]['discriminator'][num]}", icon_url=snipped[ctx.guild.id]['avatar'][num])
            embed.set_image(url=snipped[ctx.guild.id]['attachment'][num])
            embed.set_footer(text=f"#{snipped[ctx.guild.id]['channel'][num]}")
            await ctx.channel.send(embed=embed)

        except:
            embed = discord.Embed(description=snipped[ctx.guild.id]['message'][num], timestamp=snipped[ctx.guild.id]['data'][num], color=discord.Color.random())
            embed.set_author(name=f"{snipped[ctx.guild.id]['name'][num]}#{snipped[ctx.guild.id]['discriminator'][num]}", icon_url=snipped[ctx.guild.id]['avatar'][num])
            embed.set_footer(text=f"#{snipped[ctx.guild.id]['channel'][num]}")
            await ctx.channel.send(embed=embed)

    except:
        await ctx.send("Nothing to snipe.")

edited:dict = {}

@bot.event
async def on_message_edit(message_before, message_after):
    if not message_after.guild.id in edited:
        edited[message_after.guild.id] = {'name':[], 'discriminator':[], 'avatar':[], 'msgBefore':[], 'msgAfter':[], 'channel':[], 'data':[]}
    
    edited[message_after.guild.id]['name'].insert(0, message_after.author.name)
    edited[message_after.guild.id]['discriminator'].insert(0, message_after.author.discriminator)
    edited[message_after.guild.id]['avatar'].insert(0, message_after.author.avatar_url)
    edited[message_after.guild.id]['msgBefore'].insert(0, message_before.content)
    edited[message_after.guild.id]['msgAfter'].insert(0, message_after.content)
    edited[message_after.guild.id]['channel'].insert(0, message_after.channel.name)
    edited[message_after.guild.id]['data'].insert(0, message_after.created_at)

@bot.command()
async def editsnipe(ctx, num:int = 0):
    try:
        embed = discord.Embed(timestamp=edited[ctx.guild.id]['data'][num], color=discord.Color.random())
        embed.set_author(name=f"{edited[ctx.guild.id]['name'][num]}#{edited[ctx.guild.id]['discriminator'][num]}", icon_url=edited[ctx.guild.id]['avatar'][num])
        embed.add_field(name="Before", value=edited[ctx.guild.id]['msgBefore'][num])
        embed.add_field(name="After", value=edited[ctx.guild.id]['msgAfter'][num])
        embed.set_footer(text=f"#{edited[ctx.guild.id]['channel'][num]}")
        await ctx.channel.send(embed=embed)
    except:
        await ctx.channel.send("Nothing to editsnipe.")

bot.run(secrets.token)