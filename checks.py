import discord

# Custom checks

# Returns true if the user has either the ban_members permission *or* administrator permission.
def admin_or_ban(ctx):
    permissions = ctx.author.guild_permissions
    if permissions.administrator == True or permissions.ban_members == True:
        return True
    else:
        raise(discord.ext.commands.MissingPermissions(missing_perms=['ban_members']))

# Returns true if the user has either the kick_members permission *or* administrator permission.
def admin_or_kick(ctx):
    permissions = ctx.author.guild_permissions
    if permissions.administrator == True or permissions.kick_members == True:
        return True
    else:
        raise(discord.ext.commands.MissingPermissions(missing_perms=['kick_members']))

# Returns true if the user has either the manage_guild permission *or* administrator permission.
def admin_or_manage_guild(ctx):
    permissions = ctx.author.guild_permissions
    if permissions.administrator == True or permissions.manage_guild == True:
        return True
    else:
        raise(discord.ext.commands.MissingPermissions(missing_perms=['manage_guild']))

# Returns true if the user has either the manage_messages permission *or* administrator permission.
def admin_or_manage_messages(ctx):
    permissions = ctx.author.guild_permissions
    if permissions.administrator == True or permissions.manage_messages == True:
        return True
    else:
        raise(discord.ext.commands.MissingPermissions(missing_perms=['manage_messages']))

# Returns true if the bot has either the ban_members permission *or* administrator permission.
def bot_admin_or_ban(ctx):
    permissions = ctx.guild.me.guild_permissions
    if permissions.administrator == True or permissions.ban_members == True:
        return True
    else:
        raise(discord.ext.commands.BotMissingPermissions(missing_perms=['ban_members']))

# Returns true if the bot has either the kick_members permission *or* administrator permission.
def bot_admin_or_kick(ctx):
    permissions = ctx.guild.me.guild_permissions
    if permissions.administrator == True or permissions.kick_members == True:
        return True
    else:
        raise(discord.ext.commands.BotMissingPermissions(missing_perms=['kick_members']))

# Returns true if the bot has either the manage_guild permission *or* administrator permission.
def bot_admin_or_manage_guild(ctx):
    permissions = ctx.guild.me.guild_permissions
    if permissions.administrator == True or permissions.manage_guild == True:
        return True
    else:
        raise(discord.ext.commands.BotMissingPermissions(missing_perms=['manage_guild']))

# Returns true if the user has either the manage_messages permission *or* administrator permission.
def bot_admin_or_manage_messages(ctx):
    permissions = ctx.guild.me.guild_permissions
    if permissions.administrator == True or permissions.manage_messages == True:
        return True
    else:
        raise(discord.ext.commands.BotMissingPermissions(missing_perms=['manage_messages']))
