import discord, aiohttp, os, asyncio
from discord.ext import tasks

client=discord.Client()

@tasks.loop(minutes=1)
async def status():
    headers={'User-Agent':'Mozilla/5.0 (Linux; Android 10; LM-X525 Build/QKQ1.200531.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692.87 Mobile Safari/537.36'}
    async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://curseofaros.com/assets/worlds.json') as r:
                json=await r.json()
    a=0
    for i in json:
       a+=int(i['players'])
    await client.change_presence(activity = discord.Game(name=f"with {a} other(s)"))

@client.event
async def on_ready():
    print(f"Connected to {client.user}")
    temp_var=""
    spacesreq=None
    headers={'User-Agent':'Mozilla/5.0 (Linux; Android 10; LM-X525 Build/QKQ1.200531.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692.87 Mobile Safari/537.36'}
    if not os.path.isfile('./msgid.txt'):
        open('msgid.txt', 'a').close()
        msgid=None
    else:
        with open('msgid.txt') as e:
            msgid=int(e.read().strip())
    channel=await client.fetch_channel(933621354173980682)
    try:
        msg=await channel.fetch_message(msgid)
    except discord.NotFound:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://curseofaros.com/assets/worlds.json') as r:
                json=await r.json()
                for i in json:
                    spacesreq=17-len(i['name'])
                    temp_var+=f"{i['name']}:{' '*spacesreq}{i['players']} players\n"
        embed=discord.Embed(title='__Curse Of Aros Worlds__', description=f"```\n{temp_var}```", colour=discord.Color.random())
        msg=await channel.send(embed=embed)
        with open('msgid.txt', 'w+') as e:
            e.write(str(msg.id))
    status.start()
    while True:
        temp_var=""
        spacesreq=None
        embed=None
        try:
            await channel.fetch_message(msg.id)
        except discord.NotFound:
            msg=None
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://curseofaros.com/assets/worlds.json') as r:
                json=await r.json()
                for i in json:
                    spacesreq=17-len(i['name'])
                    temp_var+=f"{i['name']}:{' '*spacesreq}{i['players']} players\n"
        embed=discord.Embed(title='__Curse Of Aros Worlds__', description=f"```\n{temp_var}```", colour=discord.Color.random())
        if msg is None:
            msg=await channel.send(embed=embed)
            with open('msgid.txt', 'w+') as e:
                e.write(str(msg.id))
        else:
            await msg.edit(embed=embed)
        await asyncio.sleep(4)

client.run(os.environ['token'])
