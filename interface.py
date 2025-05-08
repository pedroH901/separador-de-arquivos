import tkinter as tk
from tkinter import filedialog, messagebox
from separadorDeArquivos import GerenciadorArquivos  # Importa sua classe original

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Arquivos")
        self.diretorio = ""

        # Botão para escolher a pasta
        tk.Button(root, text="Selecionar Pasta", command=self.selecionar_pasta).pack(pady=10)

        # Botões de ação
        tk.Button(root, text="Organizar Arquivos", command=self.organizar).pack(fill='x', padx=20, pady=5)
        tk.Button(root, text="Criar Backup", command=self.backup).pack(fill='x', padx=20, pady=5)
        tk.Button(root, text="Gerar Relatório", command=self.relatorio).pack(fill='x', padx=20, pady=5)

    def selecionar_pasta(self):
        self.diretorio = filedialog.askdirectory()
        if self.diretorio:
            messagebox.showinfo("Pasta Selecionada", f"Diretório selecionado:\n{self.diretorio}")

    def organizar(self):
        if not self.diretorio:
            return messagebox.showerror("Erro", "Nenhum diretório selecionado")
        g = GerenciadorArquivos(self.diretorio)
        g.organizar_por_extensao()
        messagebox.showinfo("Concluído", "Arquivos organizados com sucesso!")

    def backup(self):
        if not self.diretorio:
            return messagebox.showerror("Erro", "Nenhum diretório selecionado")
        g = GerenciadorArquivos(self.diretorio)
        caminho = g.criar_backup()
        if caminho:
            messagebox.showinfo("Backup criado", f"Arquivo salvo em:\n{caminho}")
        else:
            messagebox.showerror("Erro", "Falha ao criar backup")

    def relatorio(self):
        if not self.diretorio:
            return messagebox.showerror("Erro", "Nenhum diretório selecionado")
        g = GerenciadorArquivos(self.diretorio)
        caminho = g.gerar_relatorio()
        messagebox.showinfo("Relatório gerado", f"Arquivo salvo em:\n{caminho}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()