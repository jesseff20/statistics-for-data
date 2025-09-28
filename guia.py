# -*- coding: utf-8 -*-
"""
Guia interativo e autônomo para configuração e exploração do projeto.
"""
import subprocess
import sys
import shutil
from pathlib import Path


def print_header(title):
    """Imprime um cabeçalho formatado."""
    print("\n" + "-" * 60)
    print(f"\t{title}")
    print("-" * 60)


def check_tool_available(tool_name):
    """Verifica se uma ferramenta está disponível no sistema."""
    return shutil.which(tool_name) is not None


def check_python_module(module_name):
    """Verifica se um módulo Python está disponível."""
    try:
        subprocess.run(
            [sys.executable, "-c", f"import {module_name}"],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_available_notebook_runners():
    """Retorna uma lista de ferramentas disponíveis para executar notebooks."""
    runners = []

    # Verifica jupyter nbconvert
    if check_python_module("jupyter") and check_python_module("nbconvert"):
        runners.append(
            {
                "name": "jupyter_nbconvert",
                "display": "Jupyter NBConvert",
                "description": "Executa notebooks usando jupyter nbconvert (recomendado)",
            }
        )

    # Verifica se papermill está disponível
    if check_python_module("papermill"):
        runners.append(
            {
                "name": "papermill",
                "display": "Papermill",
                "description": "Executa notebooks usando papermill",
            }
        )

    # Adiciona opção de instalação se nenhuma ferramenta estiver disponível
    if not runners:
        runners.append(
            {
                "name": "install_jupyter",
                "display": "Instalar Jupyter",
                "description": "Instalar jupyter para executar notebooks",
            }
        )

    return runners


def execute_notebook_with_available_tool(notebook_path, runner_type="auto"):
    """Executa um notebook usando a ferramenta disponível."""
    if runner_type == "auto":
        runners = get_available_notebook_runners()
        if not runners or runners[0]["name"] == "install_jupyter":
            return False, "Nenhuma ferramenta de execução de notebook disponível"
        runner_type = runners[0]["name"]

    try:
        if runner_type == "jupyter_nbconvert":
            command = [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                str(notebook_path),
                "--output-dir",
                str(notebook_path.parent),
                "--inplace",
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True, "Notebook executado com sucesso usando Jupyter NBConvert"

        elif runner_type == "papermill":
            command = [
                sys.executable,
                "-m",
                "papermill",
                str(notebook_path),
                str(notebook_path),  # Sobrescreve o arquivo original
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            return True, "Notebook executado com sucesso usando Papermill"

    except subprocess.CalledProcessError as e:
        return False, f"Erro ao executar notebook: {e}"

    return False, f"Ferramenta de execução '{runner_type}' não reconhecida"


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
        print(f"   Convertido para script: {script_path.name}")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True,
            cwd=notebook_path.parent,
        )

        # Remove o arquivo de script temporário
        script_path.unlink()

        if result.stdout:
            print("--- Saída do script ---")
            print(result.stdout)

        return True, "Notebook executado com sucesso como script Python"

    except subprocess.CalledProcessError as e:
        if script_path.exists():
            script_path.unlink()  # Remove o arquivo temporário
        return False, f"Erro ao executar script Python: {e}"


def run_command(command_list):
    """Executa um comando (como lista) e trata erros."""
    try:
        command_list[0] = sys.executable
        process = subprocess.run(
            command_list, check=True, text=True, capture_output=True
        )
        print(process.stdout)
        if process.stderr:
            print("Saída de erro padrão:")
            print(process.stderr)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        command_str = " ".join(command_list)
        print(f"\nERRO ao executar '{command_str}'.", file=sys.stderr)
        if isinstance(e, FileNotFoundError):
            print(
                f"O executável '{command_list[0]}' não foi encontrado.", file=sys.stderr
            )
        else:
            print(e.stderr, file=sys.stderr)
        return False


def list_and_run_notebooks_menu():
    """Lista os notebooks disponíveis e permite ao usuário escolher um para executar."""
    notebook_files = sorted(list(Path("notebooks").rglob("*.ipynb")))
    if not notebook_files:
        print("\nNenhum notebook encontrado na pasta 'notebooks/'.", file=sys.stderr)
        input("\nPressione Enter para voltar ao menu...")
        return

    while True:
        print_header("Executar Notebooks")

        # Verifica ferramentas disponíveis
        runners = get_available_notebook_runners()
        if runners and runners[0]["name"] != "install_jupyter":
            print(f"✓ Ferramenta de execução disponível: {runners[0]['display']}")
        else:
            print("⚠ Nenhuma ferramenta de execução de notebook encontrada!")
            print("   Para executar notebooks, você precisa instalar jupyter:")
            print(f"   {sys.executable} -m pip install jupyter")
            print()

        print("Notebooks disponíveis:")
        for i, nb_path in enumerate(notebook_files):
            # Exibe o caminho relativo para clareza
            print(f"  {i+1}. {nb_path.relative_to(Path('notebooks'))}")

        print("\n  0. Voltar ao menu principal")

        if runners and runners[0]["name"] == "install_jupyter":
            print("  i. Instalar Jupyter automaticamente")

        choice = input(
            "\nDigite o número do notebook que deseja executar (ou 0 para voltar): "
        )

        if choice == "0":
            break
        elif (
            choice.lower() == "i"
            and runners
            and runners[0]["name"] == "install_jupyter"
        ):
            print("\nInstalando Jupyter...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "jupyter"], check=True
                )
                print("✓ Jupyter instalado com sucesso!")
                input("\nPressione Enter para continuar...")
                continue  # Volta ao início do loop para atualizar as ferramentas disponíveis
            except subprocess.CalledProcessError:
                print("❌ Erro ao instalar Jupyter.")
                input("\nPressione Enter para continuar...")
                continue

        try:
            index = int(choice) - 1
            if 0 <= index < len(notebook_files):
                selected_notebook = notebook_files[index]
                print(
                    f"\nExecutando: {selected_notebook.relative_to(Path('notebooks'))}"
                )

                # Executa o notebook usando a ferramenta disponível
                if not runners or runners[0]["name"] == "install_jupyter":
                    print(
                        "❌ Jupyter não disponível. Tentando executar como script Python..."
                    )
                    success, message = execute_notebook_as_script(selected_notebook)
                    if success:
                        print(f"\n✓ {message}")
                    else:
                        print(f"\n❌ {message}")
                        print("   Recomendações:")
                        print("   1. Instale jupyter: python -m pip install jupyter")
                        print("   2. Ou abra o notebook manualmente em um editor")
                else:
                    success, message = execute_notebook_with_available_tool(
                        selected_notebook
                    )
                    if success:
                        print(f"\n✓ {message}")
                    else:
                        print(f"\n❌ {message}")
                        print("   Tentando executar como script Python...")
                        success, message = execute_notebook_as_script(selected_notebook)
                        if success:
                            print(f"\n✓ {message}")
                        else:
                            print(f"\n❌ {message}")

                input("\nPressione Enter para continuar...")
            else:
                print("\nOpção inválida. Por favor, digite um número válido.")
        except ValueError:
            print("\nEntrada inválida. Por favor, digite um número.")


def explore_project_menu():
    """Apresenta um menu interativo para explorar a estrutura do projeto."""
    while True:
        print_header("Menu de Exploração do Projeto")
        print("Escolha uma opção para entender melhor cada parte do projeto:")
        print("  1. Estrutura de Pastas")
        print("  2. Notebooks de Análise")
        print("  3. Scripts Reutilizáveis (pasta src/)")
        print("  4. Qualidade e Automação (Makefile, CI, etc.)")
        print("  5. Executar um Notebook")  # Nova opção
        print("  6. Sair")  # Número da opção de sair alterado

        choice = input("\nDigite o número da sua escolha: ")

        if choice == "6":  # Número da opção de sair alterado
            print("\nSaindo do menu de exploração. Até mais!")
            break

        elif choice == "1":
            print_header("1. Estrutura de Pastas")
            print(
                "A organização das pastas segue um padrão profissional para projetos de dados:"
            )
            print("- data/: Armazena os dados. É subdividida em:")
            print("  - raw: Dados brutos, nunca modificados.")
            print("  - external: Dados de fontes externas (APIs, etc.).")
            print("  - processed: Dados limpos e prontos para análise.")
            print(
                "- notebooks/: Contém os Jupyter Notebooks, onde as análises exploratórias são feitas."
            )
            print(
                "- src/: Guarda código Python reutilizável (funções, classes). Separar o código aqui evita duplicação e facilita os testes."
            )
            print(
                "- tests/: Contém testes automatizados para garantir que o código na pasta src/ funciona como esperado."
            )
            print(
                "- .github/workflows: Define a Integração Contínua (CI), que roda testes e validações automaticamente."
            )
            input("\nPressione Enter para voltar ao menu...")

        elif choice == "2":
            print_header("2. Notebooks de Análise")
            print("Os notebooks são o coração das análises, organizados por tema:")
            print(
                "- 01_probability: Explora distribuições estatísticas fundamentais (Normal, Poisson, Binomial) com dados práticos."
            )
            print(
                "- 02_hypothesis_tests: Aplica testes de hipóteses comuns (t-test, ANOVA, Qui-quadrado) para responder perguntas de negócio."
            )
            print(
                "- 03_regression: Foca na construção de modelos preditivos (Regressão Linear e Logística) e na interpretação de seus resultados."
            )
            input("\nPressione Enter para voltar ao menu...")

        elif choice == "3":
            print_header("3. Scripts Reutilizáveis (pasta src/)")
            print(
                "A pasta src/ transforma o projeto de uma simples análise em um software robusto:"
            )
            print(
                "- src/data: Contém scripts para baixar (`loaders.py`) e limpar (`preprocess.py`) os dados de forma programática."
            )
            print(
                "- src/stats: Centraliza implementações de lógica estatística (`hypothesis.py`, `probability.py`) para serem usadas nos notebooks."
            )
            print(
                "- src/models: Estrutura o treinamento (`train.py`) e a avaliação (`evaluate.py`) de modelos de machine learning."
            )
            print(
                "- src/viz: Guarda funções para criar visualizações (`plots.py`), garantindo um estilo consistente em todo o projeto."
            )
            input("\nPressione Enter para voltar ao menu...")

        elif choice == "4":
            print_header("4. Qualidade e Automação")
            print(
                "Ferramentas que garantem a qualidade e a reprodutibilidade do projeto:"
            )
            print(
                "- tasks.py: Fornece comandos simples (atalhos) para tarefas comuns, como `python tasks.py setup`, `python tasks.py test` e `python tasks.py lint`."
            )
            print(
                "- pyproject.toml: Arquivo central que define as dependências e a configuração do projeto."
            )
            print(
                "- ruff e black: Ferramentas de lint e formatação que garantem um código limpo, legível e sem erros de estilo."
            )
            print(
                "- CI (via .github/): Processo automatizado que roda no GitHub para garantir que cada nova alteração no código mantenha o projeto funcional e com qualidade."
            )
            input("\nPressione Enter para voltar ao menu...")

        elif choice == "5":  # Nova opção para executar notebooks
            list_and_run_notebooks_menu()

        else:
            print("\nOpção inválida. Por favor, tente novamente.")
            input("\nPressione Enter para continuar...")


def main():
    """Função principal do guia interativo."""
    print_header("Guia de Configuração e Comandos do Projeto (Instalação Global)")
    print("AVISO: As dependências serão instaladas globalmente no seu sistema.")

    # Passo 1: Instalar Dependências
    print_header("Passo 1: Instalar Dependências")
    print("Instalando todas as bibliotecas para o projeto e desenvolvimento...")
    if (
        input("\nDeseja instalar/atualizar as dependências agora? (s/n): ").lower()
        == "s"
    ):
        install_command = [
            "python",
            "-m",
            "pip",
            "install",
            "--only-binary=:all:",
            ".[dev]",
        ]
        if not run_command(install_command):
            print("\n=> Falha na instalação das dependências.", file=sys.stderr)
            sys.exit(1)
        print("\n=> Sucesso! Dependências instaladas.")

    # Passo 2: Baixar os Dados
    print_header("Passo 2: Baixar os Dados")
    print("Executando o script para baixar os datasets de exemplo da internet.")
    if input("\nDeseja baixar os dados agora? (s/n): ").lower() == "s":
        data_command = ["python", "run_loaders.py"]
        if not run_command(data_command):
            print("\n=> Falha no download dos dados.", file=sys.stderr)
            sys.exit(1)
        print("\n=> Sucesso! Dados baixados.")

    # Passo 3: Rodar os Testes
    print_header("Passo 3: Rodar os Testes")
    print("Executando a suíte de testes com pytest.")
    if input("\nDeseja rodar os testes agora? (s/n): ").lower() == "s":
        test_command = ["python", "-m", "pytest"]
        run_command(test_command)

    # Passo 4: Comandos de Qualidade de Código
    print_header("Passo 4: Comandos de Qualidade de Código")
    print("- Linter: Verifica o código em busca de erros e problemas de estilo.")
    print("- Formatador: Formata todo o código automaticamente.")
    if input("\nDeseja rodar o linter ('ruff') agora? (s/n): ").lower() == "s":
        run_command(["python", "-m", "ruff", "check", "."])
    if input("\nDeseja rodar o formatador ('black') agora? (s/n): ").lower() == "s":
        run_command(["python", "-m", "black", "."])

    print_header("Configuração e Verificação Concluídas!")
    print("Seu projeto está pronto para ser usado com o Python do seu sistema.")

    # Inicia o menu de exploração
    explore_project_menu()


if __name__ == "__main__":
    main()
