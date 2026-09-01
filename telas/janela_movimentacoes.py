import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

from excecoes import EstoqueInsuficienteError, MaterialNaoEncontradoError

class JanelaMovimentacoes(ctk.CTkToplevel):
    def __init__(self, master, servico_estoque):
        super().__init__(master)
        self.servico_estoque = servico_estoque 
        self.title("Movimentações de Estoque")
        self.geometry("450x520") 
        self.transient(master)
        self.grab_set()

        if not self._configurar_monitor_responsavel():
            return

        self.abas = ctk.CTkTabview(self, corner_radius=10, fg_color="#1e1e1e")
        self.abas.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        self.abas.add(" Registar Entrada ")
        self.abas.add(" Registar Dano/Perda ")

        self.aba_entrada = self.abas.tab(" Registar Entrada ")
        self.aba_dano = self.abas.tab(" Registar Dano/Perda ")

        self._construir_aba_entrada()
        self._construir_aba_dano()
        self.atualizar_combos_mov()
    
    def _configurar_monitor_responsavel(self):
        try:
            monitores = self.servico_estoque.listar_monitores_ativos()
        except Exception as e:
            messagebox.showerror("Erro", str(e), parent=self)
            self.destroy()
            return False
        if not monitores:
            messagebox.showwarning("Aviso", "Cadastre um monitor antes!", parent=self)
            self.destroy()
            return False

        lista_monitores = [f"{m.id_monitor} - {m.nome}" for m in monitores]
        frame_monitor = ctk.CTkFrame(self, fg_color="transparent")
        frame_monitor.pack(pady=(15, 10))
        
        ctk.CTkLabel(frame_monitor, text="Monitor:", font=("Segoe UI", 12, "bold"), text_color="#e0e0e0").pack(side="left", padx=10)
        self.combo_monitor_resp = ctk.CTkComboBox(frame_monitor, values=lista_monitores, state="readonly", width=250)
        self.combo_monitor_resp.set(lista_monitores[0])
        self.combo_monitor_resp.pack(side="left", padx=5)
        return True

    def _construir_aba_entrada(self):
        ctk.CTkLabel(self.aba_entrada, text="Registrar Entrada", font=("Segoe UI", 18, "bold"), text_color="#27ae60").pack(pady=(25, 15))
        
        ctk.CTkLabel(self.aba_entrada, text="Selecione o Material:", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(5, 0))
        self.combo_mat_ent = ctk.CTkComboBox(self.aba_entrada, state="readonly", width=320, height=35)
        self.combo_mat_ent.pack(pady=5)
        
        ctk.CTkLabel(self.aba_entrada, text="Quantidade a Adicionar:", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(10, 0))
        self.entry_qtd_ent = ctk.CTkEntry(self.aba_entrada, width=320, height=35)
        self.entry_qtd_ent.pack(pady=5)
        
        ctk.CTkLabel(self.aba_entrada, text="Data (ANO-MÊS-DIA):", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(10, 0))
        self.entry_data_ent = ctk.CTkEntry(self.aba_entrada, width=320, height=35)
        self.entry_data_ent.insert(0, datetime.now().strftime("%Y-%m-%d"))  
        self.entry_data_ent.pack(pady=5)
        
        ctk.CTkButton(self.aba_entrada, text="📥 Confirmar Entrada", command=self.confirmar_entrada, 
                      fg_color="#27ae60", hover_color="#2ecc71", font=("Segoe UI", 12, "bold"), height=40).pack(pady=25)

    def _construir_aba_dano(self):
        ctk.CTkLabel(self.aba_dano, text="Registrar Baixa / Perda", font=("Segoe UI", 18, "bold"), text_color="#e74c3c").pack(pady=(25, 15))
        
        ctk.CTkLabel(self.aba_dano, text="Selecione o Material:", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(5, 0))
        self.combo_mat_dano = ctk.CTkComboBox(self.aba_dano, state="readonly", width=320, height=35)
        self.combo_mat_dano.pack(pady=5)
        
        ctk.CTkLabel(self.aba_dano, text="Quantidade Danificada/Perdida:", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(10, 0))
        self.entry_qtd_dano = ctk.CTkEntry(self.aba_dano, width=320, height=35)
        self.entry_qtd_dano.pack(pady=5)
        
        ctk.CTkLabel(self.aba_dano, text="Data (ANO-MÊS-DIA):", text_color="#a0a0a0").pack(anchor="w", padx=40, pady=(10, 0))
        self.entry_data_dano = ctk.CTkEntry(self.aba_dano, width=320, height=35)
        self.entry_data_dano.insert(0, datetime.now().strftime("%Y-%m-%d"))  
        self.entry_data_dano.pack(pady=5)
        
        ctk.CTkButton(self.aba_dano, text="⚠️ Confirmar Baixa", command=self.confirmar_dano, 
                      fg_color="#c0392b", hover_color="#e74c3c", font=("Segoe UI", 12, "bold"), height=40).pack(pady=25)

    def atualizar_combos_mov(self):
        sel_ent = self.combo_mat_ent.get().split(" - ")[0] if self.combo_mat_ent.get() else None
        sel_dano = self.combo_mat_dano.get().split(" - ")[0] if self.combo_mat_dano.get() else None

        try:
            materiais = self.servico_estoque.listar_materiais_ativos()
            lista_formatada = [f"{m.id_material} - {m.nome} (Atual: {m.quantidade})" for m in materiais]
            
            if lista_formatada:
                self.combo_mat_ent.configure(values=lista_formatada)
                self.combo_mat_dano.configure(values=lista_formatada)
                
                idx_ent = next((i for i, v in enumerate(lista_formatada) if v.startswith(f"{sel_ent} - ")), 0)
                idx_dano = next((i for i, v in enumerate(lista_formatada) if v.startswith(f"{sel_dano} - ")), 0)
                
                self.combo_mat_ent.set(lista_formatada[idx_ent])
                self.combo_mat_dano.set(lista_formatada[idx_dano])
            else:
                self.combo_mat_ent.configure(values=[""])
                self.combo_mat_dano.configure(values=[""])
                self.combo_mat_ent.set("")
                self.combo_mat_dano.set("")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}", parent=self)

    def confirmar_entrada(self):
        selecionado = self.combo_mat_ent.get()
        qtd_texto = self.entry_qtd_ent.get().strip()
        data_texto = self.entry_data_ent.get().strip()
        
        if not selecionado or not qtd_texto or not data_texto:
            return messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!", parent=self)
            
        try:
            quantidade = int(qtd_texto)
            datetime.strptime(data_texto, "%Y-%m-%d") 
            
            id_mat = int(selecionado.split(" - ")[0])
            id_mon = int(self.combo_monitor_resp.get().split(" - ")[0])

            self.servico_estoque.registrar_entrada_material(
                id_material=id_mat,
                quantidade_adicionada=quantidade,
                id_monitor=id_mon,
                data_entrada=data_texto
            )

            messagebox.showinfo("Sucesso", "Entrada registrada e estoque atualizado!", parent=self)
            self.entry_qtd_ent.delete(0, 'end')
            self.atualizar_combos_mov()  

        except ValueError:
            messagebox.showerror("Erro de Preenchimento", "Verifique os dados:\n- Quantidade deve ser um número inteiro positivo.\n- Data deve ser ANO-MÊS-DIA.", parent=self)
        except MaterialNaoEncontradoError as e:
            messagebox.showerror("Erro de Material", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha interna no sistema:\n{e}", parent=self)

    def confirmar_dano(self):
        selecionado = self.combo_mat_dano.get()
        qtd_texto = self.entry_qtd_dano.get().strip()
        data_texto = self.entry_data_dano.get().strip()

        if not selecionado or not qtd_texto or not data_texto:
            return messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!", parent=self)

        try:
            quantidade = int(qtd_texto)
            datetime.strptime(data_texto, "%Y-%m-%d") 
            
            id_mat = int(selecionado.split(" - ")[0])
            id_mon = int(self.combo_monitor_resp.get().split(" - ")[0])

            self.servico_estoque.registrar_baixa_por_dano(
                id_material=id_mat,
                quantidade_perdida=quantidade,
                id_monitor=id_mon,
                data_baixa=data_texto
            )

            messagebox.showinfo("Sucesso", "Dano registrado e estoque atualizado!", parent=self)
            self.entry_qtd_dano.delete(0, 'end')
            self.atualizar_combos_mov()  

        except ValueError:
            messagebox.showerror("Erro de Preenchimento", "Verifique os dados:\n- Quantidade deve ser um número inteiro positivo.\n- Data deve ser ANO-MÊS-DIA.", parent=self)
        except EstoqueInsuficienteError as e:
            messagebox.showwarning("Atenção - Estoque", str(e), parent=self)
        except MaterialNaoEncontradoError as e:
            messagebox.showerror("Erro de Material", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Falha interna no sistema:\n{e}", parent=self)