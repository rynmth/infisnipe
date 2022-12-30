from discord import Embed, Intents, Message, Color
from discord.ext import commands
from snipe import Snipe, EditSnipe

bot = commands.Bot(command_prefix='.', help_command=None, intents=Intents.all())
TOKEN = "Your token here."

snipped : dict[int, list[Snipe]] = {}
edited : dict[int, list[EditSnipe]] = {}


@bot.event
async def on_ready() -> None:
    for guild in bot.guilds:
        snipped[guild.id] = []
        edited[guild.id] = []

    print('Connected.')


@bot.event
async def on_message_delete(message : Message) -> None:
    snipe = Snipe()

    snipe.name = message.author.name
    snipe.discriminator = message.author.discriminator
    snipe.avatar = message.author.avatar
    snipe.content = message.content
    snipe.channel = message.channel.name
    snipe.date = message.created_at

    snipped[message.guild.id].insert(0, snipe)


@bot.command(name="snipe", aliases=["s"])
async def snipe(ctx : commands.context.Context, num : int = 0) -> None:
    if not snipped[ctx.guild.id] or num < 0 or num > len(snipped[ctx.guild.id]):
        await ctx.send("Nothing to snipe.")
        return

    snipe = snipped[ctx.guild.id][num]

    embed = Embed(
        description = snipe.content,
        timestamp = snipe.date,
        color = Color.random(),
    )
    embed.set_author(name=f"{snipe.name}#{snipe.discriminator}", icon_url=snipe.avatar)
    embed.set_footer(text=f"• {snipe.channel}")

    await ctx.channel.send(embed=embed)


@bot.event
async def on_message_edit(message_before : Message, message_after : Message) -> None:
    edit_snipe = EditSnipe()

    edit_snipe.name = message_after.author.name
    edit_snipe.discriminator = message_after.author.discriminator
    edit_snipe.avatar = message_after.author.avatar
    edit_snipe.content_before = message_before.content
    edit_snipe.content_after = message_after.content
    edit_snipe.channel = message_after.channel.name
    edit_snipe.date = message_after.created_at

    edited[message_after.guild.id].insert(0, edit_snipe)


@bot.command(name="editsnipe", aliases=["es"])
async def editsnipe(ctx : commands.context.Context, num : int = 0):
    if not edited[ctx.guild.id] or num < 0 or num > len(edited[ctx.guild.id]):
        await ctx.send("Nothing to edit snipe.")
        return

    edit_snipe = edited[ctx.guild.id][num]

    embed = Embed(
        timestamp = edit_snipe.date,
        color = Color.random(),
    )
    embed.set_author(name=f"{edit_snipe.name}#{edit_snipe.discriminator}", icon_url=edit_snipe.avatar)
    embed.add_field(name="Before", value=edit_snipe.content_before)
    embed.add_field(name="After", value=edit_snipe.content_after)
    embed.set_footer(text=f"• {edit_snipe.channel}")

    await ctx.channel.send(embed=embed)


bot.run(TOKEN)