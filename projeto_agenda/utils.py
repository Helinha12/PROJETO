from tkinter import messagebox


def sucesso(mensagem):
    messagebox.showinfo(
        "Sucesso",
        mensagem
    )


def alerta(mensagem):
    messagebox.showwarning(
        "Atenção",
        mensagem
    )


def erro(mensagem):
    messagebox.showerror(
        "Erro",
        mensagem
    )