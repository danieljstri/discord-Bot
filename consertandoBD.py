import sqlite3

# Conectar ao banco de dados SQLite (substitua 'seu_banco_de_dados.db' pelo nome do seu banco de dados)
conexao = sqlite3.connect('database.db')

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

# Nome da tabela que você deseja visualizar
nome_tabela = 'mangas'  # Substitua pelo nome da sua tabela

# Consulta SQL para selecionar todos os dados da tabela
cursor.execute(f"DELETE FROM {nome_tabela}")

# Obter todos os registros da tabela
dados = cursor.fetchall()

# Exibir os dados
print(f'Dados na tabela {nome_tabela}:')
for linha in dados:
    print(linha)

# Fechar a conexão com o banco de dados
conexao.close()
