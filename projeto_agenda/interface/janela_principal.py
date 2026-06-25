import customtkinter as ctk

from interface.components.sidebar import Sidebar
from interface.pages.contatos_page import ContatosPage
from interface.pages.cadastro_page import CadastroPage
from interface.pages.categorias_page import CategoriasPage

class JanelaPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Agenda de Contatos")
        self.geometry("1200x700")

        ctk.set_appearance_mode("light")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self,
            self.mostrar_pagina
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.container = ctk.CTkFrame(self)
        self.container.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.pagina_atual = None

        self.mostrar_pagina("contatos")

    def mostrar_pagina(self, pagina, **kwargs):

        if self.pagina_atual:
            self.pagina_atual.destroy()

        if pagina == "contatos":
            self.pagina_atual = ContatosPage(
                self.container
            )
        elif pagina == "cadastro":
            # allow passing a Contato instance via kwargs for editing
            contato = kwargs.get('contato')
            if contato:
                self.pagina_atual = CadastroPage(self.container, contato=contato)
            else:
                self.pagina_atual = CadastroPage(self.container)
        elif pagina == "categorias":
            self.pagina_atual = CategoriasPage(
                self.container
            )

        self.pagina_atual.pack(
            fill="both",
            expand=True
        )