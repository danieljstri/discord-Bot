# This example requires the 'message_content' intent.
from keys import BOT_TOKEN, channel_id
import discord
import sqlite3
from utils import get_new_chapters, get_manga, escolhe_manga

from discord.ext import tasks

# Conectar ao banco de dados SQLite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Criar a tabela de mangás se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS mangas (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL,
    manga_name TEXT NOT NULL,
    manga_id TEXT NOT NULL
)
''')
conn.commit()

class MyClient(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            print('Aconteceu')

        if message.content.startswith('$hello'):
            await message.channel.send(f'oi, {message.author.mention}')
        
        if message.content.startswith('$help'):
            await message.channel.send('''Comandos disponíveis:\n$hello - O bot te dá oi :)\n$add - Adiciona um mangá à sua lista\n$list - Lista todos os mangás que você adicionou\n$remove - Remove um mangá da sua lista\n$help - Mostra todos os comandos disponíveis''')
        
        if message.content.startswith('$add'):
            user_manga = message.content[len('$add '):].strip()
            response = escolhe_manga(user_manga)
            await message.channel.send(response)
            user_manga_number = await self.wait_for('message', check=lambda m: m.author == message.author and m.content.isdigit())
            user_manga_number = int(user_manga_number.content)
            manga_name = get_manga(user_manga)[user_manga_number]['attributes']['title']['en']
            manga_id = str(get_manga(user_manga)[user_manga_number]['id'])
            username = message.author.name
            cursor.execute('INSERT INTO mangas (username, manga_name, manga_id) VALUES (?, ?, ?)', (username, manga_name, manga_id))
            conn.commit()
            await message.channel.send(f'O mangá {manga_name} foi adicionado, {message.author.mention}!')

        if message.content.startswith('$list'):
            username = message.author.name
            cursor.execute('SELECT * FROM mangas WHERE username = ?', (username,))
            mangas = cursor.fetchall()
            print(mangas)
            if mangas:
                manga_list = '\n'.join([manga[2] for manga in mangas])
                await message.channel.send(f'Lista de mangás:\n {manga_list}')
            else:
                await message.channel.send('Nenhum mangá encontrado.')
        
        if message.content.startswith('$remove'):
            manga_name = message.content[len('$remove '):].strip()
            cursor.execute('DELETE FROM mangas WHERE manga_name = ?', (manga_name,))
            conn.commit()
            await message.channel.send(f'O mangá {manga_name} foi removido, {message.author.mention}!')
    
    @tasks.loop(hours=12)
    async def checking_chapter(self):
        cursor.execute('SELECT * FROM mangas')
        ids = cursor.fetchall() 
        for item in ids:
            print(item[3])
            manga = get_new_chapters(item[3].strip())
            if manga['have_new']:
                channel = self.get_channel(channel_id)
                await channel.send(f'Novo capítulo lançado! {manga["chapter_url"]}')
            else:
                channel = self.get_channel(channel_id)
                await channel.send(f'Nenhum novo capítulo de {item[2]} lançado.')
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        self.checking_chapter.start()

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(BOT_TOKEN)

# Fechar a conexão com o banco de dados ao encerrar o programa
conn.close()
