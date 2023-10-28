linha = 'State: S (sleeping)'

# Use split(':') para dividir a string na primeira ocorrência de ":"
parts = linha.split(':', 1)

# Verifique se há dois elementos após a divisão
if len(parts) == 2:
    chave = parts[0].strip()  # Remove espaços em branco do início e fim
    valor = parts[1].strip()  # Remove espaços em branco do início e fim

    print(f'Chave: {chave}')
    print(f'Valor: {valor}')
else:
    print('Formato de linha incorreto')
