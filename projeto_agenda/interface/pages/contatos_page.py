import customtkinter as ctk
from tkinter import ttk, messagebox

from negocio.contato_service import ContatoService
from utils import sucesso, erro


class ContatosPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        titulo = ctk.CTkLabel(
            self,
            text="Contatos",
            font=("Segoe UI", 28, "bold")
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        self.pesquisa = ctk.CTkEntry(
            self,
            placeholder_text="🔍 Pesquisar contato..."
        )

        self.pesquisa.pack(
            fill="x",
            padx=20,
            pady=10
        )

        colunas = (
            "Nome",
            "Categoria",
            "Telefones",
            "Emails",
            "Endereços"
        )

        self.tabela = ttk.Treeview(
            self,
            columns=colunas,
            show="headings",
            height=15
        )

        for coluna in colunas:
            self.tabela.heading(
                coluna,
                text=coluna
            )

        self.tabela.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )
        self._carregar_contatos()

        # ações rápidas: duplo-clique para editar e Delete para remover
        self.tabela.bind("<Double-1>", lambda e: self._editar_selecionado())
        self.tabela.bind("<Delete>", lambda e: self._excluir_selecionado())

        rodape = ctk.CTkFrame(self)

        rodape.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # placeholders serão atualizados em _carregar_contatos
        self.lbl_contatos = ctk.CTkLabel(rodape, text="")
        self.lbl_contatos.pack(side="left", padx=10)

        self.lbl_telefones = ctk.CTkLabel(rodape, text="")
        self.lbl_telefones.pack(side="left", padx=10)

        self.lbl_emails = ctk.CTkLabel(rodape, text="")
        self.lbl_emails.pack(side="left", padx=10)

        self.lbl_enderecos = ctk.CTkLabel(rodape, text="")
        self.lbl_enderecos.pack(side="left", padx=10)
        
        # ações
        acoes = ctk.CTkFrame(self)
        acoes.pack(fill="x", padx=20)

        btn_excluir = ctk.CTkButton(acoes, text="Excluir", command=self._excluir_selecionado)
        btn_excluir.pack(side="right")
        btn_editar = ctk.CTkButton(acoes, text="Editar", command=self._editar_selecionado)
        btn_editar.pack(side="right", padx=6)

    def _carregar_contatos(self):
        service = ContatoService()
        contatos = service.listar_todos()

    
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        total_contatos = 0
        total_telefones = 0
        total_emails = 0
        total_enderecos = 0
        for c in contatos:
            total_contatos += 1
            total_telefones += len(c.telefones)
            total_emails += len(c.emails)
            total_enderecos += len(c.enderecos)

            telef_str = ', '.join([t.numero for t in c.telefones]) if c.telefones else ''
            emails_str = ', '.join([e.endereco for e in c.emails]) if c.emails else ''
            enderecos_str = ', '.join([ed.rua for ed in c.enderecos]) if c.enderecos else ''

            self.tabela.insert('', 'end', iid=str(c.id), values=(c.nome, c.categoria or '', telef_str, emails_str, enderecos_str))

        # atualizar rodapé com valores reais
        try:
            self.lbl_contatos.configure(text=f"👥 Contatos: {total_contatos}")
            self.lbl_telefones.configure(text=f"📞 Telefones: {total_telefones}")
            self.lbl_emails.configure(text=f"✉️ Emails: {total_emails}")
            self.lbl_enderecos.configure(text=f"🏠 Endereços: {total_enderecos}")
        except Exception:
            pass
        
    def _excluir_selecionado(self):
        sel = self.tabela.selection()
        if not sel:
            erro('Nenhum contato selecionado')
            return
        contato_id = int(sel[0])
        # confirmar ação
        if not messagebox.askyesno("Confirmar exclusão", "Deseja excluir o contato selecionado?"):
            return

        try:
            ContatoService().remover(contato_id)
            sucesso('Contato removido')
            self._carregar_contatos()
        except Exception as e:
            erro('Erro ao remover: ' + str(e))

    def _editar_selecionado(self):
        sel = self.tabela.selection()
        if not sel:
            erro('Nenhum contato selecionado')
            return
        contato_id = int(sel[0])
        service = ContatoService()
        contatos = service.listar_todos()
        contato = next((c for c in contatos if c.id == contato_id), None)
        if contato is None:
            erro('Contato não encontrado')
            return

        # pedir para JanelaPrincipal mostrar a página de cadastro com o contato
        # container.master é a janela principal
        try:
            self.master.master.mostrar_pagina('cadastro', contato=contato)
        except Exception:
            erro('Não foi possível abrir editor')