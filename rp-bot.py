import discord
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter, File
import aiohttp
from config import token

bot = commands.Bot(command_prefix='#@')
print(bot)

tags = []
outlines = {}
servers = {}


@bot.event
async def on_ready():

    #all file processing
    #the file template is this: server, tag, start, end
    file = open('botlist.txt','r')
    print('loading characters')
    lines = file.readlines()

    for i in lines:
        i = i.split('&$^#(# ')
        tags.append(i[0])
        outlines[i[0]] = {i[1]:(i[2],i[3][:-2])}
        #file processing end
        print('logged in as')
        print(bot.user.name)
        print(bot.user.id)

    file.close()

    print('loading webhooks')
    webs = open('webhooks.txt','r')
    weblines = webs.readlines()
    lastOne = None

    for i in weblines:
        i = i.split('&$^#(# ')
        if lastOne != i[0]:
            channels = {}
            lastOne = i[0]
        else:
            channels[i[1]] = i[2][:-2]

        servers[i[0]] = channels
        webs.close()

@bot.event
async def on_message(message):
    Bot = message.author.bot
    await bot.process_commands(message)
    server = message.channel.guild.name
    channel = message.channel.name

    if Bot == False and servers[server][channel] != None:
        webhook = servers[server][channel]
        for i in outlines[server]:
            for y in message.author.roles:
                if i == y.name and outlines[server][i][0] in message.content and outlines[server][i][1]:
                    text = message.content.split(outlines[server][i][0])
                    text = text[1].split(outlines[server][i][1])
                    Message = text[0]
                    name = i
                    await webhook.send(Message, username=name)
                    await message.delete()

#commands
@bot.command()
async def setup(ctx):
    channel = ctx.message.channel
    webhook = await channel.create_webhook(name=channel.name)
    servers[ctx.guild][channel] = webhook



@bot.command(description='use this command to make your own character, usage: addchar [character name] [beginning of character text] [end of character text]')
async def addChar(ctx, tag, start, end):
    guild = ctx.guild
    user = ctx.message.author
    new_role = await guild.create_role(name=tag,mentionable=True)
    await user.add_roles(new_role)
    outlines[server][tag] = [start, end]


@bot.command(description= 'edit a charcters name, you can only do this if you have the role for it! usage: editName [current char name] [new character name]')
async def editName(ctx, char, newName):
    if char in ctx.message.author.roles:
        guild = ctx.guild
        user = ctx.message.author
        new_role = await guild.create_role(name=newName,metionable=True)

        #remove old role
        await guild.remove_role(char)

        #add the new role to the server
        await guild.add_role(new_role)
        await user.add_roles(new_role)

        #update the dictionary
        old = outlines.pop(char)
        outlines[guild][new_char] = old
    else:
        await webhook.send('you do not have permission to change me!',username=char)

bot.run(token)
