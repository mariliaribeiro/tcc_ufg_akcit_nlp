# tcc_ufg_akcit_nlp

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Este repositório contém o código desenvolvido durante o Trabalho de Conclusão de Curso da Pós Graduação em Processamento de Linguagem Natural da UFG em parceria com a AKCIT.

## Organização do projeto

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         src and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── src   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes src a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------


## Configuração do ambiente de desenvolvimento

**Requisitos:** Python 3.12 ou superior.

O primeiro passo é criar e ativar o virtualenv para instalar as depedências.

```
# Criando o virtualenv
python -m venv .venv

# Ativando o virtualenv
source .venv/bin/activate
```

Instale o poetry dentro do seu virtualenv.

```
pip install poetry
```

A gestão de dependências entre os pacotes foi configurada com o [poetry](https://python-poetry.org/docs/). Então para instalar ou atualizar os pacotes no seu ambiente virtual, basta rodar o comando abaixo.

```
poetry update
```


Obs: Para adicionar novos pacotes basta utilizar o comando abaixo:

```
poetry add nome_pacote
```