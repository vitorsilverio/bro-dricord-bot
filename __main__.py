# -*- coding: utf-8 -*-

import discord
import os
import re
import requests
from dotenv import load_dotenv

TOKEN = os.getenv('DISCORD_TOKEN')

def browiki_search(query):
    print(query)
    session = requests.Session()
    session.get('https://browiki.org/wiki/')

    params = {
        'action': 'opensearch',
        'format': 'json',
        'formatversion': 2,
        'search': query,
        'namespace': 0,
        'suggest': 'true',
        'limit': 10
    }
    
    response = session.get('https://browiki.org/api.php', params=params)

    return response.json()[3]

browiki_cmd = re.compile('^!browiki (.*)$', re.IGNORECASE)
    
client = discord.Client()

@client.event
async def on_message(message):
    channel = message.channel
    message_content = message.content
    if browiki_cmd.match(message_content):
        results = browiki_search(browiki_cmd.sub(r'\1',message_content))
        if len(results) > 0:
            await channel.send('٩(˘◡˘)۶ Encontrei a(s) seguinte(s) página(s):\n%s' % ('\n'.join(results)))
        else:
            await channel.send('(─‿‿─) Não encontrei nada na Browiki sobre o assunto')


client.run(TOKEN)

