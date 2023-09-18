import discord
import asyncio
from discord.ext import commands, tasks
import os
import json

# Crie uma instância do bot e definição do comando
intents = discord.Intents.default()
intents.message_content = True  # v2
bot = commands.Bot(command_prefix='?', intents=intents)

# Defina o token do seu bot aqui
TOKEN = 'MTE1MjI4NzkyMjA3OTQxMjMxNQ.GW_yGI.C2-AgtFwRXs2zufqWCcfXozxmLToVDzltKJ6gI'

# Obtenha o caminho completo para o arquivo JSON
JSON_FILE_PATH = os.path.join(os.getcwd(), 'VIPS_FIXO.json')

# ID do canal onde a mensagem será enviada (substitua pelo ID do canal desejado)
channel_id = 1153167482698350592

# Função para criar mensagens formatadas com os dados dos jogadores
def create_vip_message(vip_data):
    message_content = "Lista de VIPS:\n"
    for vip in vip_data:
        message_content += f"UID: {vip['uidSteam']}\n"
        message_content += f"Nome: {vip['nickName']}\n"
        message_content += f"Expiração: {vip['dataExpiracao']}\n"
        message_content += f"Roupa: {vip['roupaSpawn']}\n"
        message_content += f"Assalto: {vip['armaAssalto']}\n"
        message_content += f"Sniper: {vip['armaSniper']}\n"
        message_content += "-\n"
    return message_content

# Aviso de status do bot no Terminal
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print('Bot está online e funcionando corretamente!')

    # Inicie o loop de tarefas auto_update_vip_messages
    auto_update_vip_messages.start()

    # Execute a função de atualização da mensagem uma vez para começar
    await update_vip_message()

# Função para ler o arquivo JSON e atualizar a mensagem
async def update_vip_message():
    try:
        # Abra e leia o arquivo JSON
        with open(JSON_FILE_PATH, 'r') as file:
            vip_data = json.load(file)

        # Divida a lista de jogadores em grupos de até 15 jogadores
        player_groups = [vip_data[i:i+15] for i in range(0, len(vip_data), 15)]

        # Obtenha o canal
        channel = bot.get_channel(channel_id)

        for group in player_groups:
            message_content = create_vip_message(group)
            await channel.send(message_content)

    except Exception as e:
        print(f"Erro ao atualizar a mensagem: {e}")

@tasks.loop(seconds=10)
async def auto_update_vip_messages():
    await update_vip_message()

# Comandos
@bot.command()
async def vip(ctx):
    response_message = "Para informações sobre o status VIP, entre em contato com os administradores."
    await ctx.send(response_message)

# Inicie o bot com o token
bot.run(TOKEN)