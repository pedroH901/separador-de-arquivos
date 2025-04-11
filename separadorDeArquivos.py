import os
import shutil
import datetime
import zipfile
import logging
from pathlib import Path
import json

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("FileManager")

class GerenciadorArquivos:
    def __init__(self, diretorio_base=None):
        """Inicializa o gerenciador com diretório base opcional."""
        self.diretorio_base = os.path.abspath(diretorio_base or os.getcwd())
        self.diretorio_backup = os.path.join(self.diretorio_base, "_backups")
        Path(self.diretorio_backup).mkdir(exist_ok=True)
        
        # Categorias de arquivo simplificadas
        self.categorias = {
            "documentos": [".pdf", ".doc", ".docx", ".txt"],
            "imagens": [".jpg", ".jpeg", ".png", ".gif"],
            "audio_video": [".mp3", ".mp4", ".wav", ".avi"],
            "planilhas": [".xls", ".xlsx", ".csv"],
            "codigo": [".py", ".js", ".html", ".css"],
            "outros": []
        }
    
    def organizar_por_extensao(self):
        """Organiza arquivos por extensão em subpastas."""
        # Criar pastas para categorias
        for categoria in self.categorias:
            Path(os.path.join(self.diretorio_base, categoria)).mkdir(exist_ok=True)
        
        # Processar arquivos no diretório
        arquivos_movidos = 0
        for item in os.listdir(self.diretorio_base):
            caminho_completo = os.path.join(self.diretorio_base, item)
            
            # Pular diretórios
            if os.path.isdir(caminho_completo):
                continue
                
            # Determinar categoria do arquivo
            _, extensao = os.path.splitext(item)
            extensao = extensao.lower()
            
            categoria_destino = "outros"
            for categoria, extensoes in self.categorias.items():
                if extensao in extensoes:
                    categoria_destino = categoria
                    break
            
            # Mover o arquivo
            try:
                destino = os.path.join(self.diretorio_base, categoria_destino, item)
                shutil.move(caminho_completo, destino)
                arquivos_movidos += 1
            except Exception as e:
                logger.error(f"Erro ao mover {item}: {e}")
        
        logger.info(f"Organização concluída: {arquivos_movidos} arquivos movidos")
        return arquivos_movidos
    
    def criar_backup(self, nome_backup=None):
        """Cria um backup compactado do diretório."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        nome_arquivo = f"{nome_backup or 'backup'}_{timestamp}.zip"
        caminho_backup = os.path.join(self.diretorio_backup, nome_arquivo)
        
        try:
            with zipfile.ZipFile(caminho_backup, 'w') as zip_file:
                for root, _, files in os.walk(self.diretorio_base):
                    # Pular a pasta de backups
                    if "_backups" in root:
                        continue
                        
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Adicionar com caminho relativo
                        zip_file.write(
                            file_path, 
                            os.path.relpath(file_path, self.diretorio_base)
                        )
            
            logger.info(f"Backup criado: {caminho_backup}")
            return caminho_backup
        except Exception as e:
            logger.error(f"Erro no backup: {e}")
            return None
    
    def gerar_relatorio(self):
        """Gera um relatório simples do diretório."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        caminho_relatorio = os.path.join(self.diretorio_base, f"relatorio_{timestamp}.txt")
        
        total_arquivos = 0
        total_diretorios = 0
        contagem_extensoes = {}
        
        for root, dirs, files in os.walk(self.diretorio_base):
            # Pular pasta de backups
            if "_backups" in root:
                continue
                
            total_diretorios += len(dirs)
            total_arquivos += len(files)
            
            for file in files:
                _, ext = os.path.splitext(file)
                ext = ext.lower() if ext else "(sem extensão)"
                
                if ext in contagem_extensoes:
                    contagem_extensoes[ext] += 1
                else:
                    contagem_extensoes[ext] = 1
        
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

# Exemplo de uso via linha de comando
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gerenciador de Arquivos")
    parser.add_argument("--diretorio", "-d", help="Diretório a processar")
    parser.add_argument("comando", choices=["organizar", "backup", "relatorio"], 
                        help="Comando a executar")
    parser.add_argument("--nome", "-n", help="Nome para o backup")
    
    args = parser.parse_args()
    
    gerenciador = GerenciadorArquivos(args.diretorio)
    
    if args.comando == "organizar":
        gerenciador.organizar_por_extensao()
    elif args.comando == "backup":
        gerenciador.criar_backup(args.nome)
    elif args.comando == "relatorio":
        gerenciador.gerar_relatorio()