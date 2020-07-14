import discord
import os
import random
from app_func_n_class import *
from discord.ext import commands

# -- Data --
user_data = []

BOT_PREFIX = ("?", "!")
TOKEN = 'XXXXXXXXX'

bot = commands.Bot(command_prefix=BOT_PREFIX)


# -- Function --
def get_user(u_list, name):
    for user in u_list:
        if user.name == name:
            return user


# -- Commands --
@bot.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond",
                aliases=['eight_ball', 'eightball', '8-ball'])
async def eight_ball(ctx):
    possible_response = [
        'Thas a hella nah, dude',
        'Hmm, maybe not',
        'Honestly, I dunno',
        'WEll, maybe',
        'Absotootly',
        'dew eet'
    ]

    print('Eight ball cmd')
    await ctx.channel.send(random.choice(possible_response) + ", " + ctx.message.author.mention)


@bot.command(name='reset-all')
async def reset(ctx):
    # Deletes all messages in all channels
    channels = ['todo', 'prize-list', 'done-todo', 'done-prize-list', 'chat']
    for ch in bot.guilds[0].channels:
        for x in channels:
            if ch.name == x:
                channels.remove(x)
                channel = ch
                await channel.purge(limit=420)

    for user in user_data:
        user.todo = []
        user.done_todo = []
        user.prize = []
        user.done_prize = []

        user.exp = 0

    save_data('UserData.txt', user_data)


@bot.command(name='add-todos')
async def td_add(ctx, todos):
    print('Add todo cmd')
    asker = ctx.author.name

    to_add = parse_message(todos)

    # Adds todos to user
    user = get_user(user_data, asker)
    for x in to_add:
        user.todo.append(x)

    user.todo.sort(key=lambda y: y.exp)

    # Delete all messages in channel
    channel = ''
    for ch in bot.guilds[0].channels:
        if ch.name == 'todo':
            print('Todo channel found')
            channel = ch

    await channel.purge(limit=420)

    # Prints all tasks for each user
    for user in user_data:
        await channel.send(user.name + ' needs to do: ')
        if len(user.todo) == 0:
            await channel.send(' - No todos left!  :0')
        else:
            for todo in user.todo:
                await channel.send(' - ' + todo.text)


@bot.command(name='add-prizes')
async def pr_add(ctx, prizes):
    print('Add prizes cmd')
    asker = ctx.author.name

    to_add = parse_message(prizes)

    # Adds prize list to user
    user = get_user(user_data, asker)
    for x in to_add:
        user.prize.append(x)

    user.prize.sort(key=lambda y: y.exp)

    # Delete all messages in channel
    channel = ''
    for ch in bot.guilds[0].channels:
        if ch.name == 'prize-list':
            print('Prize list channel found')
            channel = ch

    await channel.purge(limit=420)

    # Prints all tasks for each user
    for user in user_data:
        await channel.send(user.name + ' prize goals: ')
        if len(user.prize) == 0:
            await channel.send(' - No prizes  :\'(')
        else:
            for prize in user.prize:
                await channel.send(' - ' + prize.text)


@bot.command(name='stats')
async def get_exp(ctx):
    # Display member's current exp owned
    print('Get exp stats cmd')

    global user_data
    asker = ctx.author.name

    for user in user_data:
        if asker == user.name:
            exp = user.exp
            await ctx.channel.send(ctx.message.author.mention + ' has ' + str(exp) + ' exp')
            break


