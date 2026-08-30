import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
import os
from servico_checklist import obter_area_de_trabalho

class JanelaHistorico(ctk.CTkToplevel):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema
        self.title("Histórico de Movimentações")
        self.geometry("750x450")
        self.grab_set()

        colunas = ("ID", "Monitor", "Data", "Ação", "Detalhes")
        
        ctk.CTkLabel(self, text="🕒 Histórico de Movimentações", font=("Segoe UI", 20, "bold"), text_color="#e0e0e0").pack(pady=(15, 10))
        
        frame_tabela = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Estilo da tabela adaptado para Dark Mode
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#2a2a2a", foreground="#ffffff", relief="flat", borderwidth=0)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=35, background="#1e1e1e", fieldbackground="#1e1e1e", foreground="#e0e0e0", borderwidth=0)
        style.map("Treeview", background=[('selected', '#3498db')])

        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        scrollbar = ctk.CTkScrollbar(frame_tabela, command=self.tree.yview)
        scrollbar.pack(side="right", fill="y", pady=5, padx=5)
        
        self.tree.configure(yscrollcommand=scrollbar.set)
        tamanhos_colunas = {"ID": 50, "Monitor": 120, "Data": 150, "Ação": 130, "Detalhes": 250}
        
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=tamanhos_colunas[col], anchor="w")
            
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        self.carregar_historico()

    def carregar_historico(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, log in enumerate(self.sistema.listar_historico()):
            tag = 'par' if i % 2 == 0 else 'impar'
            self.tree.insert("", "end", values=log, tags=(tag,))
            
        self.tree.tag_configure('par', background='#222222')
        self.tree.tag_configure('impar', background='#1e1e1e')


class JanelaRelatorio(ctk.CTkToplevel):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema
        self.title("Gerar Relatório")
        self.geometry("380x250")
        self.transient(master)
        self.grab_set()

        try:
            monitores_db = self.sistema.listar_monitores()
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=self)
            self.destroy()
            return
        
        if not monitores_db:
            messagebox.showwarning("Aviso", "Cadastre um monitor primeiro!", parent=self)
            self.destroy()
            return

        self.lista_monitores = [f"{linha[0]} - {linha[1]}" for linha in monitores_db]

        ctk.CTkLabel(self, text="📄 Quem está gerando o relatório?", font=("Segoe UI", 15, "bold"), text_color="#e0e0e0").pack(pady=(25, 15))
        
        self.combo_monitores = ctk.CTkComboBox(self, values=self.lista_monitores, state="readonly", width=250, height=35)
        self.combo_monitores.set(self.lista_monitores[0])
        self.combo_monitores.pack(pady=10)
        
        ctk.CTkButton(self, text="Gerar Relatório", command=self.confirmar_e_gerar, 
                      fg_color="#2980b9", hover_color="#3498db", text_color="white",
                      font=("Segoe UI", 12, "bold"), height=40).pack(pady=20)

    def confirmar_e_gerar(self):
        monitor_selecionado = self.combo_monitores.get()
        nome_responsavel = monitor_selecionado.split(" - ", 1)[1]
        agora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        nome_arquivo = f"Relatorio_Inventario_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.txt"
        
        caminho_desktop = obter_area_de_trabalho()
        pasta_relatorios = os.path.join(caminho_desktop, "Relatorios_TXT")

        if not os.path.exists(pasta_relatorios):
            os.makedirs(pasta_relatorios)

        caminho_arquivo = os.path.join(pasta_relatorios, nome_arquivo)
        
        try:
            materiais = self.sistema.listar_materiais()
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write("=" * 70 + "\n     RELATÓRIO OFICIAL DE INVENTÁRIO\n" + "=" * 70 + "\n")
                arquivo.write(f"Gerado em: {agora}\n\n--- POSIÇÃO ATUAL DO ESTOQUE ---\n\n")
                if not materiais:
                    arquivo.write("Nenhum material cadastrado no sistema.\n")
                else:
                    arquivo.write(f"{'ID':<5} | {'NOME DO MATERIAL':<25} | {'QTD':<5} | {'OBSERVAÇÕES'}\n")
                    arquivo.write("-" * 70 + "\n")
                    for mat in materiais:
                        obs = mat[3] if mat[3] else "Nenhuma"
                        nome_formatado = mat[1][:22] + "..." if len(mat[1]) > 25 else mat[1]
                        arquivo.write(f"{mat[0]:<5} | {nome_formatado:<25} | {mat[2]:<5} | {obs}\n")
                arquivo.write("\n" + "=" * 70 + f"\nRelatório gerado por: {nome_responsavel}\n" + "=" * 70 + "\n")
            
            messagebox.showinfo("Sucesso", f"Relatório gerado em: {caminho_arquivo}", parent=self)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}", parent=self)