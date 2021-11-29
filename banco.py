#importando o sqlite
import sqlite3

# conectando...
conn = sqlite3.connect('efn.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
cursor.execute("""
CREATE TABLE IF NOT EXISTS estudantes (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        cpf     TEXT NOT NULL,
        email TEXT NOT NULL,
        fone TEXT,
        cidade TEXT,
        uf TEXT NOT NULL,
        curso TEXT,
        turma TEXT
);
""")

print('Tabela criada com sucesso.')
# desconectando...
conn.close()