<br>

# 💻 Curso Datascience - Visualização de Dados e Business Intelligence. 
Mini Projeto Avaliativo - Módulo 1 - Semana 07

![Logos](./images/logos.png)

<br>
<br>

# 🏪 AED (Análise Exploratória de Dados): "Base 'Varejo'" 
Utilizando a base 'Varejo' que contém registros reais de compras
(https://www.kaggle.com/datasets/namespaiva/base-varejo/data)

<br>

## 🎯 Propósito

> O desafio propõe entregar um script em Python que realize uma Análise Exploratória da base Varejo seguindo etapas claras, documentadas e reproduzíveis. Etapas obrigatórias: 
  
<br>

1. Usar pandas; outras bibliotecas são opcionais (NumPy, Matplotlib, Seaborn).
2. Carregar a base Varejo.csv com pandas e mostrar: número de registros, colunas e tipos de dados.
3. Verificar e reportar ao menos dois problemas básicos: valores nulos por coluna, duplicatas e possíveis inconsistências (ex.: datas inválidas ou categorias vazias).
4. Fazer as três etapas de limpeza mínima necessária: remover ou imputar nulos (explique a escolha), eliminar duplicatas relevantes e ajustar tipos de dados (ex.: converter coluna DATA para datetime).
5. Gerar estatísticas descritivas básicas para coluna de número de filhos do cliente (média; mediana; desvio padrão; moda; máximo; mínimo; e contagem).
6. Explorar padrões de agrupamento com pelo menos dois agrupamentos (por exemplo: gênero com mais vendas, compras), usando groupby() ou pivot_table().
7. Produzir um pequeno bloco de conclusões (3–6 tópicos) com os principais insights obtidos e possíveis problemas remanescentes na base.

<br>

## ✅ Requisitos das tarefas

> Sprints das tarefas necessários para conclusão do mini projeto.

<br>

- **Sprint 1 (Importação dos dados):** Realização da importação dos dados na plataforma Kaggle para a IDE VsCode ou Colab, onde o script  será executado.
- **Sprint 2 (Transformação de Strings, Integer e Float e Datetime):** Desenvolvimento das funções de limpeza de texto, inteiros e decimais usando métodos e expressões regulares.
- **Sprint 3 (Limpeza de Nulos e Duplicatas):** Aplicação das condicionais e funções  para identificação e substituição de valores vazios e de str para valores de data tipo datetime, na tabela de varejo. 
- **Sprint 4 (Estatística Descritiva):** Aplicação das funções estatísticas para coletar parâmetros da coluna de Número de filhos do cliente.
- **Sprint 5 (Relatório e Documentação):** Construção dos contadores do relatório final exibido no terminal, finalização do README.md com a reflexão teórica e submissão do link no AVA.
- **Sprint 6 (Versionamento):** Envio dos arquivos (script + README.md + df_limpo), via Git para o repositório da turma no GitHub.


## 📖 Documentação e Insights

 Para uma análise profunda sobre a arquitetura do código e o storytelling detalhado dos dados, consulte a seção no final deste arquivo:

> **[📊 Visualizações e Resultados](#-visualizações-e-resultados)** 

<br>

## 🚀 Como Começar (Instalação)

> ### Pré-requisitos

* **Python:** Versão 3.12.3 ou superior.
* **Ambiente virtual .venv:** Criação do ambinte virtual e instalação das dependências.

<br>

> ### Instalação e Configuração

<br>

1. **Clone o repositório e acesse a pasta:**
```bash

git clone https://github.com/lf-vampre/sctec-datascience-mini-projeto-1-1
cd sctec-datascience-mini-projeto-1-1

```

<br>

2. **Crie e ative o ambiente virtual (venv):**
```bash

python3 -m venv .venv # ou então: python -m venv .venv

```

* Ativação (Linux/WSL/MacOS):
```bash

source .venv/bin/activate

```

* Ativação (Windows - PowerShell):
```bash

.\.venv\Scripts\Activate.ps1

```

<br>

3. **Instale as dependências:**
```bash

pip install -r requirements.txt

```

<br>

## 💻 Uso Básico

> Para iniciar o pipeline completo (ETL + AED), execute o comando abaixo no terminal:

```bash

python3 main.py # ou então: python main.py

```

O sistema imprimirá logs em tempo real e aguardará sua interação em cada etapa crítica.

<br>

## 📊 Visualizações e Resultados

> Abaixo estão a descrição da arquitetura utilizada no pipeline, os insights e storytelling gerados com as analises dos dados:

<br>



<br>

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python (Pandas, Seaborn, Matplotlib).
* **Base de Dados:** csv.
* **Ambiente:** VS Code / WSL.
* **Orquestração:** Lógica modular em Python.

---

<br>

