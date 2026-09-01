from dataclasses import dataclass
from typing import Optional

@dataclass
class Monitor:
    id_monitor: int
    nome: str
    ativo: bool = True

@dataclass
class Material:
    id_material: int
    nome: str
    quantidade: int
    observacoes: Optional[str] = None
    ativo: bool = True

@dataclass
class ItemChecklist:
    id_material: int
    nome_material: str
    qtd_esperada: int
    qtd_encontrada: int
    observacao: str
    quarto: str