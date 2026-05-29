"""
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Na documentação do Mini-Projeto foi solicitado                                                  │
│ a entrega em 1 arquivo .py, por isso toda a lógica 
│ de ETL e AED se encontra neste arquivo único.      
│
│ Fluxo do Pipeline de dados:
│ 1- EXTRACT - Verificação e conhecimento da base
│   -> df.head(5) / df.tail(5)
│   -> df.info() (número de registros, colunas e tipos de dados)
│   -> df.isnull().sum()
│
│ 2- TRANSFORM - Ajuste de colunas (Excluir e renomear)
│   -> df.drop()
│   -> df.columns
│   1. DATA: Data da compra;
│   2. CO_ID: Identificação do número de compra (número da nota fiscal);
│   3. CL_ID: Identificação do cliente (número do cliente);
│   4. CL_GENERO: Sexo biológico informado pelo cliente;
│   5. CL_EC: Estado civil do cliente:
│       1: Casado ou união estával;
│       2: Divorciado;
│       3: Separado;
│       4. Solteiro;
│       5: Viúvo.
│   6. CL_FHL: Número de filhos do cliente;
│   7. CL_SEG: Segmentação econômica do cliente (classe A, B ou C);
│   8. PR_ID: Código do produto (SKU) adquirido;
│   9. PR_CAT: Categoria do produto adquirido;
│   10. PR_NOME: Nome do produto adquirido.
│
│ 3- TRANSFORM -  Limpeza dos dados (reportar ao menos 2 problemas e fazer no mínimo 3 etapas de limpeza)
│   (DUPLICADOS)
│   -> df.duplicated().sum()
│   -> verificar os duplicados (mais de um produto na mesma nota? Faz sentido?)
│   -> df.drop.duplicates(inplace=True)
│   (TRATAMENTO DE NULOS)
│   -> df.isnull().sum()
│   -> df.isnull().mean()
│   -> df.fillna(0) ou df.fillna('Desconhecido')
│   -> df['coluna'].fillna(df['coluna'].mean()) / Média / Mediana / Moda
│   (CORREÇÃO DO TIPO DE DADOS)
│   -> df.dtypes
│   -> Numérico: pd.to_numeric(df['coluna'], error='coerce') (transforma erros em NaN) depois verificar se tem NaN
│   -> Data: pd.to_datetime(df['coluna']) -> ver os parâmetros de formatação
│   -> String, Integer, Float ?
│   -> Categorias (para textos repetidos): df['coluna'].astype('category')
│   (INCONSITÊNCIA DE DADOS)
│   -> GENERO: Somente M e F?
│   -> ESTADO CIVIL: Somente de 1 a 5?
│   -> CLASSE ECONOMICA: Somente A, B ou C?
│   -> CATEGORIAS: Quais? Repetidas?
│   -> PRODUTOS: Repetidos? Quais em cada categoria?
│   -> SKU: Únicos, repetidos para produtos diferentes?
│   (Identificação de Outliers)
│   -> Visualizar: df.describe() (olhe o min e max).
│   -> Filtrar: # Exemplo: Manter apenas valores dentro de 3 desvios padrão df = df[(df['coluna'] - df['coluna'].mean()).abs() <= (3 * df['coluna'].std())]   
│
│ 4. LOAD - Gerar nova base limpa
│   -> Salvar em um arquivo CSV
│   -> Salvar em um arquivo XLS
│   -> Garantir que a AED seja feita na base limpa
│
│ 5- AED - Gerar estatísticas e análises
│   -> Estatísticas para coluna número de filhos: (média; mediana; desvio padrão; moda; máximo; mínimo; e contagem).
│   -> Regra de Negócio: Validou a regra do identificador de número de compra (Nota pertence a um único cliente / nota pertence a um único dia)
│   -> groubpy() / pivot_table(): Explorar padrões de agrupamento com pelo menos 2 agrupamentos (Ex. Genero com mais vendas)
│      + value_counts / .dt / diff ou shift / sort_values / corr / cut 
│       a) Frequência: Quantas notas um mesmo cliente emitiu?
│       b) Perfil de consumo: Cruzar classe economica, genero e estado civil com quantidade de itens (Qual classe compra mais vezes? Qual classe tem maior volume "carrinho cheio"?)
│       c) Vendas por período: Extrair dia, dia da semana e mês da data. (Qual dia da semana e qual mês vendeu mais? Agrupar período de dias do mês pra ver picos de vendas)
│       d) Ciclo de Recompra por classe social: Média de quantos dias da última nota, para anterior em cada categoria de classe social?
│       e) Produtos: Quais categorias venderam mais e quais produtos? E por classe social?
│       f) Composição familiar e influência: Ranking de categorias pelo tamanho da família
│
│   -> Produzir um bloco de conclusões (3 a 6 tópicos)
│
└────────────────────────────────────────────────────┘
"""

# IMPORTS e CONFIGURAÇÂO
import kagglehub
import pandas as pd
from pathlib import Path
import os

kaggle_path = "namespaiva/base-varejo"
kaggle_csv = "Base Varejo.csv"
nome_df_limpo = "Base_Varejo_Limpo"


#FUNÇÃO DE EXTRAÇÃO
#FUNÇÕES DE TRANSFORMAÇÂO
#FUNÇÕES DE CARGA
#FUNÇÕES AED
#FUNÇÕES VISUALIZAÇÃO (GRAPH / PLOT)

#COMENTÁRIOS COM RETORNO DAS FUNÇÕES (NOS DOCS TAMBÉM)
#INSERIR NO DOC VERSIONAMENTO DO GIT 


def log_and_pause(message: str):
    """
    Exibe uma mensagem de log formatada e pausa a execução do programa
    aguardando a interação do usuário.
    """

    print(f"\n[LOG] {message}")
    print("-------------------------")
    input("Pressione [ENTER] para prosseguir para a próxima etapa...")
    # Limpa o terminal para o próximo bloco
    os.system('cls' if os.name == 'nt' else 'clear')


def extrair_dados():
    path = kagglehub.dataset_download(kaggle_path)
    csv_path = Path(path) / kaggle_csv
    df = pd.read_csv(csv_path, sep=';')
    return df


def main():
    # 1.
    df = extrair_dados()
    #print(df.head(5))
   #print(df.tail(5))
   


"""
┌───────────────────────────────────────────────────────────────────────────────┐
│ Executa a função main() apenas se o script for executado diretamente.         │
│ Quando o arquivo é rodado diretamente, a variável especial __name__           │
│ recebe automaticamente o valor "__main__", fazendo a condição ser verdadeira  │
│ e executando o código dentro do bloco.                                        │
└───────────────────────────────────────────────────────────────────────────────┘
"""
if __name__ == "__main__":
    main()