# -- Events --

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')

    global user_data
    server_user = []

    # -- USER --
    # Load user data
    if os.path.exists('./UserData.txt'):
        # Read user data text file
        load_data('UserData.txt', user_data)

    # Read member list in discord
    for member in bot.guilds[0].members:
        user = member.name
        if user != 'alien catte':
            server_user.append(user)

    # Check if there's new user, append new ones
    if len(user_data) < len(server_user):

        for s_user in server_user:
            user_exist_in_text = False

            for t_user in user_data:
                if s_user == t_user:
                    user_exist_in_text = True

            if not user_exist_in_text:
                print('New user: ' + s_user)
                temp = User(s_user, 0)
                user_data.append(temp)

        user_data.sort(key=lambda x: x.name)

        # Save to text file
        save_data('UserData.txt', user_data)

    # -- LISTS --

    # -- TodoChannel --

    channel = ''
    for ch in bot.guilds[0].channels:

        if ch.name == 'todo':
            print('Todo channel found')
            channel = ch

    history = await channel.history(limit=420).flatten()

    # Convert to list of strings and flip order
    history.reverse()
    raw_messages = []

    for x in history:
        raw_messages.append(x.clean_content)

    user = ''
    for y in raw_messages:

        if y.find(' needs to do:') != -1:
            idx = y.find(' needs to do:')
            user = get_user(user_data, y[0:idx])

        elif y.find(')') != -1:
            i = y.find(')')
            text = y[2:i+1]

            j = y.find('(')
            points = int(y[j + 1:-1])
            user.todo.append(Bullet(text, points))

    print(' Loaded from todo channel ')

    # -- PrizeListChannel --

    for ch in bot.guilds[0].channels:

        if ch.name == 'prize-list':
            print('Prize-list channel found')
            channel = ch

    history = await channel.history(limit=420).flatten()

    # Convert to list of strings and flip order
    history.reverse()
    raw_messages = []

    for x in history:
        raw_messages.append(x.clean_content)

    user = ''
    for y in raw_messages:

        if y.find(' prize goals:') != -1:
            idx = y.find(' prize goals:')
            user = get_user(user_data, y[0:idx])

        elif y.find(')') != -1:
            i = y.find(')')
            j = y.find('(')

            if y[2:4] == '**':
                text = y[4:i+1]
                points = int(y[j + 1:-3])
            elif y[2] == '*':
                text = y[3:i+1]
                points = int(y[j + 1:-2])
            else:
                text = y[2:i+1]
                points = int(y[j + 1:-1])

            user.prize.append(Bullet(text, points))

    print(' Loaded from prize-list channel ')

    # -- DoneTodoChannel --

    for ch in bot.guilds[0].channels:

        if ch.name == 'done-todo':
            print('Done-todo channel found')
            channel = ch

    history = await channel.history(limit=420).flatten()

    # Convert to list of strings and flip order
    history.reverse()
    raw_messages = []

    for x in history:
        raw_messages.append(x.clean_content)

    user = ''
    for y in raw_messages:

        if y.find(' done todos:') != -1:
            idx = y.find(' done todos:')
            user = get_user(user_data, y[0:idx])

        elif y.find(')') != -1:
            i = y.find(')')
            user.done_todo.append(y[2:i+1])

    print(' Loaded from done-todo channel ')

    # -- DonePrizeListChannel --

    for ch in bot.guilds[0].channels:

        if ch.name == 'done-prize-list':
            print('Done-prize-list channel found')
            channel = ch

    history = await channel.history(limit=420).flatten()

    # Convert to list of strings and flip order
    history.reverse()
    raw_messages = []

    for x in history:
        raw_messages.append(x.clean_content)

    user = ''
    for y in raw_messages:

        if y.find(' done prizes:') != -1:
            idx = y.find(' done prizes:')
            user = get_user(user_data, y[0:idx])

        elif y.find(')') != -1:
            i = y.find(')')

            if y[2:4] == '**':
                user.done_prize.append(y[4:i+1])
            elif y[2] == '*':
                user.done_prize.append(y[3:i+1])
            else:
                user.done_prize.append(y[2:i + 1])

    print(' Loaded from done-prize-list channel ')


