# This example requires the 'message_content' intent.
from keys import BOT_TOKEN, channel_id
import discord
import sqlite3

from discord.ext import tasks

# Conectar ao banco de dados SQLite3
conn = sqlite3.connect('mangas.db')
cursor = conn.cursor()

# Criar a tabela de mangás se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS mangas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')
conn.commit()

class MyClient(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            print('Aconteceu')

        if message.content.startswith('$hello'):
            await message.channel.send(f'oi, {message.author.mention}')
        
        if message.content.startswith('$image'):
            embed = discord.Embed(
            title="meu embed",
            description=f"{message.author.mention}, veja o beniyasha",
            color=discord.Color.blue()
            )
            embed.set_image(url="https://s4.anilist.co/file/anilistcdn/character/large/61407.jpg")
            await message.channel.send(embed=embed)
        
        if message.content.startswith('$add'):
            manga_name = message.content[len('$add '):].strip()
            cursor.execute('INSERT INTO mangas (name) VALUES (?)', (manga_name,))
            conn.commit()
            await message.channel.send(f'O mangá {manga_name} foi adicionado, {message.author.mention}!')
        
        if message.content.startswith('$list'):
            cursor.execute('SELECT name FROM mangas')
            mangas = cursor.fetchall()
            if mangas:
                manga_list = '\n'.join([manga[0] for manga in mangas])
                await message.channel.send(f'Lista de mangás:\n{manga_list}')
            else:
                await message.channel.send('Nenhum mangá encontrado.')
        
        if message.content.startswith('$remove'):
            manga_name = message.content[len('$remove '):].strip()
            cursor.execute('DELETE FROM mangas WHERE name = ?', (manga_name,))
            conn.commit()
            await message.channel.send(f'O mangá {manga_name} foi removido, {message.author.mention}!')
    
    @tasks.loop(minutes=30)
    async def checking(self):
        await self.wait_until_ready()
        channel = self.get_channel(channel_id)
        if channel:
            await channel.send('esse código acontece a cada 30 segundos')
    
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        self.checking.start()

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)

# Fechar a conexão com o banco de dados ao encerrar o programa
conn.close()