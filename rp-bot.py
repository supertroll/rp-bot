import discord
import asyncio
from discord.ext import commands
from discord.webhook import *

client = discord.Client()
bot = commands.Bot(command_prefix='&!')


tags = []
outlines = {}
webhook = None


async def checkForRp(message):
    for i in outlines:
        for y in message.author.roles:
            if i == y.name and outlines[i][0] in message.content and outlines[i][1]:
                text = message.content.split(outlines[i][0])
                text = text[1].split(outlines[i][1])
                print(text)
                return text[0], i


@client.event
async def on_ready():
    print('logged in as')
    print(client.user.name)
    print(client.user.id)

    #all file processing
    #the file template is this: tag, start, end
    file = open('botlist.txt','r')
    lines = file.readlines()
    print(lines)

    for i in lines:
        i = i.split('&$^#(# ')
        print('doing stuff')
        print(i)
        tags.append(i[0])
        outlines[i[0] ] = [i[1], i[2]]
        #file processing end

@client.event
async def on_message(message):
    if bot == False and webhook != None:
       message, name = await checkForRp(message)
       webhook.send(message, username=name)

#commands
@bot.command(description = 'this is the command to setup your channel to the bot(remember that you have to make a webhook first), usage: setup [webhook url]')
async def setup(ctx, webhook_url):
    webhook = webhook.from_url(webhook_urls, adapter=RequestsWebhookAdapter())

@bot.command(description='use this command to make your own character, usage: addchar [character name] [beginning of character text] [end of character text]')
async def addChar(ctx, tag, start, end):
    outlines[tag] = [start, end]


@bot.command(description= 'edit a charcters name, you can only do this if you have the role for it! usage: editName [current char name] [new character name]')
async def editName(ctx, char, newName):
    if char in ctx.message.author.roles:
        old = outlines.pop(char)
    else:
        webhook.send('you do not have permission to change me!',char)

client.run('NDM4NzI3MDczMTQ2ODYzNjI2.DnE6iA.ilE8AU5_W3foTleiosXJJQcHDPo')

