# Work with Python 3.6
import discord
import json
import os
import random
from common_embed import *

client = discord.Client()

info = [
    ["'1-3 Star Ema List'!D3:G", "Hitagi Crab"],
    ["'1-3 Star Ema List'!J3:M", "Mayoi Snail"],
    ["'1-3 Star Ema List'!P3:S", "Suruga Monkey"],
    ["'1-3 Star Ema List'!V3:Y", "Nadeko Snake"],
    ["'1-3 Star Ema List'!AB3:AE", "Tsubasa Cat"],
    ["'1-3 Star Ema List'!AH3:AK", "Karen Bee"],
    ["'1-3 Star Ema List'!AT3:AW", "Zaregoto"]
]

commands = [
    ["help", "Info about a command.\n\tExample: $help ema", ""],
    ["se", "Search through the 1-3 ema list by star and skill, you can also use 'any' as a parameter.\n\tExample: $searchEma 1;J", "Search 1-3 ema"],
    ["sne", "Search through the 4-5 ema list by name \nExample: $searchCharEma Araragi", "Search 4-5 ema"],
    ["ema", "Get the description of a 4-5 ema by using its number on the doc (You can use searchCharEma to know that number)\nExample: $ema 10", ""],
    ["setup", "Generates a random setup", ""],
    ["snp", "Search pucs by name\n\tExample: $searchPuc Araragi", "Search Puc"],
    ["puc", "Display info about a puc by using his number\n\tExample: $puc 2", ""],
    ["sse", 'Search 4-5 ema by skill\t\nExample: $searchSkillEma Size_Up', "Search ema skill"],
    ["ssp", 'Search pucs by skill\t\nExample: $searchSkillPuc Board_skill', "Search puc skill"],
    ["skill", 'Shows the description of the skill with that letter\n\tExample: $skill A', ""],
    ["strat", 'Shows a strat', ""]
]

server_default_thumbnail = "https://cdn.discordapp.com/attachments/492461461113667605/588696373205925925/cha_block_yotsugi05_v01-CAB-77324350eb109a539abaa89e02cb0576-14837714272648993982.png"

permited_ema_stars = ['1','2','3','4','5','ANY']
permited_ema_skill = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','ANY']

emaList = dict()
emaList4_5 = []
pucs = []

