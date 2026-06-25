import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, callback):
        super().__init__(
            master,
            width=220,
            corner_radius=0
        )

        self.callback = callback

        titulo = ctk.CTkLabel(
            self,
            text="📇 Agenda",
            font=("Segoe UI", 24, "bold")
        )
        titulo.pack(pady=30)

        botoes = [
            ("👥 Contatos", "contatos"),
            ("➕ Novo Contato", "cadastro"),
            ("📂 Categorias", "categorias")
        ]

        for texto, pagina in botoes:

            btn = ctk.CTkButton(
                self,
                text=texto,
                command=lambda p=pagina: self.callback(p)
            )

            btn.pack(
                fill="x",
                padx=15,
                pady=5
            )