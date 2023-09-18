import discord
from discord.ext import commands, tasks
import json
import os

# Crie uma instância do bot e definição do comando
intents = discord.Intents.default()
intents.message_content = True  # v2
bot = commands.Bot(command_prefix='?', intents=intents)

# Defina o token do seu bot aqui
TOKEN = 'MTE1MjI4NzkyMjA3OTQxMjMxNQ.GW_yGI.C2-AgtFwRXs2zufqWCcfXozxmLToVDzltKJ6gI'

# Obtenha o caminho completo para o arquivo JSON dos jogadores VIP
JSON_FILE_PATH = os.path.join(os.getcwd(), 'VIPS_FIXO.json')

# Obtenha o caminho completo para o arquivo JSON das mensagens registradas
MESSAGES_FILE_PATH = os.path.join(os.getcwd(), 'mensagens.json')

# ID do canal onde as mensagens serão enviadas (substitua pelo ID do canal desejado)
channel_id = 1153167482698350592

# Função para criar a mensagem formatada com os dados dos jogadores VIP
def create_vip_message(vip_data, max_players=15):
    message_content = ""
    players_count = 0

    for vip in vip_data:
        message_content += f"UID: {vip['uidSteam']}\n"
        message_content += f"Nome: {vip['nickName']}\n"
        message_content += f"Expiração: {vip['dataExpiracao']}\n"
        message_content += f"Roupa: {vip['roupaSpawn']}\n"
        message_content += f"Assalto: {vip['armaAssalto']}\n"
        message_content += f"Sniper: {vip['armaSniper']}\n"
        message_content += "-\n"

        players_count += 1

        if players_count >= max_players:
            break

    return message_content

# Aviso de status do bot no Terminal
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print('Bot está online e funcionando corretamente!')

    # Inicie o loop de tarefas auto_update_vip_messages
    auto_update_vip_messages.start()

    # Execute a função de atualização das mensagens uma vez para começar
    await update_vip_messages()

# Função para ler o arquivo JSON e atualizar as mensagens
async def update_vip_messages():
    try:
        # Abra e leia o arquivo JSON dos jogadores VIP
        with open(JSON_FILE_PATH, 'r') as vip_file:
            vip_data = json.load(vip_file)

        # Obtenha o canal
        channel = bot.get_channel(channel_id)

        # Verifique se o arquivo de mensagens existe
        if os.path.exists(MESSAGES_FILE_PATH):
            # Abra e leia o arquivo JSON das mensagens registradas
            with open(MESSAGES_FILE_PATH, 'r') as messages_file:
                messages_dict = json.load(messages_file)
        else:
            # Se o arquivo de mensagens não existir, crie um dicionário vazio
            messages_dict = {}

        # Verifique se já existem IDs de mensagens registrados
        if channel_id in messages_dict:
            message_id = messages_dict[channel_id]
            message = await channel.fetch_message(message_id)
            message_content = create_vip_message(vip_data)
            await message.edit(content=message_content)
        else:
            # Se não houver IDs de mensagens registrados, crie uma nova mensagem
            message_content = create_vip_message(vip_data)
            message = await channel.send(message_content)
            messages_dict[channel_id] = message.id

            # Salve os IDs das mensagens em "mensagens.json"
            with open(MESSAGES_FILE_PATH, 'w') as messages_file:
                json.dump(messages_dict, messages_file)

    except Exception as e:
        print(f"Erro ao atualizar as mensagens: {e}")

@tasks.loop(seconds=10)
async def auto_update_vip_messages():
    await update_vip_messages()

# Comandos
@bot.command()
async def vip(ctx):
    response_message = "Para informações sobre o status VIP, entre em contato com os administradores."
    await ctx.send(response_message)

# Inicie o bot com o token
bot.run(TOKEN)