@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    message = payload.message_id

    # Get user
    name = payload.member.name
    user = get_user(user_data, name)

    # Get message
    msg = await channel.fetch_message(message)
    msg_text = msg.content[2:]

    if payload.emoji.name == 'tododone':

        if channel.name == 'todo':

            # Move todos from list to done list
            idx = -1
            for t in user.todo:
                idx += 1
                if t.text == msg_text:
                    break

            user.todo.pop(idx)
            user.done_todo.append(msg_text)

            print('Marked todo as done!')

            # Add exp to user
            i = msg_text.find('(')
            points = int(msg_text[i+1: -1])
            user.exp += points

            # Save to text file
            save_data('UserData.txt', user_data)

            # Exp checking
            for p in user.prize:
                if user.exp >= p.exp:

                    # Bolds text for highlight
                    if p.text[0:2] != '**':
                        p.text = '*' + p.text + '*'

                    # Mention to everyone the prize
                    for ch in bot.guilds[0].channels:
                        if ch.name == 'chat':
                            # Alerts in chat what prizes has been met
                            await ch.send('@everyone ' + user.name + ' reached prize: ' + p.text + ' ! :D')

    elif payload.emoji.name == 'deleteitem':

        if channel.name == 'todo':

            # Remove out of list
            idx = -1
            for t in user.todo:
                idx += 1
                if t.text == msg_text:
                    break

            user.todo.pop(idx)

        elif channel.name == 'prize-list':

            # Remove out of list
            idx = -1
            for t in user.prize:
                idx += 1
                if t.text == msg_text:
                    break

            user.prize.pop(idx)

        print('Item has been deleted!')

    elif payload.emoji.name == 'prizedone':

        if channel.name == 'prize-list':
            # Checks if prizes can be claimed
            j = msg_text.find('(')

            if msg_text[0:2] == '**':
                points = int(msg_text[j + 1:-3])
            else:
                points = int(msg_text[j + 1:-2])

            if points > user.exp:
                for ch in bot.guilds[0].channels:
                    if ch.name == 'chat':
                        # Alerts in chat what prizes has been met
                        await ch.send('@' + user.name + ' Cannot claim prize, not enough exp')

            else:
                # Move prizes from list to done list
                idx = -1
                for t in user.prize:
                    idx += 1
                    if t.text == msg_text:
                        break

                user.prize.pop(idx)
                user.done_prize.append(msg_text)

        print('Marked prize as done!')

    # Updates A L L the channels (cause heck, dude)

    # -- TodoChannel --
    channel = ''
    for ch in bot.guilds[0].channels:

        if ch.name == 'todo':
            print('Todo channel found')
            channel = ch

    await channel.purge(limit=420)

    for user in user_data:

        await channel.send(user.name + ' needs to do: ')

        if len(user.todo) == 0:
            await channel.send(' - No todos left!  :0')
        else:
            for todo in user.todo:
                await channel.send(' - ' + todo.text)

    # -- DoneTodoChannel --
    for ch in bot.guilds[0].channels:

        if ch.name == 'done-todo':
            print('Done todo channel found')
            channel = ch

    await channel.purge(limit=420)

    # Prints all tasks for each user
    for user in user_data:

        await channel.send(user.name + ' done todos: ')

        if len(user.done_todo) == 0:
            await channel.send(' - None! Get workin\' beep meow!  >:0')
        else:
            for done_td in user.done_todo:
                await channel.send(' - ' + done_td)

    # -- PrizeListChannel --
    for ch in bot.guilds[0].channels:

        if ch.name == 'prize-list':
            print('Prize list channel found')
            channel = ch

    await channel.purge(limit=420)

    # Prints all tasks for each user
    for user in user_data:
        await channel.send(user.name + ' prize goals: ')
        if len(user.prize) == 0:
            await channel.send(' - No prizes  T^T')
        else:
            for prize in user.prize:
                await channel.send(' - ' + prize.text)

    # -- DonePrizeListChannel --
    for ch in bot.guilds[0].channels:

        if ch.name == 'done-prize-list':
            print('Done prize list channel found')
            channel = ch

    await channel.purge(limit=420)

    # Prints all tasks for each user
    for user in user_data:
        await channel.send(user.name + ' done prizes: ')
        if len(user.done_prize) == 0:
            await channel.send(' - Nothin\', chat this is so sad  :\'(')
        else:
            for done_pr in user.done_prize:
                await channel.send(' - ' + done_pr)


bot.run(TOKEN)


'''
# CODEYARD
@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
'''
