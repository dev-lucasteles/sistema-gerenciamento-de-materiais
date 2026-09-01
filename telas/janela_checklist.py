import customtkinter as ctk
from tkinter import messagebox
import os
import platform
import subprocess

from modelos import Material, ItemChecklist
from utils.executor import rodar_em_background

class JanelaChecklist(ctk.CTkToplevel):
    def __init__(self, master, servicos):
        super().__init__(master)
        
        self.servico_estoque = servicos["estoque"]
        self.servico_checklist = servicos["checklist"]
        
        self.title("Check-list Diário")
        self.geometry("1050x700") 
        self.transient(master)
        self.grab_set()
        
        self.entradas_checklist = {}
        self.lista_entries = []

        ctk.CTkLabel(self, text="📝 Check-list de Materiais", font=("Segoe UI", 22, "bold"), text_color="#e0e0e0").pack(pady=(25, 15))

        if not self._configurar_monitor_responsavel():
            return

        self._configurar_cabecalho()
        self._configurar_lista()
        self._carregar_materiais()

        self.btn_salvar = ctk.CTkButton(self, text="Salvar e Registrar Check-list", command=self.iniciar_salvamento, 
                                        fg_color="#d35400", hover_color="#e67e22", text_color="white",
                                        font=("Segoe UI", 14, "bold"), height=45, corner_radius=8)
        self.btn_salvar.pack(pady=20)

    def _configurar_monitor_responsavel(self):
        try:
            monitores = self.servico_estoque.listar_monitores_ativos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar monitores: {e}", parent=self)
            self.destroy()
            return False

        if not monitores:
            messagebox.showwarning("Aviso", "Você precisa cadastrar pelo menos um monitor antes de realizar o check-list!", parent=self)
            self.destroy()
            return False

        lista_monitores = [f"{m.id_monitor} - {m.nome}" for m in monitores]
        
        frame_monitor = ctk.CTkFrame(self, fg_color="transparent")
        frame_monitor.pack(pady=10)
        
        ctk.CTkLabel(frame_monitor, text="Monitor Responsável:", font=("Segoe UI", 12, "bold"), text_color="#e0e0e0").pack(side="left", padx=10)
        self.combo_monitor_resp = ctk.CTkComboBox(frame_monitor, values=lista_monitores, state="readonly", width=300)
        self.combo_monitor_resp.set(lista_monitores[0])
        self.combo_monitor_resp.pack(side="left", padx=5)
        return True

    def _configurar_cabecalho(self):
        self.frame_cabecalho = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=8)
        self.frame_cabecalho.pack(fill="x", padx=30, pady=(15, 0))
        
        font_cab = ("Segoe UI", 12, "bold")
        cor_cab = "#3498db"
        
        ctk.CTkLabel(self.frame_cabecalho, text="Material", font=font_cab, text_color=cor_cab).grid(row=0, column=0, padx=10, pady=12, sticky="w")
        ctk.CTkLabel(self.frame_cabecalho, text="Esperado", font=font_cab, text_color=cor_cab).grid(row=0, column=1, padx=10, pady=12)
        ctk.CTkLabel(self.frame_cabecalho, text="Encontrado", font=font_cab, text_color=cor_cab).grid(row=0, column=2, padx=10, pady=12)
        ctk.CTkLabel(self.frame_cabecalho, text="Observação", font=font_cab, text_color=cor_cab).grid(row=0, column=3, padx=10, pady=12)
        ctk.CTkLabel(self.frame_cabecalho, text="Quarto", font=font_cab, text_color=cor_cab).grid(row=0, column=4, padx=10, pady=12)
        
        tamanhos = [350, 100, 120, 150, 100]
        for i, t in enumerate(tamanhos):
            self.frame_cabecalho.grid_columnconfigure(i, minsize=t)

    def _configurar_lista(self):
        self.frame_lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.frame_lista.pack(fill="both", expand=True, padx=20, pady=(5, 10))

    def mover_foco(self, event, direcao, index):
        novo_index = index + direcao
        if 0 <= novo_index < len(self.lista_entries):
            self.lista_entries[novo_index].focus_set()
            fracao_rolagem = novo_index / len(self.lista_entries)
            try:
                self.frame_lista._parent_canvas.yview_moveto(fracao_rolagem)
            except:
                pass
        return "break"

    def _carregar_materiais(self):
        try:
            materiais = self.servico_estoque.listar_materiais_ativos()
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=self)
            return
            
        if not materiais:
            ctk.CTkLabel(self.frame_lista, text="Nenhum material cadastrado no sistema.", text_color="#e74c3c", font=("Segoe UI", 12)).pack(pady=20)
            return

        for i, mat in enumerate(materiais):
            bg_color = "#2a2a2a" if i % 2 == 0 else "#1e1e1e"

            frame_linha = ctk.CTkFrame(self.frame_lista, fg_color=bg_color, corner_radius=6)
            frame_linha.pack(fill="x", pady=3, padx=5)

            ctk.CTkLabel(frame_linha, text=mat.nome, text_color="#e0e0e0").grid(row=0, column=0, padx=10, pady=8, sticky="w")
            ctk.CTkLabel(frame_linha, text=str(mat.quantidade), text_color="#e0e0e0").grid(row=0, column=1, padx=10, pady=8)

            entry_qtd = ctk.CTkEntry(frame_linha, width=80, justify="center")
            entry_qtd.grid(row=0, column=2, padx=10, pady=8)

            combo_obs = ctk.CTkComboBox(frame_linha, values=["", "Pendente", "Danificado"], state="readonly", width=130)
            combo_obs.set("")
            combo_obs.grid(row=0, column=3, padx=10, pady=8)

            entry_quarto = ctk.CTkEntry(frame_linha, width=80, justify="center")
            entry_quarto.grid(row=0, column=4, padx=10, pady=8)

            tamanhos = [350, 100, 120, 150, 100]
            for col, t in enumerate(tamanhos):
                frame_linha.grid_columnconfigure(col, minsize=t)

            self.entradas_checklist[mat.id_material] = (mat.nome, mat.quantidade, entry_qtd, combo_obs, entry_quarto)
            self.lista_entries.append(entry_qtd)

        for index, entry in enumerate(self.lista_entries):
            entry.bind("<Up>", lambda event, idx=index: self.mover_foco(event, -1, idx))
            entry.bind("<Down>", lambda event, idx=index: self.mover_foco(event, 1, idx))

        if self.lista_entries:
            self.lista_entries[0].focus_set()

    def iniciar_salvamento(self):
        if not self.entradas_checklist:
            messagebox.showwarning("Aviso", "Não há materiais para verificar no check-list!", parent=self)
            return
            
        monitor_responsavel = self.combo_monitor_resp.get().split(" - ", 1)[1]
        itens_verificados = []
        
        for id_mat, dados in self.entradas_checklist.items():
            nome, qtd_esperada, entry, combo_obs, entry_quarto = dados
            qtd_txt = entry.get().strip()
            
            if not qtd_txt:
                messagebox.showerror("Erro", f"Você esqueceu de preencher a quantidade de '{nome}'.", parent=self)
                return
                
            try:
                qtd_encontrada = int(qtd_txt)
                if qtd_encontrada < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", f"A quantidade de '{nome}' deve ser um número inteiro positivo!", parent=self)
                return
                
            itens_verificados.append(
                ItemChecklist(
                    id_material=id_mat,
                    nome_material=nome,
                    qtd_esperada=qtd_esperada,
                    qtd_encontrada=qtd_encontrada,
                    observacao=combo_obs.get(),
                    quarto=entry_quarto.get().strip()
                )
            )

        self.btn_salvar.configure(state="disabled", text="Gerando Relatório... Aguarde!", fg_color="#555555")

        def tarefa_pesada():
            return self.servico_checklist.processar_checklist(monitor_responsavel, itens_verificados)
            
        def ao_terminar(resultado):
            self.finalizar_salvamento(resultado)
            
        def ao_falhar(erro):
            messagebox.showerror("Erro Crítico", f"Falha na geração: {erro}", parent=self)
            self.btn_salvar.configure(state="normal", text="Salvar e Registrar Check-list", fg_color="#d35400")

        rodar_em_background(self, tarefa_pesada, ao_terminar, ao_falhar)

    def finalizar_salvamento(self, resultado):
        if not self.winfo_exists(): return
        
        if not resultado["sucesso"]:
            messagebox.showerror("Erro", resultado.get("erro", "Erro desconhecido"), parent=self)
            self.btn_salvar.configure(state="normal", text="Salvar e Registrar Check-list", fg_color="#d35400")
            return
        
        try:
            sistema_os = platform.system()
            caminho_imagem = resultado["nome_imagem"]
            
            if sistema_os == "Windows": 
                os.startfile(caminho_imagem)
            elif sistema_os == "Darwin": 
                subprocess.Popen(["open", caminho_imagem])
            else: 
                subprocess.Popen(["xdg-open", caminho_imagem])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir a imagem: {e}", parent=self)

        if resultado["alertas"]:
            mensagem_final = f"Check-list pronto!\n\nAlertas:\n\n" + "\n".join(resultado["alertas"])
            messagebox.showwarning("Atenção!", mensagem_final, parent=self)
        else:
            messagebox.showinfo("Sucesso", "Check-list perfeito! Nenhum item faltando.", parent=self)
            
        self.destroy()