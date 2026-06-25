import customtkinter as ctk


class CategoriasPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        titulo = ctk.CTkLabel(
            self,
            text="Categorias",
            font=("Segoe UI", 28, "bold")
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        categorias = [
            "Família",
            "Amigos",
            "Trabalho",
            "Escola",
            "Outros"
        ]

        for categoria in categorias:

            item = ctk.CTkLabel(
                self,
                text=f"📂 {categoria}"
            )

            item.pack(
                anchor="w",
                padx=30,
                pady=5
            )