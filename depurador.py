async def update_vip_messages():
    try:
        print(f'Tentando abrir o arquivo em {JSON_FILE_PATH}')
        # Abra e leia o arquivo JSON
        with open(JSON_FILE_PATH, 'r') as file:
            vip_data = json.load(file)
        # Resto do código de atualização da mensagem
    except Exception as e:
        print(f"Erro ao abrir o arquivo JSON: {e}")