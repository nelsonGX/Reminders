import discord
import datetime
import aiofiles
import json

# configs
save_path = "reminders.json"
token = ""

client = discord.Client(intents=discord.Intents.all())

"""
This is a Reminder APP in discord.
It have functions to add, delete and list reminders, into JSON database.
"""

async def add_reminder(content, date):
    async with aiofiles.open(save_path, mode='r') as f:
        reminders = json.loads(await f.read())

    # generate a numberic ID here
    id = len(reminders) + 1    

    reminders.append({str(id): {"content": content, "date": date}})
    async with aiofiles.open(save_path, mode='w') as f:
        await f.write(json.dumps(reminders))
    return True

async def delete_reminder(id):
    async with aiofiles.open(save_path, mode='r') as f:
        reminders = json.loads(await f.read())

    for reminder in reminders:
        if id in reminder:
            reminders.remove(reminder)
            break

    async with aiofiles.open(save_path, mode='w') as f:
        await f.write(json.dumps(reminders))

    return True

async def list_reminders():
    async with aiofiles.open(save_path, mode='r') as f:
        reminders = json.loads(await f.read())

    return reminders

async def translate_date_to_unix_timestamp(date):
    # format: 2021-09-01 12:00
    if "-" in date:
        return int(datetime.strptime(date, "%Y-%m-%d %H:%M").timestamp())
    # format: 2021/9/1 12:00
    elif "/" in date:
        return int(datetime.strptime(date, "%Y/%m/%d %H:%M").timestamp())
    else:
        return False

async def command(tmp):
    command = tmp.split(" ")[0]
    content = tmp.split("")[1]
    date = await translate_date_to_unix_timestamp(tmp.split(" ")[2])
    if not date:
        return ""
    if command == "add":
        await add_reminder(content)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f"<@{str(client.user.id)}>"):
        reply = await command(str(message.content))
        await message.reply(reply)

client.run(token)