import sqlite3
from contextlib import contextmanager
from config import DB_PATH

class GerenciadorConexao:
    def __init__(self, caminho_banco: str = str(DB_PATH)):
        self.caminho_banco = caminho_banco
        self._inicializar_esquema()
        self._otimizar_banco()

    def _otimizar_banco(self):
        with sqlite3.connect(self.caminho_banco) as conn:
            conn.execute("PRAGMA journal_mode = WAL;")

    def _inicializar_esquema(self):
        with sqlite3.connect(self.caminho_banco) as conn:
            with conn:
                conn.execute('''
                CREATE TABLE IF NOT EXISTS monitor (
                    id_monitor INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nome TEXT NOT NULL,
                    ativo INTEGER DEFAULT 1
                )''')
                conn.execute('''
                CREATE TABLE IF NOT EXISTS material (
                    id_material INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    quantidade_material INT,
                    observacoes TEXT,
                    ativo INTEGER DEFAULT 1
                )''')
                conn.execute('''
                CREATE TABLE IF NOT EXISTS entrada (
                    id_entrada INTEGER PRIMARY KEY AUTOINCREMENT,
                    entrada DATE,
                    quantidade_entrada INT,
                    id_material INT,
                    FOREIGN KEY (id_material) REFERENCES material(id_material)
                )''')
                conn.execute('''
                CREATE TABLE IF NOT EXISTS danos (
                    id_danos INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_danos DATE,
                    quantidade_danos INT,
                    id_material INT,
                    FOREIGN KEY (id_material) REFERENCES material(id_material)
                )''')
                conn.execute('''
                CREATE TABLE IF NOT EXISTS historico_movimentacoes (
                    id_log INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_monitor INTEGER,
                    data_hora DATETIME,
                    acao TEXT NOT NULL,
                    detalhes TEXT,
                    FOREIGN KEY (id_monitor) REFERENCES monitor(id_monitor)
                )''')

    @contextmanager
    def obter_conexao(self):
        conn = sqlite3.connect(self.caminho_banco, timeout=5.0)
        conn.execute("PRAGMA busy_timeout = 5000;")
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
        finally:
            conn.close()