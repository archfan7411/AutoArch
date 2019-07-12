import discord
from discord.ext import commands
import settings
import random

def get_embed_footer(ctx):
    footer = random.choice(settings.quotes_short)
    if hasattr(ctx.bot, 'appinfo'):
        footer += ' | Created by ' + str(ctx.bot.appinfo.owner)
    return footer