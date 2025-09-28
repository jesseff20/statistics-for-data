# statistics-for-data: Estatística Aplicada

Repositório de portfólio focado em **estatística aplicada** com dados 100% abertos e código reprodutível. Projetado para demonstrar domínio prático em distribuições, testes de hipóteses, regressão e storytelling analítico.

---

## 🗺️ Mapa dos Estudos

Aqui você encontra os links para cada análise, organizada por tema:

*   **Probabilidade**
    *   `notebooks/01_probability/normal_distribution.ipynb`
    *   `notebooks/01_probability/poisson_counts.ipynb`
    *   `notebooks/01_probability/binomial_abtest.ipynb`
*   **Testes de Hipóteses**
    *   `notebooks/02_hypothesis_tests/ttest_ab_campaign.ipynb`
    *   `notebooks/02_hypothesis_tests/anova_iris_species.ipynb`
    *   `notebooks/02_hypothesis_tests/chi_square_titanic.ipynb`
*   **Regressão**
    *   `notebooks/03_regression/linear_california_housing.ipynb`
    *   `notebooks/03_regression/logistic_telco_churn.ipynb`

---

## 🚀 Guia de Instalação e Comandos

**Aviso:** Este projeto instalará as dependências diretamente no seu sistema Python, sem usar um ambiente virtual.

Você tem duas maneiras de configurar o projeto:

### Modo Automático (Recomendado)

Use o nosso guia interativo. Ele instala as dependências e prepara o projeto.

```bash
python guia.py
```
Siga as instruções na tela.

### Modo Manual (via tasks.py)

Se preferir, você pode executar cada tarefa individualmente usando o script `tasks.py`.

Para ver todas as tarefas disponíveis, execute `python tasks.py help`.

1.  **Instalar Dependências:**
    ```bash
    python tasks.py setup
    ```

2.  **Baixar os Dados:**
    ```bash
    python tasks.py data
    ```

3.  **Executar Testes:**
    ```bash
    python tasks.py test
    ```

4.  **Verificar Qualidade do Código:**
    ```bash
    python tasks.py lint
    ```

5.  **Formatar o Código:**
    ```bash
    python tasks.py format
    ```

---

## 📂 Estrutura de Pastas

O projeto está organizado da seguinte forma:

```
statistics-for-data/
├─ README.md
├─ LICENSE
├─ pyproject.toml
├─ Makefile
├─ .gitignore
├─ .github/
│  └─ workflows/ci.yml
├─ data/
│  ├─ raw/
│  ├─ external/
│  └─ processed/
├─ notebooks/
│  ├─ 01_probability/
│  ├─ 02_hypothesis_tests/
│  └─ 03_regression/
├─ src/
│  ├─ data/
│  ├─ stats/
│  └─ viz/
└─ tests/
```

---

## ✨ Boas Práticas

*   **Commits Semânticos:** As mensagens de commit seguem o padrão [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
*   **Qualidade de Código:** `black`, `isort` e `ruff` são usados para garantir um código limpo e padronizado.
*   **Testes e CI:** Testes unitários e um pipeline de Integração Contínua garantem a estabilidade do projeto.

---

## 🛣️ Roadmap

- [ ] Adicionar análise Bayesiana para testes A/B.
- [ ] Implementar bootstrap para intervalos de confiança robustos.
- [ ] Publicar os notebooks como um site estático (MkDocs).
