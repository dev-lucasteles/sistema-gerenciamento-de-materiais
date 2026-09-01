from concurrent.futures import ThreadPoolExecutor
import customtkinter as ctk
from typing import Callable, Any

_pool = ThreadPoolExecutor(max_workers=4)

def rodar_em_background(janela: ctk.CTkBaseClass, tarefa: Callable, callback_sucesso: Callable, callback_erro: Callable = None):
    def wrapper():
        try:
            resultado = tarefa()
            if janela.winfo_exists():
                janela.after(0, lambda: callback_sucesso(resultado))
        except Exception as e:
            if janela.winfo_exists() and callback_erro:
                janela.after(0, lambda: callback_erro(e))
            elif janela.winfo_exists():
                print(f"Erro em background não tratado: {e}")

    _pool.submit(wrapper)