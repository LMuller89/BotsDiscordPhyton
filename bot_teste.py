import discord
from discord.ext import commands, tasks
import json

# Crie uma instância do bot e definição do comando
intents = discord.Intents.default()
intents.message_content = True #v2
bot = commands.Bot(command_prefix='?', intents=intents)

# Defina o token do seu bot aqui
TOKEN = 'MTE1MjI4NzkyMjA3OTQxMjMxNQ.GW_yGI.C2-AgtFwRXs2zufqWCcfXozxmLToVDzltKJ6gI'

#Aviso de status do bot no Terminal        
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print('Bot está online e funcionando corretamente!')

# Função para ler o arquivo JSON e atualizar a mensagem
async def update_vip_message(channel):
    # Abra e leia o arquivo JSON
    with open('VIPS_FIXO.json', 'r') as file:
        vip_data = json.load(file)

    # Crie uma mensagem formatada com os dados do arquivo JSON
    message_content = "Lista de VIPS:\n"
    for entry in vip_data:
        message_content += f"Nome: {entry['nome']}\n"
        message_content += f"Data de Expiração: {entry['data_expiracao']}\n"
        message_content += "-----------------------\n"

    # Tente encontrar e atualizar a mensagem existente (substitua 'MESSAGE_ID' pelo ID da mensagem)
    message_id = 1153159334629494886  # Substitua pelo ID da mensagem
    try:
        message = await channel.fetch_message(message_id)
        await message.edit(content=message_content)
    except discord.NotFound:
        # Se a mensagem não for encontrada, crie uma nova mensagem
        message = await channel.send(message_content)

# Use um loop para atualizar a mensagem a cada 1 minuto (60 segundos)
@tasks.loop(seconds=60)
async def auto_update_vip_message():
    # Obtenha o canal de texto onde deseja atualizar a mensagem (substitua 'CHANNEL_ID' pelo ID do canal)
    channel_id = 1152294485359870015  # Substitua pelo ID do canal
    channel = bot.get_channel(channel_id)
    
    if channel:
        await update_vip_message(channel)

#Comandos
@bot.command()
async def vip(ctx):
    # Responda com uma mensagem informando sobre o status VIP
    response_message = "Para informações sobre o status VIP, entre em contato com os administradores."
    await ctx.send(response_message)

# Inicie o bot com o token
bot.run(TOKEN)