# -*- coding: utf-8 -*-

import discord
import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

TOKEN = os.getenv('DISCORD_TOKEN')

def browiki_search(query):
    session = requests.Session()
    #session.get('https://browiki.org/wiki/')

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

def ragnaplace_search(query):
    session = requests.Session()
    #session.get('https://ragnaplace.com/home')

    params = {
        'search': query
    }
    
    response = session.post('https://api.ragnaplace.com/ro/search/top?order=name&server=bro', json=params)
    results = response.json()
    items = []
    monsters = []
    maps = []
    skills = []
    npcs = []
    for i in results['item']['list']:
        items.append('-%s https://ragnaplace.com/bro/item/%s' % (i['name'], i['id']))
    for i in results['monster']['list']:
        monsters.append('-%s https://ragnaplace.com/bro/mob/%s' % (i['name'], i['id']))
    for i in results['skill']['list']:
        skills.append('-%s https://ragnaplace.com/bro/skill/%s' % (i['name'], i['id']['id']))
    for i in results['npc']['list']:
        npcs.append('-%s https://ragnaplace.com/bro/npc/%s' % (i['name'], i['id']))
    for i in results['map']['list']:
        maps.append('-%s https://ragnaplace.com/bro/map/%s' % (i['name'], i['id']))
    return items,monsters,maps,skills,npcs

def irowiki_search(query):
    session = requests.Session()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'db.irowiki.org',
        'Referer': 'http://db.irowiki.org/db/search/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    params = {
        'quick': query
    }
    
    response = session.get('http://db.irowiki.org/db/search/', params=params, headers=headers)
    soup = BeautifulSoup(response.content, features='lxml')
    results = []
    result_table = soup.select('.bgLtTable')[1]
    for link in result_table.select('a'):
        results.append('[%s](http://db.irowiki.org%s)' % (link.text, link['href']))
    return results


help_cmd = re.compile('^!(ajuda|help).*$', re.IGNORECASE)
browiki_cmd = re.compile('^!browiki (.*)$', re.IGNORECASE)
irowiki_cmd = re.compile('^!irowiki (.*)$', re.IGNORECASE)
ragnaplace_cmd = re.compile('^!ragnaplace (.*)$', re.IGNORECASE)
    
client = discord.Client()

@client.event
async def on_message(message):
    try:
        channel = message.channel
        message_content = message.content
        if help_cmd.match(message_content):
            await channel.send('ᕦ(⩾﹏⩽)ᕥ Como posso ajudá-lo? Para fazer buscas nas bases de ragnarok experimente a lista de comandos abaixo.\nLista de comandos\n```\n!browiki <termo>\n!ragnaplace <termo>\n!irowiki <termo>\n!ajuda\n```\nTroque `<termo>` pelo que está buscando. Por exemplo:\n`!browiki Salão de Ymir`')
        if browiki_cmd.match(message_content):
            results = browiki_search(browiki_cmd.sub(r'\1',message_content))
            if len(results) > 0:
                await channel.send('٩(˘◡˘)۶ Encontrei a(s) seguinte(s) página(s):\n%s' % ('\n'.join(results)))
            else:
                await channel.send('(─‿‿─) Não encontrei nada na Browiki sobre o assunto')
        if ragnaplace_cmd.match(message_content):
            items,monsters,maps,skills,npcs = ragnaplace_search(ragnaplace_cmd.sub(r'\1',message_content))
            if len(items) > 0:
                await channel.send('٩(˘◡˘)۶ Encontrei a(s) seguinte(s) página(s):\nItens:\n%s' % ('\n'.join(items)))
            if len(monsters) > 0:
                await channel.send('٩(˘◡˘)۶ Encontrei a(s) seguinte(s) página(s):\nMonstros:\n%s' % ('\n'.join(monsters)))
            if len(maps) > 0:
                await channel.send('٩(˘◡˘)۶ Encontrei a(s) seguinte(s) página(s):\nMapas:\n%s' % ('\n'.join(maps)))
            if len(skills) > 0:
                await channel.send('٩(˘◡˘)۶ Encontrei a(s) seguinte(s) página(s):\nHabilidades:\n%s' % ('\n'.join(skills)))
            if len(npcs) > 0:
                await channel.send('٩(˘◡˘)۶ Encontrei a(s) seguinte(s) página(s):\nNpcs:\n%s' % ('\n'.join(npcs)))
        if irowiki_cmd.match(message_content):
            results = irowiki_search(irowiki_cmd.sub(r'\1',message_content))
            if len(results) > 0:
                message = discord.Embed(title="٩(˘◡˘)۶ Encontrei a(s) seguinte(s) página(s):", description='%s' % (', '.join(results)))
                await channel.send(embed=message)
            else:
                await channel.send('(─‿‿─) Não encontrei nada na irowiki sobre o assunto')
    except Exception as e:
        print(e)


client.run(TOKEN)

