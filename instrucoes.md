# statistics-for-data — Plano completo (Estatística Aplicada)

> Repositório do portfólio focado em **estatística aplicada** com dados **100% abertos** e código reprodutível. Projetado para demonstrar domínio prático em distribuições, testes de hipóteses, regressão e storytelling analítico.

---

## 1) Objetivos do repositório

- Consolidar **fundamentos estatísticos** em projetos práticos com dados públicos.
- Demonstrar **boas práticas** de versionamento, qualidade de código, testes, CI, documentação e licenças.
- Entregar **notebooks didáticos** e **scripts reutilizáveis** que resolvem problemas reais (educação, finanças, CX, operações).

**Resultados esperados**

- Portfólio navegável (README + docs) com estudos organizados por tema.
- Reprodutibilidade total (environment, seed, dados versionados/baixados via script).
- Gráficos e interpretações alinhados a negócio, com **efeito** e **poder estatístico**.

---

## 2) Estrutura de pastas (sugestão)

```
statistics-for-data/
├─ README.md
├─ LICENSE
├─ pyproject.toml              # ou requirements.txt / environment.yml
├─ tasks.py                    # script de automação de tarefas
├─ .gitignore
├─ .pre-commit-config.yaml     # black, ruff, isort, nbstripout, end-of-file-fixer
├─ .github/
│  └─ workflows/
│     └─ ci.yml               # testes + validação notebooks
├─ data/
│  ├─ raw/                    # dados brutos
│  ├─ external/               # extraídos de APIs / fontes externas
│  └─ processed/              # dados tratados/feature store simples
├─ docs/                      # artefatos de documentação (mkdocs/quarto)
├─ notebooks/
│  ├─ 01_probability/
│  │  ├─ normal_distribution.ipynb
│  │  ├─ poisson_counts.ipynb
│  │  └─ binomial_abtest.ipynb
│  ├─ 02_hypothesis_tests/
│  │  ├─ ttest_ab_campaign.ipynb
│  │  ├─ anova_iris_species.ipynb
│  │  └─ chi_square_titanic.ipynb
│  └─ 03_regression/
│     ├─ linear_california_housing.ipynb
│     └─ logistic_telco_churn.ipynb
├─ src/
│  ├─ data/
│  │  ├─ loaders.py           # funções p/ baixar/carregar dados públicos
│  │  └─ preprocess.py        # limpeza, padronização, DQ checks
│  ├─ stats/
│  │  ├─ probability.py       # implementações "from scratch" (pdf, cdf, pmf)
│  │  └─ hypothesis.py        # t-test, chi2, ANOVA (validação vs SciPy)
│  ├─ features/engineering.py # feature engineering comum
│  ├─ models/
│  │  ├─ train.py             # treinos simples (regressão/logística)
│  │  └─ evaluate.py          # métricas + curvas (ROC, PR, residuais)
│  └─ viz/plots.py            # funções de visualização padronizadas
└─ tests/
   ├─ test_probability.py
   ├─ test_hypothesis.py
   └─ test_loaders.py
```

---

## 3) Fontes de dados abertas (curadoria)

| Tema                     | Fonte aberta                                 | Dataset (exemplos)                                     | Uso no repositório                                                 |
| ------------------------ | -------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------ |
| Probabilidade (Normal)   | **scikit-learn datasets**                    | *California Housing* (valores de casas)                | Aproximar log(preço) à Normal; z-scores; QQ-plot                   |
| Probabilidade (Poisson)  | **NYC Open Data**                            | *311 Service Requests* (contagem por dia/hora)         | Modelar contagens; verificar overdispersion; comparar com Poisson  |
| Probabilidade (Binomial) | **Open A/B datasets** ou **simulado**        | CTR de campanhas (cliques vs impressões)               | Estimar p e intervalos; simular resultados; teste binomial         |
| Testes – t-test          | **E-commerce A/B** (open samples)            | Conversão A vs B (taxas, ticket)                       | t-test independentes/pareado; Cohen’s d; verificação de suposições |
| Testes – ANOVA           | **Iris (UCI/OpenML)**                        | Comprimento de sépalas por espécie                     | ANOVA 1 fator; pós-hoc (Tukey HSD); eta²/omega²                    |
| Testes – Qui-quadrado    | **Titanic** (espalhado em repositórios open) | Tabela de contingência (sexo x sobrevivência)          | χ² de independência; resíduos padronizados                         |
| Regressão Linear         | **California Housing** (sklearn)             | Preço vs variáveis (rooms, income, latitude/longitude) | OLS; multicolinearidade (VIF); validações de resíduo               |
| Regressão Logística      | **Telco Customer Churn** (IBM Sample Data)   | Churn (0/1) com variáveis categóricas/numéricas        | Logit; odds ratio; AUC/ROC; matriz de confusão                     |

> Observação: Kaggle também é bem-vindo via **Kaggle API** (opcional). Para reprodutibilidade sem conta, priorize conjuntos nativos (sklearn/UCIs) e APIs públicas (ex.: NYC Open Data).

