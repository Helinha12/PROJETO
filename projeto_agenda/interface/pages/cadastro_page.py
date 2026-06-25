import customtkinter as ctk
from dominio.contato import Contato
from dominio.telefone import Telefone
from dominio.email import Email
from dominio.endereco import Endereco
from negocio.contato_service import ContatoService


class CadastroPage(ctk.CTkFrame):

    def __init__(self, master, contato=None):
        super().__init__(master)

        titulo_text = "Editar Contato" if contato is not None else "Novo Contato"
        titulo = ctk.CTkLabel(
            self,
            text=titulo_text,
            font=("Segoe UI", 28, "bold")
        )

        titulo.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            self,
            text="Nome"
        ).pack(
            anchor="w",
            padx=20
        )

        self.nome = ctk.CTkEntry(
            self,
            width=400
        )

        self.nome.pack(
            padx=20,
            pady=10
        )

        ctk.CTkLabel(
            self,
            text="Categoria"
        ).pack(
            anchor="w",
            padx=20
        )

        self.categoria = ctk.CTkOptionMenu(
            self,
            values=[
                "Selecione",
                "Família",
                "Amigos",
                "Trabalho",
                "Escola",
                "Outros"
            ]
        )

        self.categoria.set("Selecione")
        self.categoria.pack(
            padx=20,
            pady=10
        )

        self._editing_id = None

        ctk.CTkLabel(
            self,
            text="Telefone"
        ).pack(
            anchor="w",
            padx=20
        )

        self.telefone = ctk.CTkEntry(
            self,
            width=400
        )

        self.telefone.pack(
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            self,
            text="Adicionar telefone",
            command=self.adicionar_telefone
        ).pack(
            padx=20,
            pady=(0, 10),
            anchor="w"
        )

        ctk.CTkLabel(
            self,
            text="Email"
        ).pack(
            anchor="w",
            padx=20
        )

        self.email = ctk.CTkEntry(
            self,
            width=400
        )

        self.email.pack(
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            self,
            text="Adicionar email",
            command=self.adicionar_email
        ).pack(
            padx=20,
            pady=(0, 10),
            anchor="w"
        )

        ctk.CTkLabel(
            self,
            text="Endereço"
        ).pack(
            anchor="w",
            padx=20
        )

        self.endereco = ctk.CTkEntry(
            self,
            width=400
        )

        self.endereco.pack(
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            self,
            text="Adicionar endereço",
            command=self.adicionar_endereco
        ).pack(
            padx=20,
            pady=(0, 10),
            anchor="w"
        )

        self.salvar = ctk.CTkButton(
            self,
            text="Salvar",
            command=self._on_salvar
        )

        self.salvar.pack(
            pady=20
        )

        self.frame_telefones = ctk.CTkFrame(self)
        self.frame_telefones.pack(fill="x", padx=20, pady=(0, 10))
        self.telefones = []

        self.frame_emails = ctk.CTkFrame(self)
        self.frame_emails.pack(fill="x", padx=20, pady=(0, 10))
        self.emails = []

        self.frame_enderecos = ctk.CTkFrame(self)
        self.frame_enderecos.pack(fill="x", padx=20, pady=(0, 10))
        self.enderecos = []

        self._editing_id = None
        # if editing existing contato, preencher campos
        if contato is not None:
            self._fill_from_contato(contato)

    def adicionar_telefone(self):
        self._create_dynamic_field(self.frame_telefones, "Telefone", self.telefones)

    def adicionar_email(self):
        self._create_dynamic_field(self.frame_emails, "Email", self.emails)

    def adicionar_endereco(self):
        self._create_dynamic_field(self.frame_enderecos, "Endereço", self.enderecos)

    def _create_dynamic_field(self, container, placeholder, entries_list):
        row = ctk.CTkFrame(container)

        entry = ctk.CTkEntry(
            row,
            width=340,
            placeholder_text=placeholder
        )
        entry.pack(side="left", fill="x", expand=True, pady=5)

        remover = ctk.CTkButton(
            row,
            text="Remover",
            width=90,
            command=lambda: self._remove_dynamic_field(row, entry, entries_list)
        )
        remover.pack(side="right", padx=(10, 0), pady=5)

        row.pack(fill="x")
        entries_list.append(entry)

    def _remove_dynamic_field(self, row, entry, entries_list):
        if entry in entries_list:
            entries_list.remove(entry)
        row.destroy()

    def _collect_values(self):
        nome = self.nome.get().strip()

        telefones = []
        # include single entry if filled
        if hasattr(self, 'telefone') and self.telefone.get().strip():
            telefones.append(self.telefone.get().strip())
        for e in self.telefones:
            v = e.get().strip()
            if v:
                telefones.append(v)

        emails = []
        if hasattr(self, 'email') and self.email.get().strip():
            emails.append(self.email.get().strip())
        for e in self.emails:
            v = e.get().strip()
            if v:
                emails.append(v)

        enderecos = []
        if hasattr(self, 'endereco') and self.endereco.get().strip():
            enderecos.append(self.endereco.get().strip())
        for e in self.enderecos:
            v = e.get().strip()
            if v:
                enderecos.append(v)

        return nome, telefones, emails, enderecos

    def _on_salvar(self):
        nome, telefones, emails, enderecos = self._collect_values()
        categoria = self.categoria.get().strip() if hasattr(self, 'categoria') else ''

        from utils import sucesso, erro

        if not nome:
            erro('Preencha o nome do contato')
            return

        if not categoria or categoria == 'Selecione':
            erro('Selecione uma categoria')
            return

        if not telefones:
            erro('Preencha pelo menos um telefone')
            return

        if not emails:
            erro('Preencha pelo menos um email')
            return

        if not enderecos:
            erro('Preencha pelo menos um endereço')
            return

        contato = Contato(
            nome=nome,
            categoria=categoria,
            telefones=[Telefone(numero=n) for n in telefones],
            emails=[Email(endereco=e) for e in emails],
            enderecos=[Endereco(rua=ad) for ad in enderecos],
            id=getattr(self, '_editing_id', None)
        )

        service = ContatoService()
        try:
            novo_id = service.salvar(contato)
            contato.id = novo_id
            sucesso('Contato salvo com sucesso')
        except Exception as e:
            erro('Erro ao salvar contato: ' + str(e))
            return

        # limpar campos
        self.nome.delete(0, 'end')
        self.categoria.set('Selecione')
        if hasattr(self, 'telefone'):
            self.telefone.delete(0, 'end')
        if hasattr(self, 'email'):
            self.email.delete(0, 'end')
        if hasattr(self, 'endereco'):
            self.endereco.delete(0, 'end')
        for lst in (self.telefones + self.emails + self.enderecos):
            lst.destroy()
        self.telefones.clear(); self.emails.clear(); self.enderecos.clear()

    def _fill_from_contato(self, contato):
        # preenche campos com dados do contato para edição
        self.nome.delete(0, 'end')
        self.nome.insert(0, contato.nome)

        self.categoria.set(contato.categoria or 'Selecione')

        # limpar campos base antes de preencher
        self.telefone.delete(0, 'end')
        self.email.delete(0, 'end')
        self.endereco.delete(0, 'end')

        if contato.telefones:
            self.telefone.insert(0, contato.telefones[0].numero)
            for t in contato.telefones[1:]:
                entry = ctk.CTkEntry(self.frame_telefones, width=400, placeholder_text='Telefone')
                entry.insert(0, t.numero)
                entry.pack(pady=5, fill='x')
                self.telefones.append(entry)

        if contato.emails:
            self.email.insert(0, contato.emails[0].endereco)
            for e in contato.emails[1:]:
                entry = ctk.CTkEntry(self.frame_emails, width=400, placeholder_text='Email')
                entry.insert(0, e.endereco)
                entry.pack(pady=5, fill='x')
                self.emails.append(entry)

        if contato.enderecos:
            self.endereco.insert(0, contato.enderecos[0].rua)
            for ed in contato.enderecos[1:]:
                entry = ctk.CTkEntry(self.frame_enderecos, width=400, placeholder_text='Endereço')
                entry.insert(0, ed.rua)
                entry.pack(pady=5, fill='x')
                self.enderecos.append(entry)
        
        # preserve id for update
        self._editing_id = contato.id