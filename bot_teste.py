import discord
import asyncio
from discord.ext import commands, tasks
import json
import os

# Crie uma instância do bot e definição do comando
intents = discord.Intents.default()
intents.message_content = True #v2
bot = commands.Bot(command_prefix='?', intents=intents)

# Defina o token do seu bot aqui
TOKEN = 'MTE1MjI4NzkyMjA3OTQxMjMxNQ.GW_yGI.C2-AgtFwRXs2zufqWCcfXozxmLToVDzltKJ6gI'

# Obtenha o caminho completo para o arquivo JSON
JSON_FILE_PATH = os.path.join(os.getcwd(), 'VIPS_FIXO.json')

# Aviso de status do bot no Terminal        
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print('Bot está online e funcionando corretamente!')

# Função para ler o arquivo JSON e atualizar a mensagem
async def update_vip_message(channel):
    # Abra e leia o arquivo JSON
    with open(JSON_FILE_PATH, 'r') as file:
        vip_data = json.load(file)

    # Crie uma mensagem formatada com os dados do arquivo JSON
    message_content = "Lista de VIPS:\n"
    for entry in vip_data:
        message_content += f"Nome: {entry['nome']}\n"
        message_content += f"Data de Expiração: {entry['data_expiracao']}\n"
        message_content += "-----------------------\n"

    # ID do canal onde a mensagem será enviada (substitua pelo ID do canal desejado)
    channel_id = 1153167482698350592
    # ID da mensagem que você deseja atualizar (substitua pelo ID da mensagem desejada)
    message_id = 1153169851301503127

# Função para criar e atualizar a mensagem
async def update_message():
    message_number = 1
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    
    while True:
        # Atualize a mensagem com o número atual
        await message.edit(content=f'Número atual: {message_number}')
        
        # Aguarde 10 segundos antes da próxima atualização
        await asyncio.sleep(10)
        
        message_number += 1

# Comandos
@bot.command()
async def vip(ctx):
    # Responda com uma mensagem informando sobre o status VIP
    response_message = "Para informações sobre o status VIP, entre em contato com os administradores."
    await ctx.send(response_message)

# Inicie o bot com o token
bot.run(TOKEN)