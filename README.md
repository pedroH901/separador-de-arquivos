# 🗄️ Gerenciador de Arquivos em Python

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)

Um utilitário de linha de comando e interface gráfica para organizar arquivos por extensão, criar backups compactados e gerar relatórios de diretórios.

---

## 📖 Cenário

> Uma empresa de banco de dados chamada DWC sofreu um ataque de hackers que invadiram seus sistemas, bagunçando todo o conteúdo armazenado. Após buscar uma solução, a DWC encontrou nossa equipe e solicitou ajuda para resolver o problema. Aceitamos o desafio e criamos esta ferramenta para restaurar a ordem.

---

## ✨ Funcionalidades Principais

* **Organização Automática**: Move arquivos para pastas nomeadas de acordo com suas extensões (ex: `documentos`, `imagens`, `videos`).
* **Criação de Backups**: Gera um arquivo `.zip` contendo todos os arquivos do diretório especificado, com um timestamp para controle de versão.
* **Geração de Relatórios**: Cria um arquivo de texto (`.txt`) com um resumo do conteúdo do diretório, incluindo a contagem de arquivos por extensão.
* **Interface Dupla**: Pode ser utilizado tanto através de uma interface gráfica simples (GUI) com Tkinter quanto via linha de comando (CLI) para automação e scripting.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Tkinter** para a interface gráfica (biblioteca padrão do Python)
* **Bibliotecas Nativas:** `os`, `shutil`, `datetime`, `zipfile`, `logging`, `argparse`.

---

## 🚀 Como Utilizar

Não é necessária nenhuma instalação de pacotes externos. Apenas clone este repositório:

```bash
git clone https://github.com/gabriel-wav/separador-de-arquivos.git
cd separador-de-arquivos
```

Você pode usar a ferramenta de duas maneiras:

### 1. Utilizando a Interface Gráfica (GUI)

Esta é a maneira mais fácil e visual de usar o programa.

Execute o seguinte comando no seu terminal:

```bash
python interface.py
```

Uma janela se abrirá com as seguintes opções:

- **Selecionar Pasta**: Clique para escolher o diretório que você deseja gerenciar.
- **Organizar Arquivos**: Após selecionar uma pasta, clique para mover os arquivos para subpastas por tipo.
- **Criar Backup**: Cria um backup `.zip` da pasta selecionada.
- **Gerar Relatório**: Cria um arquivo `.txt` com as estatísticas da pasta.

### 2. Utilizando a Linha de Comando (CLI)

Para usuários avançados ou para uso em scripts, você pode usar `separadorDeArquivos.py` diretamente do terminal.

**Estrutura do comando:**
```bash
python separadorDeArquivos.py [comando] --diretorio "/caminho/para/sua/pasta"
```

**Comandos disponíveis:**

#### `organizar`: Organiza os arquivos no diretório especificado.

```bash
python separadorDeArquivos.py organizar --diretorio "C:\Users\SeuUsuario\Downloads"
```

#### `backup`: Cria um backup do diretório. Você pode especificar um nome para o arquivo de backup.

```bash
# Backup com nome padrão (ex: backup_2025-06-08_093000.zip)
python separadorDeArquivos.py backup --diretorio "C:\Users\SeuUsuario\Documentos"

# Backup com nome personalizado
python separadorDeArquivos.py backup --diretorio "C:\Users\SeuUsuario\Documentos" --nome "Backup_Projeto_Final"
```

#### `relatorio`: Gera um relatório de conteúdo do diretório.

```bash
python separadorDeArquivos.py relatorio --diretorio "C:\Users\SeuUsuario\Imagens"
```

---

## 👨‍💻 Autores e Contribuições

Este projeto foi desenvolvido em equipe, com as seguintes contribuições:

**Antonio Ferreira** ([@Antoniojferreira3](https://github.com/Antoniojferreira3)):
- Desenvolvimento da classe principal (`__init__`).
- Criação da interface gráfica com Tkinter (`interface.py`).

**Danilo Gutierre** ([@danilinhotj187](https://github.com/danilinhotj187)):
- Implementação da função de organização de arquivos por extensão (`organizar_por_extensao`).

**Gabriel Fernandes** ([@gabriel-wav](https://github.com/gabriel-wav)):
- Implementação da função de criação de backups em formato `.zip` (`criar_backup`).

**Pedro Henrique** ([@pedroH901](https://github.com/pedroH901)):
- Implementação da função de geração de relatórios (`gerar_relatorio`).
- Configuração da interface de linha de comando com `argparse`.
