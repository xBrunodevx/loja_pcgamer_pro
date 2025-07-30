import os
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import itertools

# -----------------------------------------
# CONFIGURAÇÕES INICIAIS
# -----------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USUARIOS_FILE = os.path.join(BASE_DIR, "usuarios.json")
PRODUTOS_FILE = os.path.join(BASE_DIR, "produtos.json")

def criar_arquivos_padrao():
    if not os.path.exists(USUARIOS_FILE):
        usuarios_iniciais = {"admin": "1234"}
        with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
            json.dump(usuarios_iniciais, f, indent=4, ensure_ascii=False)
    if not os.path.exists(PRODUTOS_FILE):
        produtos_iniciais = [
            {"nome": "Placa de Vídeo RTX 3070", "descricao": "8GB GDDR6, Ray Tracing, excelente para jogos em 1440p.", "preco": 3499.90, "imagem": "rtx3070.jpg"},
            {"nome": "Processador Intel i9-14900K", "descricao": "24 núcleos, 32 threads, clock de até 6GHz.", "preco": 2999.90, "imagem": "i9_14900k.jpg"},
            {"nome": "Memória RAM 16GB DDR4", "descricao": "2x8GB, 3200MHz, CL16, excelente desempenho.", "preco": 399.99, "imagem": "ram16gb.jpg"},
            {"nome": "SSD NVMe 1TB", "descricao": "Leitura 3500MB/s, escrita 3000MB/s, super rápido.", "preco": 499.90, "imagem": "ssd1tb.jpg"},
            {"nome": "Fonte 750W 80 Plus Gold", "descricao": "Alta eficiência, ideal para PCs gamers potentes.", "preco": 699.00, "imagem": "fonte750w.jpg"},
            {"nome": "Gabinete Gamer RGB", "descricao": "Vidro temperado, iluminação RGB frontal.", "preco": 459.90, "imagem": "gabinete_rgb.jpg"},
            {"nome": "Headset HyperX", "descricao": "Som 7.1 virtual, microfone destacável.", "preco": 299.90, "imagem": "headset_hyperx.jpg"}
        ]
        with open(PRODUTOS_FILE, "w", encoding="utf-8") as f:
            json.dump(produtos_iniciais, f, indent=4, ensure_ascii=False)

criar_arquivos_padrao()

with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
    usuarios = json.load(f)

with open(PRODUTOS_FILE, "r", encoding="utf-8") as f:
    produtos = json.load(f)

