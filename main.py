import discord
from discord.ext import commands
import cogs
import settings
import random
import misc

bot = commands.Bot(command_prefix='=')

bot.add_cog(cogs.Moderation(bot))
bot.add_cog(cogs.Fun(bot))
bot.add_cog(cogs.Utility(bot))

@bot.event
async def on_ready():
    activity = discord.Activity(name=bot.command_prefix+'help', type=discord.ActivityType.watching)
    await bot.change_presence(activity = activity)
    bot.appinfo = await bot.application_info()
    print('Logged in as '+str(bot.user)+'\n---\nGuilds: '+str(len(bot.guilds)))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingPermissions):
        await ctx.send("You don't have the required permissions to use that command.\nMissing permission(s): `"+', '.join(error.missing_perms)+'`.')
    if isinstance(error, discord.ext.commands.BotMissingPermissions):
        await ctx.send("I don't have permission to do that here!\nAsk a server owner to give me the `"+', '.join(error.missing_perms)+"` permission(s).")
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("Looks like you're missing a required argument there.")
    if isinstance(error, discord.ext.commands.BadArgument):
        await ctx.send("Invalid argument(s) provided.")
    print(str(error))
class AutoArchHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

    async def send_bot_help(self, mapping):
        ctx = self.context
        help_embed = discord.Embed(
            title = 'Commands',
            description = self.get_opening_note(),
            colour = discord.Colour.gold()
        )
        help_embed.set_footer(text = misc.get_embed_footer(ctx))
        help_embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        for cog in mapping.keys():

            name = 'Other'
            if cog != None:
                name = cog.qualified_name
                if hasattr(cog, 'custom_icon'):
                    name = cog.custom_icon + ' ' + name

            help_embed.add_field(name = name, value = ', '.join([command.name for command in mapping[cog]]))

        await self.get_destination().send(embed = help_embed)

    async def send_command_help(self, command):
        ctx = self.context
        help_embed = discord.Embed(
            title = self.get_command_signature(command),
            description = command.help,
            colour = discord.Colour.gold()
        )
        help_embed.set_footer(text = misc.get_embed_footer(ctx))
        help_embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        await self.get_destination().send(embed = help_embed)

    async def send_cog_help(self, cog):
        ctx = self.context
        commands = ', '.join([command.qualified_name for command in cog.get_commands()])
        help_embed = discord.Embed(
            title = cog.qualified_name,
            description = commands,
            colour = discord.Colour.gold()
        )
        help_embed.set_footer(ttext = misc.get_embed_footer(ctx))
        help_embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        await self.get_destination().send(embed = help_embed)

    async def send_group_help(self, group):
        ctx = self.context
        commands = ', '.join([command.qualified_name for command in group.commands])
        help_embed = discord.Embed(
            title = group.qualified_name + ' Subcommands',
            description = commands,
            colour = discord.Colour.gold()
        )
        help_embed.set_footer(text = misc.get_embed_footer(ctx))
        help_embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)

        await self.get_destination().send(embed = help_embed)

@bot.command(help = 'Link to the bot\'s GitHub repo.')
async def source(ctx):
    source_embed = discord.Embed(
        title = 'Bot Source',
        description = 'The full source code is available at\n'+settings.source+'\nand is licensed under '+settings.license+'.',
        colour = discord.Colour.gold()
    )
    source_embed.set_thumbnail(url = ctx.bot.user.avatar_url)
    source_embed.set_footer(text = misc.get_embed_footer(ctx))
    source_embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
    await ctx.send(embed = source_embed)

@bot.command(help = 'Shows information about the bot.')
async def info(ctx):
    info_embed = discord.Embed(
        title = 'Bot Info',
        description = 'I\'m '+ctx.bot.user.mention+', and I was created by '+str(ctx.bot.appinfo.owner)+'.\nSee `'+ctx.bot.command_prefix+'help` for a list of commands.\nI can see `'+str(len(bot.guilds))+'` servers and have a latency of `'+str(int(bot.latency*1000))+'` ms.',
        colour = discord.Colour.gold()
    )
    info_embed.set_thumbnail(url = ctx.bot.user.avatar_url)
    info_embed.set_author(name = str(ctx.author), icon_url = ctx.author.avatar_url)
    info_embed.set_footer(text = misc.get_embed_footer(ctx))
    await ctx.send(embed = info_embed)

@bot.command(help = 'Shows the bot\'s latency.')
async def ping(ctx):
    ping_embed = discord.Embed(
        title = 'Pong!',
        description = 'Bot latency: `'+str(int(ctx.bot.latency*1000))+' ms`',
        colour = discord.Colour.gold()
    )
    ping_embed.set_thumbnail(url=ctx.bot.user.avatar_url)
    ping_embed.set_author(name = str(ctx.author), icon_url = ctx.author.avatar_url)
    ping_embed.set_footer(text = misc.get_embed_footer(ctx))
    await ctx.send(embed=ping_embed)

bot.help_command = AutoArchHelpCommand()

bot.run(settings.token)
