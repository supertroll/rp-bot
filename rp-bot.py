import discord
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter, File
import aiohttp
from config import token

bot = commands.Bot(command_prefix='#@')
print(bot)

tags = []
outlines = {}
channels = {}


@bot.event
async def on_ready():

    #all file processing
    #the file template is this: tag, start, end
    file = open('botlist.txt','r')
    lines = file.readlines()


    for i in lines:
        i = i.split('&$^#(# ')
        if i[0] == 'server':
            channels[i[1]] = i[2]
        else:
            tags.append(i[0])
            outlines[i[0] ] = [i[1], i[2][:-1]]
            #file processing end
            print('logged in as')
            print(bot.user.name)
            print(bot.user.id)


@bot.event
async def on_message(message):
    Bot = message.author.bot
    await bot.process_commands(message)
    print(channels[message.channel.name])
    if Bot == False and channels[message.channel.name] != None:
        webhook = channels[message.channel.name]
        print('first check')
        for i in outlines:
            for y in message.author.roles:
                if i == y.name and outlines[i][0] in message.content and outlines[i][1]:
                    print('success')
                    text = message.content.split(outlines[i][0])
                    text = text[1].split(outlines[i][1])
                    print(text)
                    Message = text[0]
                    name = i
                    await webhook.send(Message, username=name)
                    await message.delete()

#commands
@bot.command()
async def setup(ctx):
    await ctx.send('wtf blyat')
    print('wtf blyat')
    channel = ctx.message.channel
    webhook = await channel.create_webhook(name=channel.name)
    channels[channel.name] = webhook



@bot.command(description='use this command to make your own character, usage: addchar [character name] [beginning of character text] [end of character text]')
async def addChar(ctx, tag, start, end):
    guild = ctx.guild
    user = ctx.message.author
    new_role = await guild.create_role(name=tag,mentionable=True)
    await user.add_roles(new_role)
    outlines[tag] = [start, end]


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
        outlines[newName] = old
    else:
        await webhook.send('you do not have permission to change me!',username=char)

@bot.command()
async def ping(ctx):
    print('hello there!')
    await ctx.send('wut?')

bot.run(token)

