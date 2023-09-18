import discord
import asyncio
from discord.ext import commands, tasks
import os
import json

# Crie uma instância do bot e definição do comando
intents = discord.Intents.default()
intents.message_content = True #v2
bot = commands.Bot(command_prefix='?', intents=intents)

# Defina o token do seu bot aqui
TOKEN = 'MTE1MjI4NzkyMjA3OTQxMjMxNQ.GW_yGI.C2-AgtFwRXs2zufqWCcfXozxmLToVDzltKJ6gI'

# Obtenha o caminho completo para o arquivo JSON
JSON_FILE_PATH = os.path.join(os.getcwd(), 'VIPS_FIXO.json')

# ID do canal onde a mensagem será enviada (substitua pelo ID do canal desejado)
channel_id = 1153167482698350592
# ID da mensagem que você deseja atualizar (substitua pelo ID da mensagem desejada)
message_id = 1153196301610135595

# Aviso de status do bot no Terminal        
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print('Bot está online e funcionando corretamente!')

    # Inicie o loop de tarefas auto_update_vip_messages
    auto_update_vip_messages.start()

    await update_vip_message()

# Função para ler o arquivo JSON e atualizar a mensagem
async def update_vip_message():
    try:  # Adicione um bloco try aqui
        # Abra e leia o arquivo JSON
        with open(JSON_FILE_PATH, 'r') as file:
            vip_data = json.load(file)

        # Crie uma mensagem formatada com os dados do arquivo JSON
        message_content = "Lista de VIPS:\n"
        for vip in vip_data:
            message_content += f"ID Steam: {vip['uidSteam']}\n"
            message_content += f"Nome: {vip['nickName']}\n"
            message_content += f"Data Aquisição: {vip['dataAquisicao']}\n"
            message_content += f"Data Expiração: {vip['dataExpiracao']}\n"
            message_content += f"Roupa: {vip['roupaSpawn']}\n"
            message_content += f"Assalto: {vip['armaAssalto']}\n"
            message_content += f"Sniper: {vip['armaSniper']}\n"
            message_content += "-----------------------\n"

        return message_content
    except Exception as e:
        print(f"Erro ao atualizar a mensagem: {e}")
        return None

@tasks.loop(seconds=10)
async def auto_update_vip_messages():
    try:
        channel = bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        message_content = await update_vip_message()

        if message_content:
            await message.edit(content=message_content)
    except Exception as e:
        print(f"Erro ao atualizar a mensagem: {e}")

#Comandos
@bot.command()
async def vip(ctx):
    # Responda com uma mensagem informando sobre o status VIP
    response_message = "Para informações sobre o status VIP, entre em contato com os administradores."
    await ctx.send(response_message)

# Inicie o bot com o token
bot.run(TOKEN)