import sqlite3
from typing import List, Tuple

class HistoricoRepository:
    def __init__(self, conexao: sqlite3.Connection):
        self.conn = conexao

    def listar_historico_completo(self) -> List[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT h.id_log, m.nome, h.data_hora, h.acao, h.detalhes 
            FROM historico_movimentacoes h
            LEFT JOIN monitor m ON h.id_monitor = m.id_monitor
            ORDER BY h.id_log DESC
        ''')
        return cursor.fetchall()