@client.event
async def on_message(message):

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    """
    user = message.author
    server = message.guild

    roles = []
    for rol in user.roles:
        roles.append(rol.id)
    if 589331304445902858 not in roles:
        await user.add_roles(server.get_role(589331304445902858))
    """

    # gets the channel where the message was writen
    channel = message.channel

    if message.content.startswith('$commands'):
        msg = ''
        for command in commands:
            msg = msg  + '$' + command[0]
            if (command[2] != ""): msg = msg + " - " + command[2]
            msg = msg + "\n"
        embed_msg = generic_embed("Commands", msg, "", server_default_thumbnail)
        await channel.send(embed = embed_msg)
    
    # $help
    if message.content.startswith(commandF(0, space=False)):
        command_found = False
        cmd = message.content.split(" ")
        if (len(cmd) != 2):
            if len(cmd) == 1: await channel.send(embed = generic_embed("Help", "Use $commands to see all the commands and `$help command` to see its description", "", server_default_thumbnail))
            else: await channel.send(embed = error_embed())
        else:
            cmd = cmd[1]
            for i in range (0, len(commands)):
                if (cmd == commands[i][0] and cmd != "help"):
                    msg = commands[i][1]
                    command_found = True
            if command_found == True:
                await channel.send(embed = generic_embed("Command " + cmd, msg, "", server_default_thumbnail))
            else:
                await channel.send(embed = error_embed(error = "Command not found"))

    # $searchEma
    elif message.content.startswith(commandF(1)):
        emaList = loadEmaList1_3()
        msg = ""
        find = message.content.split(" ")
        find = find[1].split(";")
        if (len(find) != 2):
            await channel.send(embed = error_embed())
        else:
            if (not(find[0] in permited_ema_stars) or not(find[1] in permited_ema_skill)):
                await channel.send(embed = error_embed(error = "Wrong Parameters"))
            else:
                find[1] = find[1].upper()
                find[0] = find[0].upper()
                for arc in emaList:
                    for ema in emaList[arc]:
                        if((find[1]==ema[1] or find[1]=="ANY") and (find[0]==ema[2] or find[0].upper=="ANY")):
                            msg = msg + "\t%s - %s - %s\n" % (ema[0],ema[1],ema[2])
                if(len(msg) > 2048):
                    embed_msg = error_embed(error="Result too big")
                else:
                    embed_msg = generic_embed("Ema Found", msg, "", server_default_thumbnail)
                await channel.send(embed = embed_msg)
    
    # $searchNameEma
    elif message.content.startswith(commandF(2)):
        emaList4_5 = loadEmaList4_5()
        msg = ""
        find = message.content.split()
        if (len(find) != 2):
            await channel.send(embed = error_embed())
        else:
            for ema in emaList4_5["data"]:
                if( find[1] in ema[0] ):
                    msg = msg + "\t%s - %s\n" % (ema[0], ema[2])
            embed_msg = generic_embed("Ema found", msg, "", server_default_thumbnail)
        await channel.send(embed = embed_msg)
    
    # $ema
    elif message.content.startswith(commandF(3)):
        emaList4_5 = loadEmaList4_5()
        msg = ""
        find = message.content.split()

        if (len(find) != 2):
            await channel.send(embed = error_embed())
        try:
            num = int(find[1])-1
            if(num<len(emaList4_5["data"])):
                ema = emaList4_5["data"][num]
                embed_msg = generic_embed(ema[0], ema[3], ema[4], "")
                await channel.send(embed = embed_msg)
            else:
                await channel.send(embed = error_embed(error="Not in range"))
        except ValueError:
            await channel.send(embed = error_embed(error = "Wrong format, %s is not a number" % find[1]))
    
    # $setup
    elif message.content.startswith(commandF(4, space = False)):
        pucs = loadPucs()
        ema = loadEmaList4_5()
        num_puc = random.randint(0,len(pucs['data']))
        num_ema1 = random.randint(0,len(ema['data']))
        while(True):
            num_ema2 = random.randint(0,len(ema['data']))
            if(num_ema2 != num_ema1):
                break
        msg = pucs['data'][num_puc][0]
        fields = [
            ["Puc", pucs['data'][num_puc][1], False],
            ["Ema 1", ema['data'][num_ema1][0], True],
            ["Ema 2", ema['data'][num_ema2][0], True]
        ]
        embed_msg = field_embed("Setup", "", fields, pucs['data'][num_puc][20], server_default_thumbnail)
        await channel.send(embed=embed_msg)

    # $searchNamePuc
    elif message.content.startswith(commandF(5)):
        pucs = loadPucs()
        msg = ""
        find = message.content.split(" ")
        if (len(find)!=2): embed_msg = error_embed(error="Wrong format")
        else:
            for puc in pucs['data']:
                if find[1] in puc[1]: 
                    msg = msg + "\n" + str(puc[0]) + " " + puc[1]
            embed_msg = generic_embed("Pucs found", msg, "", server_default_thumbnail)
        await channel.send(embed=embed_msg)

    # $puc
    elif message.content.startswith(commandF(6)):
        pucs = loadPucs()
        find = message.content.split(" ")
        if (len(find)!=2): embed_msg = error_embed(error="Wrong format")
        else:
            try:
                num = int(find[1]) - 1
                if(num>=len(pucs['data']) or num<0): embed_msg = error_embed(error="Number not in range")
                else:
                    puc = pucs['data'][num]
                    field = [
                        ["Viability:", puc[3] + "/"+ puc[4], False],
                        ["Rank 1", puc[5], True],
                        ["Rank 2", puc[6], True],
                        ["Rank 3", puc[7], True],
                        ["Rank 4", puc[8], True],
                        ["Rank 5", puc[9], True],
                        ["Rank 6", puc[10], True],
                        ["Rank 7", puc[11], True],
                        ["Rank 8", puc[12], True],
                        ["Score at 100", puc[13], False],
                        ["Score at 120", puc[14], False]
                    ]
                    embed_msg = field_embed(puc[1], puc[len(puc)-2], field, puc[len(puc)-1], server_default_thumbnail)
            except ValueError:
                embed_msg = error_embed(error="%s is not a number" % (find[2]))
        await channel.send(embed=embed_msg)
    
    # $searchSkillEma
    elif message.content.startswith(commandF(7)):
        emaList4_5 = loadEmaList4_5()
        msg = ""
        find = message.content.split()
        if (len(find) != 2):
            await channel.send(embed = error_embed())
        else:
            for ema in emaList4_5["data"]:
                if( find[1].replace("_", " ").lower() in ema[2].lower() ):
                    msg = msg + "\t%s - %s\n" % (ema[0], ema[2])
            embed_msg = generic_embed("Ema found", msg, "", server_default_thumbnail)
        await channel.send(embed = embed_msg)
    
    # $searchSkillPuc
    elif message.content.startswith(commandF(8)):
        pucs = loadPucs()
        msg = ""
        find = message.content.split(" ")
        if (len(find)!=2): embed_msg = error_embed(error="Wrong format")
        else:
            for puc in pucs['data']:
                if find[1].replace("_", " ").lower() in puc[2].lower(): 
                    msg = msg + "\n" + str(puc[0]) + " " + puc[1]
            embed_msg = generic_embed("Pucs found", msg, "", server_default_thumbnail)
        await channel.send(embed=embed_msg)

    # $skill
    elif message.content.startswith(commandF(9)):
        skills = loadSkills()
        find = message.content.split(" ")
        if (len(find)!=2): embed_msg = error_embed(error="Wrong format")
        else:
            msg = ''
            for skill in skills['data']:
                if find[1].lower() == skill[0].lower(): 
                   msg = skill[0] + " : " + skill[1]
            if msg == '': 
                embed_msg = error_embed(error="Skill not found")
            else:
                embed_msg = generic_embed("Skill description", msg, "", server_default_thumbnail)
        await channel.send(embed=embed_msg)
    
    # $strat
    elif message.content.startswith("$strat"):
        strats = loadStrats()
        find = message.content.split(" ")
        find = find[1].split("_")
        find = " ".join(find)
        find = find.upper()
        msg = ''
        for s in strats['data']:
            if s[1].upper() == find:
                for i in s:
                    if i.startswith("http"):
                        await channel.send(embed = generic_embed("", "", i, ""))
                    elif i.upper() == find:
                        continue
                    else:
                        msg = msg + i + "\n"
                await channel.send(embed = generic_embed("", msg, "", server_default_thumbnail))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def loadEmaList4_5():
    f = open("emaList4_5.json")
    jfile = json.load(f)
    return jfile

def loadEmaList1_3():
    f = open("emaList.json")
    jfile = json.load(f)
    db = dict()
    for arc in info:
        db[arc[1]]=[]
    for ema in jfile["data"]:
        db[ema[4]].append(ema)
    return db

def loadPucs():
    f = open("puc.json")
    jfile = json.load(f)
    return jfile

def loadSkills():
    f = open("skills.json")
    jfile = json.load(f)
    return jfile

def loadStrats():
    f = open("strats.json")
    jfile = json.load(f)
    return jfile

def commandF(num, space=True):
    if space == True : return "$" + commands[num][0] + " "
    else : return "$" + commands[num][0]

#client.run(os.getenv('TOKEN'))
client.run("NjA3MjM5ODM3MjY2ODcwMzQ0.XUWxNQ.Bgs7mt0peRYxtNwd41IP0RVY3vA")