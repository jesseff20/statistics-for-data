# -*- coding: utf-8 -*-
"""
Script Python para automação de tarefas, uma alternativa ao Makefile.

Uso:
  python tasks.py [tarefa]

Tarefas disponíveis:
  - setup: Instala as dependências.
  - format: Formata o código.
  - lint: Analisa o código com ruff.
  - test: Executa os testes.
  - data: Baixa os datasets.
  - notebook <nome>: Executa um notebook específico.
  - help: Mostra esta mensagem.
"""
import subprocess
import sys
import shutil
from pathlib import Path

# Pega o caminho para o executável do Python que está rodando o script
PYTHON_EXEC = sys.executable


def check_python_module(module_name):
    """Verifica se um módulo Python está disponível."""
    try:
        subprocess.run(
            [PYTHON_EXEC, "-c", f"import {module_name}"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_available_notebook_runner():
    """Retorna a melhor ferramenta disponível para executar notebooks."""
    # Verifica jupyter nbconvert primeiro (preferido)
    if check_python_module("jupyter") and check_python_module("nbconvert"):
        return "jupyter_nbconvert"

    # Verifica papermill como alternativa
    if check_python_module("papermill"):
        return "papermill"

    return None


def install_jupyter():
    """Instala jupyter se não estiver disponível."""
    print("--- Jupyter não encontrado. Instalando... ---")
    try:
        subprocess.run([PYTHON_EXEC, "-m", "pip", "install", "jupyter"], check=True)
        print("--- Jupyter instalado com sucesso! ---")
        return True
    except subprocess.CalledProcessError:
        print("ERRO: Falha ao instalar jupyter.", file=sys.stderr)
        return False


def convert_notebook_to_script(notebook_path):
    """Converte um notebook para um script Python executável."""
    try:
        import json

        with open(notebook_path, "r", encoding="utf-8") as f:
            notebook = json.load(f)

        script_lines = []
        script_lines.append(
            f"# Convertido automaticamente do notebook: {notebook_path.name}"
        )
        script_lines.append("# Execute este script como alternativa ao notebook\n")

        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "code":
                source = cell.get("source", [])
                if source:
                    script_lines.append("# " + "-" * 50)
                    # Junta as linhas de código da célula
                    if isinstance(source, list):
                        code = "".join(source)
                    else:
                        code = source
                    script_lines.append(code)
                    script_lines.append("")

        script_path = notebook_path.parent / f"{notebook_path.stem}_converted.py"
        with open(script_path, "w", encoding="utf-8") as f:
            f.write("\n".join(script_lines))

        return script_path

    except Exception as e:
        return None


def execute_notebook_as_script(notebook_path):
    """Executa um notebook convertendo-o para script Python."""
    script_path = convert_notebook_to_script(notebook_path)

    if not script_path:
        return False, "Erro ao converter notebook para script Python"

    try:
        print(f"--- Convertendo para script: {script_path.name} ---")
        result = subprocess.run(
            [PYTHON_EXEC, str(script_path)], check=True, cwd=notebook_path.parent
        )

        # Remove o arquivo de script temporário
        script_path.unlink()

        return True, "Notebook executado com sucesso como script Python"

    except subprocess.CalledProcessError as e:
        if script_path.exists():
            script_path.unlink()  # Remove o arquivo temporário
        return False, f"Erro ao executar script Python: {e}"


# Dicionário que mapeia o nome da tarefa ao comando a ser executado
COMMANDS = {
    "setup": {
        "description": "Instala as dependências do projeto e de desenvolvimento.",
        "command": f'"{PYTHON_EXEC}" -m pip install ".[dev]"',
    },
    "format": {
        "description": "Formata o código com black e isort.",
        "command": f'"{PYTHON_EXEC}" -m black . && "{PYTHON_EXEC}" -m isort .',
    },
    "lint": {
        "description": "Analisa o código com ruff.",
        "command": f'"{PYTHON_EXEC}" -m ruff check .',
    },
    "test": {
        "description": "Executa a suíte de testes com pytest.",
        "command": f'"{PYTHON_EXEC}" -m pytest',
    },
    "data": {
        "description": "Baixa os datasets de exemplo.",
        "command": f'"{PYTHON_EXEC}" run_loaders.py',
    },
}


def find_notebook_path(notebook_identifier):
    """Encontra o caminho completo de um notebook a partir de um identificador."""
    notebooks_dir = Path("notebooks")
    # Tenta encontrar por nome exato (ex: normal_distribution)
    for nb_path in notebooks_dir.rglob(f"**/{notebook_identifier}.ipynb"):
        return nb_path
    # Se não encontrou, tenta por parte do nome (ex: normal)
    for nb_path in notebooks_dir.rglob(f"**/*{notebook_identifier}*.ipynb"):
        return nb_path
    return None


def run_notebook(notebook_identifier):
    """Executa um notebook específico usando nbconvert."""
    nb_path = find_notebook_path(notebook_identifier)
    if not nb_path:
        print(
            f"\nERRO: Notebook '{notebook_identifier}' não encontrado.", file=sys.stderr
        )
        sys.exit(1)

    print(f"--- Executando notebook: {nb_path} ---")
    # Comando para executar o notebook no lugar, salvando a saída no mesmo diretório
    command = f'"{PYTHON_EXEC}" -m nbconvert --to notebook --execute "{nb_path}" --output-dir="{nb_path.parent}" --inplace'

    try:
        subprocess.run(command, check=True, shell=True)
        print(f"--- Notebook '{nb_path.name}' executado com sucesso! ---")
    except subprocess.CalledProcessError:
        print(f"\nERRO ao executar o notebook '{nb_path.name}'.", file=sys.stderr)
        sys.exit(1)


def run_task(task_name):
    """Executa uma tarefa específica do dicionário COMMANDS."""
    if task_name not in COMMANDS:
        print(f"\nERRO: Tarefa '{task_name}' não encontrada.", file=sys.stderr)
        print_help()
        sys.exit(1)

    task = COMMANDS[task_name]
    print(f"--- Executando tarefa: {task_name} ---")
    print(f"    {task['description']}")

    try:
        subprocess.run(task["command"], check=True, shell=True)
        print(f"--- Tarefa '{task_name}' concluída com sucesso! ---")
    except subprocess.CalledProcessError:
        print(f"\nERRO ao executar a tarefa '{task_name}'.", file=sys.stderr)
        sys.exit(1)


def print_help():
    """Imprime a mensagem de ajuda com as tarefas disponíveis."""
    print("\nUso: python tasks.py [tarefa] [argumentos]")
    print("\nTarefas disponíveis:")
    for name, details in COMMANDS.items():
        print(f"  {name:<10} - {details['description']}")
    print(
        f"  {'notebook':<10} - Executa um notebook específico. Ex: python tasks.py notebook normal_distribution"
    )


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print_help()
        sys.exit(0)

    task_to_run = args[0]

    if task_to_run == "notebook":
        if len(args) < 2:
            print(
                "\nERRO: O comando 'notebook' requer o nome do notebook como argumento.",
                file=sys.stderr,
            )
            print_help()
            sys.exit(1)
        notebook_identifier = args[1]
        run_notebook(notebook_identifier)
    else:
        run_task(task_to_run)
