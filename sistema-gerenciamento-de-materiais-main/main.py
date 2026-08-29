import customtkinter as ctk
from backend_gerenciador import BancoDeDados

from telas.janela_monitor import JanelaMonitor
from telas.janela_material import JanelaMaterial
from telas.janela_movimentacoes import JanelaMovimentacoes
from telas.janela_checklist import JanelaChecklist
from telas.janela_historico_relatorio import JanelaHistorico, JanelaRelatorio

# Configuração global de aparência para Dark Mode
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gerenciamento de Materiais")
        # Fundo da janela bem escuro (quase preto) para dar profundidade
        self.configure(fg_color="#121212") 
        self.sistema = BancoDeDados()
        
        self._configurar_geometria()
        self.protocol("WM_DELETE_WINDOW", self.fechar_sistema)
        self._construir_menu()

    def _configurar_geometria(self):
        largura_janela = 500
        altura_janela = 680
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        self.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    def _construir_menu(self):
        # Container principal em um tom de cinza escuro para destacar do fundo preto
        self.frame_principal = ctk.CTkFrame(self, corner_radius=20, fg_color="#1e1e1e")
        self.frame_principal.pack(pady=40, padx=40, fill="both", expand=True)

        # Título com cor clara para alto contraste
        self.label_titulo = ctk.CTkLabel(self.frame_principal, text="📦 Menu Principal", 
                                        font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), 
                                        text_color="#e0e0e0")
        self.label_titulo.pack(pady=(30, 5))
        
        self.label_sub = ctk.CTkLabel(self.frame_principal, text="Gerenciamento de Estoque", 
                                    font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#888888")
        self.label_sub.pack(pady=(0, 25))

        # Configuração padrão dos botões para Dark Mode
        btn_kwargs = {
            "width": 300,
            "height": 45,
            "corner_radius": 8,
            "font": ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            "anchor": "center", # <-- Alterado para centralizar o texto
            "border_width": 1,         
            "border_color": "#444444"  # Borda visível para delimitar a caixa
        }

        # Lista de botões
        botoes = [
            ("  Gerenciar Monitores", JanelaMonitor),
            ("  Gerenciar Materiais", JanelaMaterial),
            ("  Registrar Entradas e Perdas", JanelaMovimentacoes),
            ("  Realizar Check-list Diário", JanelaChecklist),
            ("  Gerar Relatório de Estoque", JanelaRelatorio),
            ("  Ver Histórico de Ações", JanelaHistorico)
        ]

        for texto, classe in botoes:
            btn = ctk.CTkButton(self.frame_principal, text=texto, 
                                command=lambda c=classe: self.abrir_tela(c),
                                fg_color="#2a2a2a",      # Fundo do botão mais claro que o quadro principal
                                text_color="#ffffff",    # Texto totalmente branco
                                hover_color="#3a3a3a",   # Brilho sutil ao passar o mouse
                                **btn_kwargs)
            btn.pack(pady=8)

        # Botão de Sair mantendo o destaque em vermelho, ajustado para combinar com fundo escuro
        btn_sair = ctk.CTkButton(self.frame_principal, text="Sair do Sistema", 
                                 command=self.fechar_sistema, 
                                 fg_color="#c0392b", hover_color="#a53125", 
                                 text_color="#ffffff", width=300, height=45, 
                                 corner_radius=8, font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"))
        btn_sair.pack(pady=(30, 20))

    def abrir_tela(self, ClasseDaJanela):
        ClasseDaJanela(self, self.sistema)

    def fechar_sistema(self):
        try:
            self.sistema.fechar_conexao()
        except Exception:
            pass 
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()