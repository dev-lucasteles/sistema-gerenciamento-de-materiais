import customtkinter as ctk
from tkinter import messagebox

class JanelaMonitor(ctk.CTkToplevel):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema
        self.title("Gerenciar Monitores")
        self.geometry("450x400")
        self.transient(master)
        self.grab_set()
        
        self.abas = ctk.CTkTabview(self, corner_radius=10, fg_color="#1e1e1e")
        self.abas.pack(fill="both", expand=True, padx=20, pady=20)

        self.abas.add(" Cadastrar ")
        self.abas.add(" Atualizar ")
        self.abas.add(" Deletar ")

        self.aba_cadastrar = self.abas.tab(" Cadastrar ")
        self.aba_atualizar = self.abas.tab(" Atualizar ")
        self.aba_deletar = self.abas.tab(" Deletar ")

        self._construir_aba_cadastrar()
        self._construir_aba_atualizar()
        self._construir_aba_deletar()
        self.atualizar_listas()

    def _construir_aba_cadastrar(self):
        ctk.CTkLabel(self.aba_cadastrar, text="Cadastrar Novo Monitor", font=("Segoe UI", 18, "bold"), text_color="#e0e0e0").pack(pady=(25, 15))
        
        ctk.CTkLabel(self.aba_cadastrar, text="Nome Completo do Monitor:", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(10, 0))
        self.entry_nome_mon = ctk.CTkEntry(self.aba_cadastrar, width=320, height=35)
        self.entry_nome_mon.pack(pady=5)
        
        ctk.CTkButton(self.aba_cadastrar, text="Salvar Monitor", command=self.salvar_monitor, 
                      fg_color="#27ae60", hover_color="#2ecc71", font=("Segoe UI", 12, "bold"), height=40).pack(pady=30)

    def _construir_aba_atualizar(self):
        ctk.CTkLabel(self.aba_atualizar, text="Atualizar Monitor", font=("Segoe UI", 18, "bold"), text_color="#e0e0e0").pack(pady=(25, 15))
        
        ctk.CTkLabel(self.aba_atualizar, text="Selecione o Monitor antigo:", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(5, 0))
        self.combo_atualizar = ctk.CTkComboBox(self.aba_atualizar, state="readonly", width=320, height=35, command=self.preencher_dados_atuais)
        self.combo_atualizar.pack(pady=5)
        
        ctk.CTkLabel(self.aba_atualizar, text="Digite o Novo Nome:", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(10, 0))
        self.entry_novo_nome = ctk.CTkEntry(self.aba_atualizar, width=320, height=35)
        self.entry_novo_nome.pack(pady=5)
        
        ctk.CTkButton(self.aba_atualizar, text="Atualizar Nome", command=self.btn_atualizar_click, 
                      fg_color="#2980b9", hover_color="#3498db", font=("Segoe UI", 12, "bold"), height=40).pack(pady=25)

    def _construir_aba_deletar(self):
        ctk.CTkLabel(self.aba_deletar, text="Deletar Monitor", font=("Segoe UI", 18, "bold"), text_color="#e74c3c").pack(pady=(35, 15))
        
        ctk.CTkLabel(self.aba_deletar, text="Selecione o Monitor a ser removido:", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(10, 0))
        self.combo_deletar = ctk.CTkComboBox(self.aba_deletar, state="readonly", width=320, height=35)
        self.combo_deletar.pack(pady=5)
        
        ctk.CTkButton(self.aba_deletar, text="🗑️ Deletar Monitor", command=self.btn_deletar_click, 
                      fg_color="#c0392b", hover_color="#e74c3c", font=("Segoe UI", 12, "bold"), height=40).pack(pady=35)

    def preencher_dados_atuais(self, valor_selecionado=None):
        selecionado = self.combo_atualizar.get()
        if not selecionado: return
        id_mon = int(selecionado.split(" - ")[0])
        monitor = next((m for m in self.sistema.listar_monitores() if m[0] == id_mon), None)
        if monitor:
            self.entry_novo_nome.delete(0, 'end')
            self.entry_novo_nome.insert(0, monitor[1])

    def atualizar_listas(self):
        sel_atual = self.combo_atualizar.get().split(" - ")[0] if self.combo_atualizar.get() else None
        try:
            lista_formatada = [f"{m[0]} - {m[1]}" for m in self.sistema.listar_monitores()]
            if lista_formatada:
                self.combo_atualizar.configure(values=lista_formatada)
                self.combo_deletar.configure(values=lista_formatada)
                idx_atual = next((i for i, v in enumerate(lista_formatada) if v.startswith(f"{sel_atual} - ")), 0)
                self.combo_atualizar.set(lista_formatada[idx_atual])
                self.combo_deletar.set(lista_formatada[0])
                self.preencher_dados_atuais()
            else:
                self.combo_atualizar.configure(values=[""]); self.combo_deletar.configure(values=[""])
                self.combo_atualizar.set(""); self.combo_deletar.set("")
                self.entry_novo_nome.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}", parent=self)

    def salvar_monitor(self):
        nome = self.entry_nome_mon.get().strip()
        if not nome: return messagebox.showerror("Erro", "O nome é obrigatório!", parent=self)
        try:
            self.sistema.criar_monitor(nome)
            messagebox.showinfo("Sucesso", f"Monitor '{nome}' cadastrado!", parent=self)
            self.entry_nome_mon.delete(0, 'end')
            self.atualizar_listas() 
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}", parent=self)

    def btn_atualizar_click(self):
        selecionado, novo_nome = self.combo_atualizar.get(), self.entry_novo_nome.get().strip()
        if not selecionado or not novo_nome: return messagebox.showerror("Erro", "Preencha o novo nome!", parent=self)
        try:
            self.sistema.atualizar_monitor(int(selecionado.split(" - ")[0]), novo_nome)
            messagebox.showinfo("Sucesso", "Monitor atualizado!", parent=self)
            self.entry_novo_nome.delete(0, 'end')
            self.atualizar_listas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}", parent=self)

    def btn_deletar_click(self):
        selecionado = self.combo_deletar.get()
        if not selecionado: return messagebox.showerror("Erro", "Selecione!", parent=self)
        if messagebox.askyesno("Confirmar", f"Deletar:\n{selecionado}?", parent=self):
            try:
                self.sistema.deletar_monitor(int(selecionado.split(" - ")[0]))
                messagebox.showinfo("Sucesso", "Deletado!", parent=self)
                self.atualizar_listas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}", parent=self)