---

## 4) Escopo por notebook (o que exatamente entregar)

### 4.1. Probabilidade

**(a) **``

- **Dados**: California Housing (sklearn) → variável alvo `MedHouseVal` (e/ou log-transform).
- **Passos**: EDA, histograma, KDE, **QQ-plot**, IC para média, padronização (z-score), lei dos grandes números, TLC com simulação (amostragens repetidas).
- **Saídas**: Tabela de estatísticas, verificação de normalidade (Shapiro-Wilk), interpretação de outliers, storytelling.

**(b) **``

- **Dados**: NYC 311 (agregação diária/horária por tipo de chamado).
- **Passos**: Ajustar Poisson, checar **overdispersion** (comparar média vs variância), alternativa **Quasi-Poisson**/NegBin; análise de sazonalidade simples.
- **Saídas**: Taxas médias por período, diagnóstico gráfico das contagens vs ajuste Poisson.

**(c) **``

- **Dados**: CTR (cliques, impressões) – público ou simulado fiel.
- **Passos**: Estimar `p̂`, IC (Wilson), teste binomial, teste de proporções (two-proportion z-test), cálculo de **tamanho de amostra** e **poder**.
- **Saídas**: Recomendação sobre o vencedor A/B com efeito absoluto/relativo.

### 4.2. Testes de Hipóteses

**(a) **``

- **Dados**: Métrica contínua (ex.: ticket médio A vs B).
- **Passos**: Teste de normalidade/variâncias (Levene), **t-test** (independente/pareado), **Cohen’s d**, **Bayes factor** (opcional), interpretação de negócio.
- **Saídas**: Conclusão textual com **efeito** + **IC** + **p-valor** + **poder**.

**(b) **``

- **Dados**: Iris (sepal length por espécie).
- **Passos**: ANOVA 1 fator; supostos; **Tukey HSD**; **eta²/omega²**; violino/boxplots; pontos de atenção (heterocedasticidade).
- **Saídas**: Quadro ANOVA, pares significativos e interpretação biológica.

**(c) **``

- **Dados**: Tabela sexo × sobrevivência (ou classe × sobrevivência).
- **Passos**: Tabela de contingência; χ² de independência; **resíduos padronizados** (quais células explicam associação).
- **Saídas**: Heatmap de resíduos; síntese do risco relativo (quando aplicável).

### 4.3. Regressão

**(a) **``

- **Passos**: OLS (statsmodels), supostos (linearidade, normalidade dos resíduos, homocedasticidade), **VIF**, seleção de variáveis (AIC/BIC), regularização (Lasso/Ridge) opcional.
- **Saídas**: Tabela resumida (coeficientes, IC, p, R², R²-aj), diagnóstico de resíduos e mapa de erros por região (se aplicável).

**(b) **``

- **Passos**: One-hot, padronização, **logit** (statsmodels), **odds ratio** interpretável, curva **ROC** e **PR**, matriz de confusão calibrada por custo (threshold tuning), **calibração** (Brier score, calibration curve).
- **Saídas**: Drivers de churn, recomendações acionáveis (retenção, oferta, canais).

---

## 5) Padrões de código e ambiente

- **Python** 3.11+; `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn`, `pingouin` (efeitos/poder), `requests` (APIs), `pyjanitor` (limpeza, opcional).
- **Estilo**: `black`, `isort`, `ruff`; tipagem com `mypy` (quando aplicável).
- **Notebooks**: `nbstripout` para limpar outputs; `jupytext` (opcional) para versionar como `.py`.
- **Seeds**: `numpy.random.seed(42)` para reprodutibilidade em simulações.

**Exemplo **``** (trecho)**

```toml
[project]
name = "statistics-for-data"
requires-python = ">=3.11"
dependencies = [
  "pandas==2.2.2",
  "numpy==1.26.4",
  "scipy==1.13.1",
  "statsmodels==0.14.2",
  "scikit-learn==1.5.1",
  "matplotlib==3.8.4",
  "seaborn==0.13.2",
  "pingouin==0.5.4",
  "requests==2.32.3"
]
```

---

## 6) Scripts essenciais (src/)

`` (esqueleto)

```python
from pathlib import Path
import pandas as pd
import requests

DATA_DIR = Path("data")
RAW = DATA_DIR / "raw"
EXTERNAL = DATA_DIR / "external"
PROCESSED = DATA_DIR / "processed"

RAW.mkdir(parents=True, exist_ok=True)
EXTERNAL.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

def load_california_housing() -> pd.DataFrame:
    from sklearn.datasets import fetch_california_housing
    ds = fetch_california_housing(as_frame=True)
    df = ds.frame
    df.to_csv(RAW / "california_housing.csv", index=False)
    return df

def load_nyc_311(limit: int = 100_000) -> pd.DataFrame:
    # Endpoint público do NYC 311 (exemplo genérico com $limit)
    base = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
    params = {"$limit": limit}
    r = requests.get(base, params=params, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(pd.compat.StringIO(r.text))
    df.to_csv(EXTERNAL / "nyc_311.csv", index=False)
    return df

```

