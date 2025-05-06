# os: usado para interagir com o sistema operacional, como navegar por pastas e checar se arquivos existem.
import os

# shutil: usado para mover arquivos de um lugar para outro.
import shutil

# datetime: usado para trabalhar com datas e horas, como criar timestamps para backups.
import datetime

# zipfile: usado para criar arquivos zip, que são compactados para economizar espaço.
import zipfile

# logging: usado para registrar mensagens de log, como erros e informações sobre o que o programa está fazendo.
import logging

# pathlib: usado para manipular caminhos de arquivos de forma mais fácil e legível.
from pathlib import Path

# json: usado para trabalhar com arquivos JSON, que são um formato comum para armazenar dados estruturados.
import json

# Configuração básica do sistema de log para mostrar data e mensagem de cada evento
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("FileManager")  # Cria um registrador de log com o nome "FileManager"

# Classe principal que gerencia arquivos no sistema
class GerenciadorArquivos:
    def __init__(self, diretorio_base=None):
        """Inicializa o gerenciador com diretório base opcional."""
        
        # Define o diretório base como o atual ou como o passado pelo usuário
        self.diretorio_base = os.path.abspath(diretorio_base or os.getcwd())
        
        # Define a pasta onde serão salvos os backups
        self.diretorio_backup = os.path.join(self.diretorio_base, "_backups")
        
        # Cria a pasta de backup se ela ainda não existir
        Path(self.diretorio_backup).mkdir(exist_ok=True)
        
        # Define categorias para organizar os arquivos por tipo/extensão
        self.categorias = {
            "documentos": [".pdf", ".doc", ".docx", ".txt"],
            "imagens": [".jpg", ".jpeg", ".png", ".gif"],
            "audio_video": [".mp3", ".mp4", ".wav", ".avi"],
            "planilhas": [".xls", ".xlsx", ".csv"],
            "codigo": [".py", ".js", ".html", ".css"],
            "outros": []  # Onde vão parar os arquivos que não pertencem a nenhuma categoria
        }

    def organizar_por_extensao(self):
        """Organiza arquivos por extensão em subpastas."""
        
        # Cria subpastas para cada categoria, se ainda não existirem
        for categoria in self.categorias:
            Path(os.path.join(self.diretorio_base, categoria)).mkdir(exist_ok=True)
        
        arquivos_movidos = 0  # Contador de arquivos movidos
        
        # Percorre todos os arquivos e pastas do diretório base
        for item in os.listdir(self.diretorio_base):
            caminho_completo = os.path.join(self.diretorio_base, item)
            
            # Ignora se o item for uma pasta (só processa arquivos)
            if os.path.isdir(caminho_completo):
                continue
            
            # Pega a extensão do arquivo
            _, extensao = os.path.splitext(item)
            extensao = extensao.lower()
            
            # Define a categoria padrão como "outros"
            categoria_destino = "outros"
            
            # Verifica a qual categoria o arquivo pertence
            for categoria, extensoes in self.categorias.items():
                if extensao in extensoes:
                    categoria_destino = categoria
                    break
            
            try:
                # Define o caminho de destino e move o arquivo
                destino = os.path.join(self.diretorio_base, categoria_destino, item)
                shutil.move(caminho_completo, destino)
                arquivos_movidos += 1
            except Exception as e:
                # Em caso de erro, registra no log
                logger.error(f"Erro ao mover {item}: {e}")
        
        # Log final com total de arquivos organizados
        logger.info(f"Organização concluída: {arquivos_movidos} arquivos movidos")
        return arquivos_movidos

    def criar_backup(self, nome_backup=None):
        """Cria um backup compactado do diretório."""
        
        # Gera timestamp com data e hora
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        
        # Define nome do arquivo de backup
        nome_arquivo = f"{nome_backup or 'backup'}_{timestamp}.zip"
        caminho_backup = os.path.join(self.diretorio_backup, nome_arquivo)
        
        try:
            # Cria o arquivo ZIP
            with zipfile.ZipFile(caminho_backup, 'w') as zip_file:
                for root, _, files in os.walk(self.diretorio_base):
                    # Ignora a pasta de backups para evitar incluir ela no próprio backup
                    if "_backups" in root:
                        continue
                        
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        # Adiciona o arquivo ao ZIP com caminho relativo
                        zip_file.write(
                            file_path, 
                            os.path.relpath(file_path, self.diretorio_base)
                        )
            
            # Log de sucesso
            logger.info(f"Backup criado: {caminho_backup}")
            return caminho_backup
        except Exception as e:
            # Log de erro
            logger.error(f"Erro no backup: {e}")
            return None

    def gerar_relatorio(self):
        """Gera um relatório simples do diretório."""
        
        # Timestamp para o nome do relatório
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        caminho_relatorio = os.path.join(self.diretorio_base, f"relatorio_{timestamp}.txt")
        
        total_arquivos = 0  # Contador de arquivos
        total_diretorios = 0  # Contador de pastas
        contagem_extensoes = {}  # Dicionário para contar por tipo de extensão
        
        # Percorre todo o diretório
        for root, dirs, files in os.walk(self.diretorio_base):
            if "_backups" in root:
                continue  # Ignora a pasta de backups
            
            total_diretorios += len(dirs)
            total_arquivos += len(files)
            
            for file in files:
                _, ext = os.path.splitext(file)
                ext = ext.lower() if ext else "(sem extensão)"
                
                # Conta quantos arquivos de cada tipo existem
                if ext in contagem_extensoes:
                    contagem_extensoes[ext] += 1
                else:
                    contagem_extensoes[ext] = 1
        
        # Escreve o relatório em um arquivo .txt
        with open(caminho_relatorio, 'w', encoding='utf-8') as f:
            f.write(f"RELATÓRIO DE DIRETÓRIO: {self.diretorio_base}\n")
            f.write(f"Data: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"Total de arquivos: {total_arquivos}\n")
            f.write(f"Total de pastas: {total_diretorios}\n\n")
            
            f.write("DISTRIBUIÇÃO POR EXTENSÃO:\n")
            for ext, quantidade in sorted(contagem_extensoes.items()):
                f.write(f"{ext}: {quantidade} arquivo(s)\n")
        
        logger.info(f"Relatório gerado: {caminho_relatorio}")
        return caminho_relatorio

# Bloco que permite rodar o script direto do terminal com argumentos
if __name__ == "__main__":
    import argparse  # Biblioteca para interpretar comandos de terminal
    
    # Define os argumentos possíveis no terminal
    parser = argparse.ArgumentParser(description="Gerenciador de Arquivos")
    parser.add_argument("--diretorio", "-d", help="Diretório a processar")
    parser.add_argument("comando", choices=["organizar", "backup", "relatorio"], 
                        help="Comando a executar")
    parser.add_argument("--nome", "-n", help="Nome para o backup")
    
    args = parser.parse_args()  # Lê os argumentos fornecidos
    
    # Cria uma instância do gerenciador com o diretório informado
    gerenciador = GerenciadorArquivos(args.diretorio)
    
    # Executa o comando solicitado no terminal
    if args.comando == "organizar":
        gerenciador.organizar_por_extensao()
    elif args.comando == "backup":
        gerenciador.criar_backup(args.nome)
    elif args.comando == "relatorio":
        gerenciador.gerar_relatorio()
