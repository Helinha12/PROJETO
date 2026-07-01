import customtkinter as ctk
from tkinter import messagebox, ttk
from negocio.Contato_service import ContatoService

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class InterfaceGrafica(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.service = ContatoService()
        
        self.title("Agenda de Contatos Premium")
        self.geometry("1150x700")
        self.minsize(950, 600)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- MENU LATERAL ---
        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")
        self.frame_menu.grid_rowconfigure(4, weight=1)

        self.lbl_logo = ctk.CTkLabel(self.frame_menu, text="Agenda v2.0", font=("Arial", 20, "bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=30)

        self.btn_tela_cadastro = ctk.CTkButton(self.frame_menu, text="Cadastrar Contato", command=self.mostrar_tela_cadastro)
        self.btn_tela_cadastro.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.btn_tela_consulta = ctk.CTkButton(self.frame_menu, text="Consultar / Pesquisar", command=self.mostrar_tela_consulta)
        self.btn_tela_consulta.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # --- CONTÊINER DINÂMICO ---
        self.container_telas = ctk.CTkFrame(self, fg_color="transparent")
        self.container_telas.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container_telas.grid_columnconfigure(0, weight=1)
        self.container_telas.grid_rowconfigure(0, weight=1)

        self.tela_cadastro = FrameCadastro(self.container_telas, self.service)
        self.tela_consulta = FrameConsulta(self.container_telas, self.service)

        self.mostrar_tela_cadastro()

    def mostrar_tela_cadastro(self):
        self.tela_consulta.grid_forget()
        self.tela_cadastro.grid(row=0, column=0, sticky="nsew")
        self.btn_tela_cadastro.configure(fg_color="#1f538d")
        self.btn_tela_consulta.configure(fg_color=["#3a3a3a", "#242424"])

    def mostrar_tela_consulta(self):
        self.tela_cadastro.grid_forget()
        self.tela_consulta.grid(row=0, column=0, sticky="nsew")
        self.tela_consulta.atualizar_tabela()
        self.btn_tela_consulta.configure(fg_color="#1f538d")
        self.btn_tela_cadastro.configure(fg_color=["#3a3a3a", "#242424"])


class FrameCadastro(ctk.CTkFrame):
    def __init__(self, parent, service):
        super().__init__(parent)
        self.service = service
        
        # Listas temporárias na memória
        self.lista_telefones_adicionados = []
        self.lista_emails_adicionados = []
        self.lista_enderecos_adicionados = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.lbl_titulo = ctk.CTkLabel(self, text="Formulário de Cadastro", font=("Arial", 22, "bold"))
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, pady=15)

        # 1. Nome Completo e Categoria
        self.txt_nome = ctk.CTkEntry(self, placeholder_text="Nome Completo", height=35)
        self.txt_nome.grid(row=1, column=0, columnspan=2, padx=40, pady=5, sticky="ew")

        self.cb_categoria = ctk.CTkComboBox(self, values=["Pessoal", "Trabalho", "Família", "Outros"], height=35)
        self.cb_categoria.grid(row=2, column=0, columnspan=2, padx=40, pady=5, sticky="ew")

        # 2. Seção Multi-Telefone
        self.frame_tel = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tel.grid(row=3, column=0, columnspan=2, padx=40, pady=5, sticky="ew")
        self.frame_tel.grid_columnconfigure(0, weight=1)
        
        self.txt_telefone_input = ctk.CTkEntry(self.frame_tel, placeholder_text="Digitar Telefone", height=32)
        self.txt_telefone_input.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_add_tel = ctk.CTkButton(self.frame_tel, text="+", width=40, height=32, font=("Arial", 16, "bold"), command=self.adicionar_telefone_lista)
        self.btn_add_tel.grid(row=0, column=1)
        
        self.lbl_status_tels = ctk.CTkLabel(self, text="Nenhum telefone adicionado.", font=("Arial", 11, "italic"), text_color="gray")
        self.lbl_status_tels.grid(row=4, column=0, columnspan=2, padx=40, pady=2, sticky="w")

        # 3. Seção Multi-Email
        self.frame_mail = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_mail.grid(row=5, column=0, columnspan=2, padx=40, pady=5, sticky="ew")
        self.frame_mail.grid_columnconfigure(0, weight=1)
        
        self.txt_email_input = ctk.CTkEntry(self.frame_mail, placeholder_text="Digitar E-mail", height=32)
        self.txt_email_input.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_add_mail = ctk.CTkButton(self.frame_mail, text="+", width=40, height=32, font=("Arial", 16, "bold"), command=self.adicionar_email_lista)
        self.btn_add_mail.grid(row=0, column=1)
        
        self.lbl_status_mails = ctk.CTkLabel(self, text="Nenhum e-mail adicionado.", font=("Arial", 11, "italic"), text_color="gray")
        self.lbl_status_mails.grid(row=6, column=0, columnspan=2, padx=40, pady=2, sticky="w")

        # 4. Seção Multi-Endereço Detalhado
        self.lbl_end_secao = ctk.CTkLabel(self, text="Informações de Endereço", font=("Arial", 14, "bold"))
        self.lbl_end_secao.grid(row=7, column=0, columnspan=2, padx=40, pady=(15, 2), sticky="w")

        self.frame_inputs_endereco = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_inputs_endereco.grid(row=8, column=0, columnspan=2, padx=40, pady=5, sticky="ew")
        self.frame_inputs_endereco.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.txt_rua = ctk.CTkEntry(self.frame_inputs_endereco, placeholder_text="Rua/Av", height=30)
        self.txt_rua.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky="ew")

        self.txt_numero = ctk.CTkEntry(self.frame_inputs_endereco, placeholder_text="Nº", height=30)
        self.txt_numero.grid(row=0, column=2, padx=2, pady=2, sticky="ew")

        self.txt_cep = ctk.CTkEntry(self.frame_inputs_endereco, placeholder_text="CEP", height=30)
        self.txt_cep.grid(row=0, column=3, padx=2, pady=2, sticky="ew")

        self.txt_bairro = ctk.CTkEntry(self.frame_inputs_endereco, placeholder_text="Bairro", height=30)
        self.txt_bairro.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

        self.txt_cidade = ctk.CTkEntry(self.frame_inputs_endereco, placeholder_text="Cidade", height=30)
        self.txt_cidade.grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        self.txt_estado = ctk.CTkEntry(self.frame_inputs_endereco, placeholder_text="Estado", height=30)
        self.txt_estado.grid(row=1, column=2, padx=2, pady=2, sticky="ew")

        self.btn_add_endereco = ctk.CTkButton(self.frame_inputs_endereco, text="+", width=35, height=30, fg_color="#1f538d", font=("Arial", 16, "bold"), command=self.adicionar_endereco_lista)
        self.btn_add_endereco.grid(row=1, column=3, padx=2, pady=2, sticky="ew")

        self.lbl_status_enderecos = ctk.CTkLabel(self, text="Nenhum endereço adicionado ainda.", font=("Arial", 11, "italic"), text_color="gray")
        self.lbl_status_enderecos.grid(row=9, column=0, columnspan=2, padx=40, pady=2, sticky="w")

        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(self, text="Salvar Novo Contato", command=self.salvar, fg_color="green", hover_color="#005c00", height=42)
        self.btn_salvar.grid(row=10, column=0, columnspan=2, padx=40, pady=20, sticky="ew")

    def adicionar_telefone_lista(self):
        tel = self.txt_telefone_input.get().strip()
        if not tel:
            messagebox.showwarning("Aviso", "Digite um número de telefone válido!")
            return
        self.lista_telefones_adicionados.append(tel)
        self.lbl_status_tels.configure(text=f"Telefones adicionados: {len(self.lista_telefones_adicionados)} ({', '.join(self.lista_telefones_adicionados)})", text_color="green")
        self.txt_telefone_input.delete(0, "end")

    def adicionar_email_lista(self):
        email = self.txt_email_input.get().strip()
        if not email:
            messagebox.showwarning("Aviso", "Digite um e-mail válido!")
            return
        self.lista_emails_adicionados.append(email)
        self.lbl_status_mails.configure(text=f"E-mails adicionados: {len(self.lista_emails_adicionados)} ({', '.join(self.lista_emails_adicionados)})", text_color="green")
        self.txt_email_input.delete(0, "end")

    def adicionar_endereco_lista(self):
        rua = self.txt_rua.get().strip()
        num = self.txt_numero.get().strip()
        bairro = self.txt_bairro.get().strip()
        cidade = self.txt_cidade.get().strip()
        estado = self.txt_estado.get().strip()
        cep = self.txt_cep.get().strip()

        if not (rua and num and bairro and cidade and estado and cep):
            messagebox.showwarning("Aviso", "Preencha todos os campos do endereço antes de clicar em '+'!")
            return

        endereco_dict = {
            'rua': rua, 'numero': num, 'bairro': bairro, 
            'cidade': cidade, 'estado': estado, 'cep': cep
        }
        self.lista_enderecos_adicionados.append(endereco_dict)

        self.lbl_status_enderecos.configure(text=f"Endereços adicionados: {len(self.lista_enderecos_adicionados)}", text_color="green")
        self.txt_rua.delete(0, "end")
        self.txt_numero.delete(0, "end")
        self.txt_bairro.delete(0, "end")
        self.txt_cidade.delete(0, "end")
        self.txt_estado.delete(0, "end")
        self.txt_cep.delete(0, "end")

    def salvar(self):
        nome = self.txt_nome.get().strip()
        categoria = self.cb_categoria.get()

        if not nome or not categoria:
            messagebox.showerror("Erro de Validação", "O campo Nome Completo deve ser preenchido!")
            return

        
        if self.txt_telefone_input.get().strip():
            self.adicionar_telefone_lista()
        if self.txt_email_input.get().strip():
            self.adicionar_email_lista()
        if self.txt_rua.get().strip():
            self.adicionar_endereco_lista()

        # Validações rígidas de listas mínimas
        if not self.lista_telefones_adicionados:
            messagebox.showerror("Erro de Validação", "Você precisa adicionar pelo menos um telefone clicando no botão '+'!")
            return
        if not self.lista_enderecos_adicionados:
            messagebox.showerror("Erro de Validação", "Você precisa adicionar pelo menos um endereço completo clicando no botão '+'!")
            return

        try:
            self.service.cadastrar_contato(nome, categoria, self.lista_telefones_adicionados, self.lista_emails_adicionados, self.lista_enderecos_adicionados)
            messagebox.showinfo("Sucesso", "Contato completo salvo com sucesso no banco!")
            
            # Reset Geral da Interface
            self.txt_nome.delete(0, "end")
            self.lista_telefones_adicionados = []
            self.lista_emails_adicionados = []
            self.lista_enderecos_adicionados = []
            
            self.lbl_status_tels.configure(text="Nenhum telefone adicionado.", text_color="gray")
            self.lbl_status_mails.configure(text="Nenhum e-mail adicionado.", text_color="gray")
            self.lbl_status_enderecos.configure(text="Nenhum endereço adicionado ainda.", text_color="gray")
            
        except ValueError as e:
            messagebox.showerror("Erro", str(e))


class FrameConsulta(ctk.CTkFrame):
    def __init__(self, parent, service):
        super().__init__(parent)
        self.service = service
        self.id_selecionado = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        
        self.frame_busca = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_busca.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        self.frame_busca.grid_columnconfigure(0, weight=1)  # <-- Corrigido aqui!

        self.txt_busca = ctk.CTkEntry(self.frame_busca, placeholder_text="Pesquisar contato por nome...")
        self.txt_busca.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.btn_busca = ctk.CTkButton(self.frame_busca, text="Buscar", width=100, command=self.atualizar_tabela)
        self.btn_busca.grid(row=0, column=1, padx=5)

    
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2a2a2a", foreground="white", fieldbackground="#2a2a2a", rowheight=30)
        style.map("Treeview", background=[('selected', '#1f538d')])

    
        self.tabela = ttk.Treeview(self, columns=("ID", "Nome", "Categoria", "Telefones", "E-mails", "Endereços"), show="headings")
        self.tabela.heading("ID", text="ID")
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("Categoria", text="Categoria")
        self.tabela.heading("Telefones", text="Telefones")
        self.tabela.heading("E-mails", text="E-mails")
        self.tabela.heading("Endereços", text="Endereços")
        
        
        self.tabela.column("ID", width=40, anchor="center")
        self.tabela.column("Nome", width=150)
        self.tabela.column("Categoria", width=100)
        self.tabela.column("Telefones", width=150)
        self.tabela.column("E-mails", width=150)
        self.tabela.column("Endereços", width=350)
        self.tabela.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
        self.tabela.bind("<<TreeviewSelect>>", self.mapear_selecao)

        
        self.btn_deletar = ctk.CTkButton(self, text="Excluir Contato Selecionado", command=self.excluir, fg_color="red", hover_color="#990000", height=35)
        self.btn_deletar.grid(row=2, column=0, padx=15, pady=15, sticky="ew")

    def atualizar_tabela(self):
        
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        
        termo = self.txt_busca.get()
        for c in self.service.listar_contatos(termo):
            self.tabela.insert("", "end", values=(
                c.id, 
                c.nome, 
                c.categoria, 
                ", ".join(c.telefones), 
                ", ".join(c.emails), 
                " | ".join(c.enderecos)
            ))

    def mapear_selecao(self, event):
        item_selecionado = self.tabela.selection()
        if item_selecionado:
            valores = self.tabela.item(item_selecionado, "values")
            self.id_selecionado = valores[0]

    def excluir(self):
        try:
            self.service.excluir_contato(self.id_selecionado)
            messagebox.showinfo("Sucesso", "Contato removido com sucesso!")
            self.id_selecionado = None
            self.atualizar_tabela()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))