`` (trecho – validar com SciPy)

```python
import numpy as np
from scipy import stats

def two_sample_ttest(a: np.ndarray, b: np.ndarray, equal_var: bool = False):
    return stats.ttest_ind(a, b, equal_var=equal_var)

def chi_square_independence(table: np.ndarray):
    chi2, p, dof, expected = stats.chi2_contingency(table)
    residuals = (table - expected) / np.sqrt(expected)
    return chi2, p, dof, expected, residuals
```

`` (trecho)

```python
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, brier_score_loss

def classification_report_proba(y_true, y_proba, threshold=0.5):
    y_pred = (y_proba >= threshold).astype(int)
    auc = roc_auc_score(y_true, y_proba)
    return {"auc": auc, "threshold": threshold, "brier": brier_score_loss(y_true, y_proba)}
```

---

## 7) Qualidade, testes e CI

- **Unit tests** (`tests/`):
  - `test_probability.py`: pdf/cdf/pmf implementadas vs `scipy.stats` (tolerâncias).
  - `test_hypothesis.py`: `ttest_ind`/`chi2_contingency`/ANOVA (validação cruzada).
  - `test_loaders.py`: checar colunas/chaves mínimas e não-vazio.
- **CI (GitHub Actions)**: rodar lint, testes e execução rápida de notebooks com `nbmake` (subset amostral de dados, p.ex. `LIMIT=5000`).
- **Pre-commit**: formatação, trailing whitespace, nbstripout.

---

## 8) Visualização (padrão)

- Histograma + KDE, **QQ-plot** (Normal), **heatmap de resíduos** (χ²), **box/violin** (ANOVA), **residual vs fitted** (OLS), **ROC/PR** (logística).
- Funções centralizadas em `src/viz/plots.py` para padronizar títulos, legendas e notas.

---

## 9) Storytelling e entregáveis por notebook

Cada notebook deve ter esta hierarquia padrão no topo:

1. **Objetivo do estudo** (pergunta de negócio)
2. **Fonte & Licença** (link e licença resumida)
3. **Dicionário de dados** (variáveis-chave)
4. **Metodologia** (passos, suposições, testes, métricas)
5. **Resultados** (tabelas e gráficos essenciais)
6. **Interpretação** (efeitos, riscos, recomendação)
7. **Limitações** (viés, suposição violada, dados faltantes)
8. **Reprodutibilidade** (seed, versão libs, como rodar)

> **Obrigatório**: sempre reportar **efeito** (Cohen’s d, eta²/omega²), **intervalos de confiança** e, quando fizer sentido, **poder** (power analysis).

---

## 10) README.md (modelo do repositório)

- **Título e objetivo**
- **Mapa dos estudos** (links para cada notebook)
- **Como rodar** (`python tasks.py setup`, `python tasks.py data`, `python tasks.py test`)
- **Estrutura de pastas**
- **Dados e licenças** (tabela resumida)
- **Boas práticas** (commit message, convenções)
- **Roadmap** (próximas melhorias)

---

## 11) tasks.py (Automação de Tarefas)

O script `tasks.py` automatiza tarefas comuns do projeto. Ele é uma alternativa em Python puro ao `Makefile`.

**Uso:** `python tasks.py [tarefa]`

**Tarefas disponíveis:**
- `setup`: Instala as dependências.
- `data`: Baixa os datasets de exemplo.
- `test`: Roda a suíte de testes.
- `lint`: Analisa o código com ruff.
- `format`: Formata o código com black e isort.
- `help`: Mostra todas as tarefas.

---

## 12) Licenças e conformidade

- Código: **MIT** (simples e permissiva).
- Dados: respeitar licença de cada fonte (mencionar em cada notebook/README). Evitar persistir *dados pessoais*.

---

## 13) Estudos de caso adicionais (opcionais)

- **Educação** (alinhado ao seu histórico): predição de evasão a partir de dados acadêmicos públicos/sintéticos → reforçar métricas (-10% evasão como referência conceitual).
- **Finanças**: relação entre renda (World Bank) e indicadores de bem-estar; ou séries do Banco Central (regressão/elasticidade).
- **CX/Operações**: análise de tempo de atendimento (público 311) → impacto em satisfação (proxy) e priorização.

---

## 14) Checklist de conclusão (por tópico)

-

---

## 15) Roadmap

1. Adicionar **Bayesian A/B** (PyMC) como contraste aos testes frequencistas.
2. Implementar **bootstrap** para ICs robustos em métricas de negócio.
3. Publicar os notebooks como site (MkDocs Material/GitHub Pages).
4. Criar **templates** de notebook para replicar estudos com novas fontes.

---

### Pronto para gerar os arquivos-base?

Posso montar **README**, **pyproject/requirements**, **Makefile**, **workflows de CI** e os **esqueletos de notebooks** já com células-guia e placeholders de gráficos/interpretação.

