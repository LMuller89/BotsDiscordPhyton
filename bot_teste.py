import discord
from discord.ext import commands

# Crie uma instância do bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Defina o token do seu bot aqui
TOKEN = 'MTE1MjI4NzkyMjA3OTQxMjMxNQ.G4kKk0.6-NWC2bveprJQATzczQ3BuEGYhp0wKRmewQNJE'

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command()
async def VIP(ctx):
    # Responda com uma mensagem informando sobre o status VIP
    response_message = "Para informações sobre o status VIP, entre em contato com os administradores."
    await ctx.send(response_message)

# Inicie o bot com o token
bot.run(TOKEN)