# -----------------------------------------
# Função para efeito hover nos botões
# -----------------------------------------
def add_hover_effect(botao, cor_hover, cor_normal):
    botao.bind("<Enter>", lambda e: botao.config(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.config(bg=cor_normal))

# -----------------------------------------
# Classe Principal
# -----------------------------------------
class LojaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Loja PC Gamer PRO")
        self.configure(bg="#0f0f0f")
        self.geometry("600x500")
        self.resizable(False, False)
        self.usuario_logado = None
        self.carrinho = []

        self.frames = {}
        for Tela in (LoginFrame, MenuFrame, ProdutosFrame, CarrinhoFrame, FinalizarFrame):
            frame = Tela(self)
            self.frames[Tela] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(LoginFrame)

    def show_frame(self, cont):
        self.frames[cont].tkraise()

    def login(self, usuario, senha):
        if usuario in usuarios and usuarios[usuario] == senha:
            self.usuario_logado = usuario
            messagebox.showinfo("Login", f"Bem-vindo(a), {usuario}!")
            self.frames[ProdutosFrame].refresh_produtos()
            self.frames[CarrinhoFrame].refresh_carrinho()
            self.show_frame(MenuFrame)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def cadastrar(self, usuario, senha):
        if usuario in usuarios:
            messagebox.showerror("Erro", "Usuário já existe.")
        else:
            usuarios[usuario] = senha
            with open(USUARIOS_FILE, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

    def logout(self):
        self.usuario_logado = None
        self.carrinho.clear()
        self.frames[LoginFrame].clear_entries()
        self.show_frame(LoginFrame)

    def adicionar_ao_carrinho(self, produto):
        self.carrinho.append(produto)
        messagebox.showinfo("Carrinho", f"{produto['nome']} adicionado ao carrinho.")
        self.frames[CarrinhoFrame].refresh_carrinho()

    def remover_do_carrinho(self, index):
        if 0 <= index < len(self.carrinho):
            produto = self.carrinho.pop(index)
            messagebox.showinfo("Carrinho", f"{produto['nome']} removido do carrinho.")
            self.frames[CarrinhoFrame].refresh_carrinho()

    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showwarning("Carrinho", "Seu carrinho está vazio.")
            return
        total = sum(p["preco"] for p in self.carrinho)
        with open(os.path.join(BASE_DIR, f"pedido_{self.usuario_logado}.txt"), "w", encoding="utf-8") as f:
            for p in self.carrinho:
                f.write(f"{p['nome']} - R$ {p['preco']:.2f}\n")
            f.write(f"\nTotal: R$ {total:.2f}\n")
        messagebox.showinfo("Compra Finalizada", "Compra registrada com sucesso!")
        self.carrinho.clear()
        self.frames[CarrinhoFrame].refresh_carrinho()
        self.show_frame(MenuFrame)

# -----------------------------------------
# Telas / Frames
# -----------------------------------------

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#0f0f0f")

        # Título com animação de cores
        self.titulo = tk.Label(self, text="LOGIN", font=("Arial", 24, "bold"), fg="#00ffea", bg="#0f0f0f")
        self.titulo.pack(pady=40)
        self.cores = itertools.cycle(["#00ffea", "#00ffaa", "#00ff6a", "#00ffea"])
        self.animar_titulo()

        # Entrada usuário
        tk.Label(self, text="Usuário:", fg="white", bg="#0f0f0f", font=("Arial", 14)).pack(pady=(10,5))
        self.entry_usuario = tk.Entry(self, font=("Arial", 14))
        self.entry_usuario.pack(pady=5)

        # Entrada senha
        tk.Label(self, text="Senha:", fg="white", bg="#0f0f0f", font=("Arial", 14)).pack(pady=5)
        self.entry_senha = tk.Entry(self, show="*", font=("Arial", 14))
        self.entry_senha.pack(pady=5)

        # Botões login e cadastro
        btn_frame = tk.Frame(self, bg="#0f0f0f")
        btn_frame.pack(pady=20)

        self.btn_login = tk.Button(btn_frame, text="Login", bg="#00ff6a", fg="black", font=("Arial", 12), width=10, command=self.fazer_login)
        self.btn_login.pack(side="left", padx=10)
        add_hover_effect(self.btn_login, "#00ffaa", "#00ff6a")

        self.btn_cadastrar = tk.Button(btn_frame, text="Cadastrar", bg="#00ffea", fg="black", font=("Arial", 12), width=10, command=self.fazer_cadastro)
        self.btn_cadastrar.pack(side="left", padx=10)
        add_hover_effect(self.btn_cadastrar, "#00ffff", "#00ffea")

    def animar_titulo(self):
        cor = next(self.cores)
        self.titulo.config(fg=cor)
        self.after(500, self.animar_titulo)

    def fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        self.master.login(usuario, senha)

    def fazer_cadastro(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        if usuario == "" or senha == "":
            messagebox.showwarning("Erro", "Usuário e senha não podem ser vazios.")
            return
        self.master.cadastrar(usuario, senha)

    def clear_entries(self):
        self.entry_usuario.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)


class MenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#0f0f0f")

        self.titulo = tk.Label(self, text="MENU PRINCIPAL", font=("Arial", 24, "bold"), fg="#00ffea", bg="#0f0f0f")
        self.titulo.pack(pady=40)
        self.cores = itertools.cycle(["#00ffea", "#00ffaa", "#00ff6a", "#00ffea"])
        self.animar_titulo()

        btns_frame = tk.Frame(self, bg="#0f0f0f")
        btns_frame.pack(pady=20)

        self.btn_produtos = tk.Button(btns_frame, text="Ver Produtos", bg="#00ff6a", fg="black", font=("Arial", 14), width=20, height=2, command=lambda: master.show_frame(ProdutosFrame))
        self.btn_produtos.pack(pady=10)
        add_hover_effect(self.btn_produtos, "#00ffaa", "#00ff6a")

        self.btn_carrinho = tk.Button(btns_frame, text="Ver Carrinho", bg="#00ffea", fg="black", font=("Arial", 14), width=20, height=2, command=lambda: master.show_frame(CarrinhoFrame))
        self.btn_carrinho.pack(pady=10)
        add_hover_effect(self.btn_carrinho, "#00ffff", "#00ffea")

        self.btn_finalizar = tk.Button(btns_frame, text="Finalizar Compra", bg="#0099ff", fg="black", font=("Arial", 14), width=20, height=2, command=lambda: master.show_frame(FinalizarFrame))
        self.btn_finalizar.pack(pady=10)
        add_hover_effect(self.btn_finalizar, "#33bbff", "#0099ff")

        self.btn_logout = tk.Button(btns_frame, text="Logout", bg="#ff0033", fg="black", font=("Arial", 14), width=20, height=2, command=master.logout)
        self.btn_logout.pack(pady=10)
        add_hover_effect(self.btn_logout, "#ff3366", "#ff0033")

    def animar_titulo(self):
        cor = next(self.cores)
        self.titulo.config(fg=cor)
        self.after(500, self.animar_titulo)


class ProdutosFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#0f0f0f")

        self.titulo = tk.Label(self, text="PRODUTOS DISPONÍVEIS", font=("Arial", 20, "bold"), fg="#00ffea", bg="#0f0f0f")
        self.titulo.pack(pady=10)
        self.cores = itertools.cycle(["#00ffea", "#00ffaa", "#00ff6a", "#00ffea"])
        self.animar_titulo()

        self.canvas = tk.Canvas(self, bg="#0f0f0f", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#0f0f0f")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)

        self.btn_voltar = tk.Button(self, text="Voltar", bg="#ff0033", fg="black", font=("Arial", 12), command=lambda: master.show_frame(MenuFrame))
        self.btn_voltar.pack(pady=10)
        add_hover_effect(self.btn_voltar, "#ff3366", "#ff0033")

    def animar_titulo(self):
        cor = next(self.cores)
        self.titulo.config(fg=cor)
        self.after(500, self.animar_titulo)

    def refresh_produtos(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for produto in produtos:
            frame_prod = tk.Frame(self.scrollable_frame, bg="#121212", bd=2, relief="ridge", padx=10, pady=10)
            frame_prod.pack(padx=10, pady=5, fill="x")

            tk.Label(frame_prod, text=produto["nome"], font=("Arial", 16, "bold"), fg="#00ff6a", bg="#121212").pack(anchor="w")
            tk.Label(frame_prod, text=produto["descricao"], font=("Arial", 12), fg="white", bg="#121212", wraplength=450, justify="left").pack(anchor="w", pady=5)
            tk.Label(frame_prod, text=f"Preço: R$ {produto['preco']:.2f}", font=("Arial", 14, "bold"), fg="#00ffaa", bg="#121212").pack(anchor="w", pady=5)

            caminho_imagem = os.path.join(BASE_DIR, "imagens", produto["imagem"])
            try:
                img = Image.open(caminho_imagem)
                img = img.resize((150, 150))
                foto = ImageTk.PhotoImage(img)
                label_img = tk.Label(frame_prod, image=foto, bg="#121212")
                label_img.image = foto
                label_img.pack(side="right", padx=10)
            except:
                tk.Label(frame_prod, text="[Imagem não disponível]", fg="red", bg="#121212").pack(side="right", padx=10)

            btn_adicionar = tk.Button(frame_prod, text="Adicionar ao Carrinho", bg="#00ff6a", fg="black", font=("Arial", 12), command=lambda p=produto: self.master.adicionar_ao_carrinho(p))
            btn_adicionar.pack(side="bottom", pady=10)
            add_hover_effect(btn_adicionar, "#00ffaa", "#00ff6a")


class CarrinhoFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#0f0f0f")

        self.titulo = tk.Label(self, text="SEU CARRINHO", font=("Arial", 20, "bold"), fg="#00ffea", bg="#0f0f0f")
        self.titulo.pack(pady=10)
        self.cores = itertools.cycle(["#00ffea", "#00ffaa", "#00ff6a", "#00ffea"])
        self.animar_titulo()

        self.lista_carrinho = tk.Listbox(self, font=("Arial", 12))
        self.lista_carrinho.pack(fill="both", expand=True, padx=10)

        btn_frame = tk.Frame(self, bg="#0f0f0f")
        btn_frame.pack(pady=10)

        self.btn_remover = tk.Button(btn_frame, text="Remover Item", bg="#ff0033", fg="black", width=15, command=self.remover_item)
        self.btn_remover.pack(side="left", padx=5)
        add_hover_effect(self.btn_remover, "#ff3366", "#ff0033")

        self.btn_voltar = tk.Button(btn_frame, text="Voltar", bg="#00ff6a", fg="black", width=15, command=lambda: master.show_frame(MenuFrame))
        self.btn_voltar.pack(side="left", padx=5)
        add_hover_effect(self.btn_voltar, "#00ffaa", "#00ff6a")

    def animar_titulo(self):
        cor = next(self.cores)
        self.titulo.config(fg=cor)
        self.after(500, self.animar_titulo)

    def refresh_carrinho(self):
        self.lista_carrinho.delete(0, tk.END)
        for prod in self.master.carrinho:
            self.lista_carrinho.insert(tk.END, f"{prod['nome']} - R$ {prod['preco']:.2f}")

    def remover_item(self):
        selecionado = self.lista_carrinho.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return
        index = selecionado[0]
        self.master.remover_do_carrinho(index)


class FinalizarFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#0f0f0f")

        self.titulo = tk.Label(self, text="FINALIZAR COMPRA", font=("Arial", 20, "bold"), fg="#00ffea", bg="#0f0f0f")
        self.titulo.pack(pady=20)
        self.cores = itertools.cycle(["#00ffea", "#00ffaa", "#00ff6a", "#00ffea"])
        self.animar_titulo()

        self.label_total = tk.Label(self, text="Total: R$ 0.00", font=("Arial", 16, "bold"), fg="#00ff6a", bg="#0f0f0f")
        self.label_total.pack(pady=10)

        btn_frame = tk.Frame(self, bg="#0f0f0f")
        btn_frame.pack(pady=20)

        self.btn_confirmar = tk.Button(btn_frame, text="Confirmar Compra", bg="#00ff6a", fg="black", width=20, font=("Arial", 14), command=self.confirmar_compra)
        self.btn_confirmar.pack(side="left", padx=10)
        add_hover_effect(self.btn_confirmar, "#00ffaa", "#00ff6a")

        self.btn_voltar = tk.Button(btn_frame, text="Voltar", bg="#ff0033", fg="black", width=20, font=("Arial", 14), command=lambda: master.show_frame(MenuFrame))
        self.btn_voltar.pack(side="left", padx=10)
        add_hover_effect(self.btn_voltar, "#ff3366", "#ff0033")

    def animar_titulo(self):
        cor = next(self.cores)
        self.titulo.config(fg=cor)
        self.after(500, self.animar_titulo)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        total = sum(p["preco"] for p in self.master.carrinho)
        self.label_total.config(text=f"Total: R$ {total:.2f}")

    def confirmar_compra(self):
        self.master.finalizar_compra()


if __name__ == "__main__":
    app = LojaApp()
    app.mainloop()
