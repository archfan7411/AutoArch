import discord
from discord.ext import commands
import random
import settings
import checks
import misc

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_icon = '\U0001f528'

    @commands.command(help = 'Bans any number of mentioned users.')
    @commands.check(checks.admin_or_ban)
    @commands.check(checks.bot_admin_or_ban)
    @commands.guild_only()
    async def ban(self, ctx, *, args):
        members = ctx.message.mentions
        if len(members) == 0:
            await ctx.send('Please mention at least one member to ban.')
            return
        i = 0
        for user in members:
            try:
                await ctx.guild.ban(user)
                i += 1
            except:
                await ctx.send("Error: Could not ban "+str(user))
        await ctx.send('Banned '+str(i)+' member(s).')

    @commands.command(help = 'Kicks any number of mentioned users.')
    @commands.check(checks.admin_or_kick)
    @commands.check(checks.bot_admin_or_kick)
    @commands.guild_only()
    async def kick(self, ctx, *, args):
        members = ctx.message.mentions
        if len(members) == 0:
            await ctx.send('Please mention at least one member to kick.')
            return
        i = 0
        for user in members:
            try:
                await ctx.guild.kick(user)
                i += 1
            except:
                await ctx.send("Error: Could not kick "+str(user))
        await ctx.send('Kicked '+str(i)+' member(s).')

    @commands.command(help = 'Mass-deletes a specified number of messages in the current channel.')
    @commands.check(checks.admin_or_manage_messages)
    @commands.check(checks.bot_admin_or_manage_messages)
    async def clear(self, ctx, amount : int):
        if amount < 1:
            await ctx.send('You can only clear a positive number of messages!', delete_after=5)
            return
        await ctx.message.delete()
        i = 0
        async for message in ctx.channel.history(limit = amount):
            try:
                await message.delete()
                i += 1
            except:
                continue
        await ctx.send('Cleared '+str(i)+' messages.', delete_after = 5)

    @commands.command(help = 'Adds a vote in the #voting channel, if it exists.')
    @commands.check(checks.admin_or_manage_guild)
    @commands.guild_only()
    async def vote(self, ctx, *, args):
        vote_embed = discord.Embed(
            title = 'Vote!',
            description = args,
            colour = discord.Colour.gold()
        )

        for channel in ctx.guild.channels:
            if channel.name == 'voting':
                try:
                    msg = await channel.send(embed=vote_embed)
                    await msg.add_reaction('\U0001f44d')
                    await msg.add_reaction('\U0001f44e')
                    await ctx.message.add_reaction('\U00002705')
                except:
                    await ctx.message.add_reaction('\U0000274e')
                return

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_icon = '\U0001f6a9'

    @commands.command(name = '8ball', help = 'Returns a random response to a yes/no question.')
    async def _8ball(self, ctx, *, args=''):
        choices = ['Maybe...', 'Not entirely sure.', 'Seems probable.', 'Count on it.', 'Most definitely.', 'Would not bet on it.', 'Unsure. Unlikely though.', 'Oh, definitely not.']
        choice = random.choice(choices)
        choice_embed = discord.Embed(
            description = choice,
            colour = discord.Colour.gold()
        )
        choice_embed.set_footer(text = misc.get_embed_footer(ctx))
        choice_embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=choice_embed)

    @commands.command(help = 'Randomly picks an option from a comma-separated list.')
    async def choose(self, ctx, *, options):
        picks = options.split(',')
        choice = random.choice(picks).strip()
        pick_embed = discord.Embed(
            description = 'I pick '+choice+'.',
            colour = discord.Colour.gold()
        )
        pick_embed.set_footer(text = misc.get_embed_footer(ctx))
        pick_embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=pick_embed)

    @commands.command(help = 'Randomly selects a user in the server.')
    async def pickuser(self, ctx):
        pick = random.choice([member for member in ctx.guild.members if not member.bot])
        pick_embed = discord.Embed(
            title = 'I pick...',
            description = pick.mention+'!',
            colour = discord.Colour.gold()
        )
        pick_embed.set_footer(text = misc.get_embed_footer(ctx))
        pick_embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=pick_embed)

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_icon = '\U00002699'

    @commands.command(help = "Links a mentioned user's avatar.")
    async def avatar(self, ctx, member : discord.Member):
        await ctx.send(member.avatar_url)

    @commands.command(help = 'Invite link for the bot.')
    async def invite(self, ctx):
        invite_embed = discord.Embed(
            description = '[Invite me!](https://discordapp.com/api/oauth2/authorize?client_id='+str(ctx.bot.user.id)+'&permissions=0&scope=bot)',
            colour = discord.Colour.gold()
        )
        invite_embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        invite_embed.set_author(name = str(ctx.author), icon_url = ctx.author.avatar_url)
        invite_embed.set_footer(text = misc.get_embed_footer(ctx))
        await ctx.send(embed=invite_embed)

    @commands.command(help = 'Shows information about the server.')
    async def serverinfo(self, ctx):
        guild = ctx.guild
        info_embed = discord.Embed(
            title = ctx.guild.name,
            colour = discord.Colour.gold()
        )
        info_embed.add_field(
            name = 'General',
            value = 'Total members: '+str(len(guild.members))+'\nBot users: '+str(len([member for member in guild.members if member.bot]))+'\nTotal Channels: '+str(len(guild.channels)-len(guild.categories))+'\nText Channels: '+str(len(guild.text_channels))+'\nVoice Channels: '+str(len(guild.voice_channels))
        )
        info_embed.add_field(
            name = 'Server',
            value = 'Owner: '+ctx.guild.owner.mention+'\nTotal Roles: '+str(len(guild.roles))+'\nServer Region: `'+str(guild.region)+'`\nGuild ID: `'+str(guild.id)+'`'
        )
        info_embed.set_thumbnail(url = guild.icon_url)
        info_embed.set_author(name = str(ctx.author), icon_url = ctx.author.avatar_url)
        info_embed.set_footer(text = misc.get_embed_footer(ctx))
        await ctx.send(embed=info_embed)

    @commands.command(help = '"Let Me Google That For You": Returns a link to search the term on Google.')
    async def lmgtfy(self, ctx, *, term):
        msg = 'https://google.com/search?q=' + term.replace(' ', '+')
        await ctx.send(msg)
