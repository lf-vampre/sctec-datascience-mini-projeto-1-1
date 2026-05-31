"""
┌──────────────────────────────────────────────────────────────┐
│ Na documentação do Mini-Projeto foi solicitado               │
│ a entrega em 1 arquivo .py, por isso toda a lógica           │
│ de ETL e AED se encontra neste arquivo único.                │
├──────────────────────────────────────────────────────────────┤
│ Fluxo do Pipeline de dados:
│
│ 1- EXTRACT - Verificação e conhecimento da base
│ 2- TRANSFORM - Ajuste de colunas (Excluir e renomear) 
│ 3- TRANSFORM - Limpeza dos dados (DUPLICADOS)
│ 4- TRANSFORM - Correção dos dados e tratamento
│   -> Correção de tipos (str > datetime)
│   -> Inconsistência de dados
│   -> Identificação de Outliers


│   
│  
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
│   -> (reportar ao menos 2 problemas e fazer no mínimo 3 etapas de limpeza)
│   ->  Produzir um bloco de conclusões (3 a 6 tópicos)
│
└────────────────────────────────────────────────────┘
"""

# IMPORTS & CONFIGURAÇÂO
import kagglehub
import pandas as pd
from pathlib import Path
import os

kaggle_path = "namespaiva/base-varejo"
kaggle_csv = "Base Varejo.csv"
nome_df_limpo = "Base_Varejo_Limpo"


##### FUNÇÃO PARA AUDITORIA DO CÓDIGO ##### 
"""
┌──────────────────────────────────────────────────────────────┐
│ Para facilitar o acompanhamento da execução do pipeline,     │
│ essa função pausa a execução do programa, exibe uma mensagem │ 
│ e aguarda a interação do avaliador para continuar.           │
└──────────────────────────────────────────────────────────────┘
"""
def log_and_pause(message: str, clean: bool):
    # Exibe uma mensagem de log formatada e pausa a execução do programa
    # aguardando a interação do usuário.

    print(f"\n[LOG] {message}")
    print('-------------------------')
    input('Pressione [ENTER] para prosseguir para a próxima etapa...\n')

    if clean:
        # Limpa o terminal para o próximo bloco
        os.system('cls' if os.name == 'nt' else 'clear')


##### FUNÇÕES DE EXTRAÇÃO E VERIFICAÇÃO ##### 
"""
┌──────────────────────────────────────────────────────────────┐
│ 1- EXTRACT - Verificação e conhecimento da base              │
│   -> df.head(5) / df.tail(5)                                 │
│   -> df.info()                                               │
│   -> df.isnull().sum()                                       │
└──────────────────────────────────────────────────────────────┘
"""
def extrair_dados(path: str, csv: str) -> pd.DataFrame:
    path = kagglehub.dataset_download(path)
    csv_path = Path(path) / csv
    df = pd.read_csv(csv_path, sep=';')
    log_and_pause(f'Dados extraídos com sucesso da base: {csv_path}', False )
    return df

def verificar_dados(df: pd.DataFrame):
    print(df.head(5))
    log_and_pause('Exibindo as primeiras 5 linhas da Base Varejo. Função utilizada: df.head(5)', False )

    print(df.tail(5))
    log_and_pause('Exibindo as Últimas 5 linhas da Base Varejo. Função utilizada: df.tail(5)', False)

    print(df.info())
    log_and_pause('Exibindo número de registros, colunas, valores não nulos e tipo de dados. Função utilizada: df.info()', False)

    print(df.isnull().sum())
    log_and_pause('Exibindo quantidade de valores nulos por coluna. Função utilizada df.isnull().sum()', True)


##### FUNÇÕES DE TRANSFORMAÇÂO ##### 
"""
┌──────────────────────────────────────────────────────────────┐
│ 2- TRANSFORM - Ajuste de colunas (Excluir e renomear)        │
│   -> df.drop()                                               │
│   -> df.columns -> Renomear as Colunas                       │
├────────┬────────────┬────────────────────────────────────────┤
│ Coluna │    Nome    │              Renomeação                │
├────────┼────────────┼────────────────────────────────────────┤
│   1    │  DATA      │ Data                                   │
│   2    │  CO_ID     │ Nota_Fiscal                            │
│   3    │  CL_ID     │ Num_Cliente                            │
│   4    │  CL_GENERO │ Sexo                                   │
│   5    │  CL_EC     │ Estado_Civil                           │
│   6    │  CL_FHL    │ Num_Filhos                             │
│   7    │  CL_SEG    │ Classe_Economica                       │
│   8    │  PR_ID     │ Cod_Produto                            │
│   9    │  PR_CAT    │ Cat_Produto                            │
│  10    │  PR_NOME   │ Nome_Produto                           │
├────────┴────────────┴────────────────────────────────────────┤
│ Estado_Civil:                                                │
│       1: Casado ou união estával;                            │
│       2: Divorciado;                                         │
│       3: Separado;                                           │
│       4. Solteiro;                                           │
│       5: Viúvo.                                              │
└──────────────────────────────────────────────────────────────┘
"""
def remover_colunas(df: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    # drop retorna uma cópia por padrão (inplace=False)
    # Parâmetro "erros='ignore'" ignora nome de colunas que não existe
    df = df.drop(columns=colunas, errors='ignore')
    log_and_pause(f'Colunas removidas. Colunas restantes na base: {df.columns}', False )
    return df

def renomear_todas_colunas(df: pd.DataFrame, nome_colunas: list[str]) -> pd.DataFrame:
    # Verificação se a qtde de novos nomes é igual qtde de colunas
    if len(nome_colunas) != len(df.columns):
        # Se for diferente, retorna um erro e para a execução do programa
        raise ValueError(
            f'O número de novos nomes ({len(nome_colunas)}) deve ser igual '
            f'ao número de colunas do DataFrame ({len(df.columns)}).'
        )
    
    df.columns = nome_colunas
    log_and_pause(f'Colunas renomeadas. Colunas atuais na base: {df.columns}', True )
    return df


"""
┌──────────────────────────────────────────────────────────────┐
│ 3- TRANSFORM -  Limpeza dos dados                            │
│   [DUPLICADOS]                                               │
│ Mais de um produto na mesma nota? Faz sentido nessa base?    │
│                                   │                          │
│ Durante a análise preliminar dos duplicados, foram           │
│ identificados 96.553 registros repetidos (11,6% da base).    │
│ Considerando a ausência de uma coluna de quantidade e o      │
│ contexto de vendas no varejo, foi realizada uma investigação │
│ minusciosa para verificar se essas repetições correspondiam  │
│ a inconsistências nos dados ou à representação de múltiplas  │
│ unidades vendidas do mesmo produto em uma mesma nota fiscal. │
│ Os resultados indicaram que as repetições representam        │
│ quantidades comercializadas e por isso não foram excluídas   │
│ da base                                                      │
└──────────────────────────────────────────────────────────────┘
"""
def analise_duplicados(df: pd.DataFrame):
    #############################################################
    # Exibindo total linhas, únicas e duplicadas
    # Objetivo: mostrar quantos registros seriam perdidos ao aplicar drop_duplicates().
    #############################################################

    total_linhas = len(df)
    linhas_unicas = len(df.drop_duplicates())
    duplicadas = total_linhas - linhas_unicas
    
    print(f'Total de linhas: {total_linhas:,}')
    print(f'Linhas únicas: {linhas_unicas:,}')
    print(f'Linhas duplicadas: {duplicadas:,}')
    print(f'Percentual removido: {(duplicadas/total_linhas)*100:.2f}%')

    log_and_pause('Mostrando o impacto da remoção dos duplicados.', False)

    #############################################################
    # Objetivo: verificar quantas vezes um mesmo produto aparece dentro da mesma nota fiscal.
    #############################################################

    # Contar quantas vezes cada combinação Nota Fiscal + Produto ocorre
    freq_produtos = (
        df.groupby(['Nota_Fiscal', 'Cod_Produto'])
          .size()
          .reset_index(name='qtd')
    )

    # Exibir os caso mais frequentes para análise
    print(
        freq_produtos
            .sort_values('qtd', ascending=False)
            .head(10)
    )

    log_and_pause('Mostrando a frequência que cada produto aparece nas notas.', False)

    #############################################################
    # Estatísticas descritivas das quantidades encontradas
    # Objetivo: verificar se as repetições seguem um padrão compatível com quantidade vendida.
    #############################################################

    print(freq_produtos['qtd'].describe())

    log_and_pause(
        'Mostrando a estatística nas quantidades encontradas.'
        '\n Conclusão:'
        '\n 75% dos produtos aparecem apenas uma vez por nota'
        '\n poucas ocorrências com múltiplas unidades'
        '\n nenhuma frequência anormal foi observada'
        , False)
    
    #############################################################    
    # Análise detalhada de uma nota fiscal. 
    # Objetivo: verificar se diferentes produtos aparecem em qtde diferentes dentro da mesma compra.
    #############################################################

    # Nf exemplo:
    nota = 477026

    # Quantidade de ocorrências de cada produto nessa nota
    itens_nota = (
        df[df['Nota_Fiscal'] == nota]
          .groupby('Cod_Produto')
          .size()
          .sort_values(ascending=False)
    )
    print(itens_nota.head(10))

    log_and_pause(
        f'Mostrando quantidade de produtos na nota fiscal exemplo n.{nota}'
        '\n Conclusão:'
        '\n Produtos diferentes possuem quantidades diferentes'
        '\n O padrão é compatível com uma compra contendo múltiplas unidades'
        , False)
    
    #############################################################    
    # Analisar o impacto da remoção de duplicatas em cada nota
    # Objetivo: verificar como o drop_duplicates() altera a composição das notas.
    #############################################################    

    # Quantidade de itens por nota na base original
    itens_original = df.groupby('Nota_Fiscal').size()

    # Quantidade de itens por nota após remover duplicatas
    itens_sem_dup = (
        df.drop_duplicates()
        .groupby('Nota_Fiscal')
        .size()
    )

    # Criar DataFrame misto para comparacao
    comparacao = pd.DataFrame({
        'original': itens_original,
        'sem_duplicacao': itens_sem_dup
    })

    # Criar coluna "diferenca" para análise
    comparacao['diferenca'] = (
        comparacao['original']
        - comparacao['sem_duplicacao']
    )

    print( comparacao
            .sort_values('diferenca', ascending=False)
            .head(10)
    )

    log_and_pause(
        'Mostrando quantidade de itens removidos em cada nota com drop_duplicates()'
        '\n Conclusão:'
        '\n Algumas notas perderiam mais de 20 itens'
        '\n A remoção das linhas repetidas alteraria significativamente o conteúdo das vendas'
        , False)
    
    #############################################################    
    # Imprimir conclusão final
    #############################################################    
    log_and_pause(
        'Após análise minusciosa da Base em relação as linhas repetidas, concluiu-se:'
        '\n 1. A remoção de duplicatas eliminaria 11,6% da base'
        '\n 2. As repetições por produto possuem frequência máxima de apenas 6 ocorrências'
        '\n 3. A distribuição das frequências é compatível com quantidades vendidas'
        '\n 4. Produtos diferentes apresentam quantidades diferentes dentro da mesma nota fiscal'
        '\n 5. A remoção dos registros alteraria substancialmente a composição das notas'
        '\n Portanto, os registros repetidos foram interpretados como representação implícita' 
        '\n da quantidade vendida de cada produto, e não como erros de duplicação dos dados.'
        '\n Dessa forma, os registros foram mantidos na base analítica.'
        , True)


"""
""
┌──────────────────────────────────────────────────────────────┐
│ 4- TRANSFORM - Correção dos dados e tratamento               │
│   -> Correção de tipos (str > datetime)                      │
│   -> Inconsistência de dados                                 │
│   -> Identificação de Outliers                               │
└──────────────────────────────────────────────────────────────┘


│   -> Categorias (para textos repetidos): df['coluna'].astype('category')

 
"""
def correcao_dados(df: pd.DataFrame):
    # Converter strings para data, colocando NaT onde falhar
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    print('Coluna Data transformada no tipo datetime com sucesso!')

    # Inconsistência de dados -> Data: Somente data?
    datas_invalidas = df['Data'].isna()
    print(f"Linhas com Datas inválidas: {len(datas_invalidas)}")

    # Inconsistência de dados -> Sexo: Somente M e F?
    print('Valores encontrados na coluna Sexo:')
    print(df['Sexo'].value_counts(dropna=False))

    # Inconsistência de dados -> ESTADO CIVIL: Somente de 1 a 5?
    print('Valores encontrados na coluna Estado_Civil:')
    print(df['Estado_Civil'].value_counts().sort_index())
    
    # Inconsistência de dados -> CLASSE ECONOMICA: Somente A, B ou C?
    print('Valores encontrados na coluna Classe_Economica:')
    print(df['Classe_Economica'].value_counts(dropna=False))

    # Inconsistência de dados -> CATEGORIAS: Quais? Repetidas?
    print('Valores encontrados na coluna Categorias:')
    print(df['Cat_Produto'].value_counts())

    # Inconsistência de dados -> PRODUTOS: Repetidos? Quais em cada categoria?
    print('Valores únicos encontrados na coluna Produtos:')
    print(df['Nome_Produto'].nunique())

    # Inconsistência de dados -> SKU: Únicos, repetidos para produtos diferentes?

    produtos_multiplas_categorias = (
    df.groupby('Nome_Produto')['Cat_Produto']
      .nunique()
      .reset_index()
    )

    produtos_multiplas_categorias = (
        produtos_multiplas_categorias[
            produtos_multiplas_categorias['Cat_Produto'] > 1
        ]
    )

    print(f'produtos em multipla categoria: {produtos_multiplas_categorias}')



    sku_multiplos_produtos = (
    df.groupby('Cod_Produto')['Nome_Produto']
      .nunique()
      .reset_index()
    )

    sku_multiplos_produtos = (
        sku_multiplos_produtos[
            sku_multiplos_produtos['Nome_Produto'] > 1
        ]
    )

    print(f'SKU mais de u m produto: {sku_multiplos_produtos}')


    produto_multiplos_skus = (
    df.groupby('Nome_Produto')['Cod_Produto']
      .nunique()
      .reset_index()
    )

    produto_multiplos_skus = (
        produto_multiplos_skus[
            produto_multiplos_skus['Cod_Produto'] > 1
        ]
    )

    print('Produto mais de um sku: ')
    print(produto_multiplos_skus)


    produto_dim = (
    df[
        ['Cod_Produto',
         'Nome_Produto',
         'Cat_Produto']
    ]
    .drop_duplicates()
    )

    print(produto_dim.shape)


    print(
    produto_dim.groupby('Cod_Produto')
    .size()
    .value_counts()
    )


"""
┌──────────────────────────────────────────────────────────────┐
│ 5- TRANSFORM -  Limpeza dos dados [TRATAMENTO DE NULOS]      │
│   -> df.isnull().sum()                                       │
│   -> df.isnull().mean()                                      │
│   -> df.fillna(0) ou df.fillna('Desconhecido')               │
│   -> df['coluna'].fillna(df['coluna'].mean())                │
│       (Média / Mediana / Moda)                               │
└──────────────────────────────────────────────────────────────┘
"""
def verificacao_nulos(df: pd.DataFrame):
    print(df.isnull().sum())
    print(df.isna().sum())



#FUNÇÕES DE CARGA
#FUNÇÕES AED
#FUNÇÕES VISUALIZAÇÃO (GRAPH / PLOT)

#COMENTÁRIOS COM RETORNO DAS FUNÇÕES (NOS DOCS TAMBÉM)
#INSERIR NO DOC VERSIONAMENTO DO GIT 

##### FUNÇÕES PRINCIPAL ##### 
"""
┌──────────────────────────────────────────────────────────────┐
│ Função principal main()                                      │
│   -> Orquestra todo o pipeline de ETL + AED                  │
└──────────────────────────────────────────────────────────────┘
"""
def main():
    # EXTRACT: Extrair dados e armazenar no DataFrame df
    log_and_pause('Iniciando extração da base de Dados Varejo do Kaggle.', False)
    df = extrair_dados(kaggle_path, kaggle_csv)
    
    # EXTRACT: Análise e verificação preliminar
    #log_and_pause('Iniciando análise e verificação preliminar.', False)
    #verificar_dados(df)

    # TRANSFORM: Remover colunas excedentes
    log_and_pause('Remover colunas excedentes da base.', False)
    df_limpo = remover_colunas(df, ['Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13'])

    # TRANSFORM: Renomear todas as colunas
    log_and_pause('Renomear todas as colunas da base.', False)
    df_limpo = renomear_todas_colunas(
        df_limpo, 
        ['Data', 'Nota_Fiscal', 'Num_Cliente', 'Sexo', 'Estado_Civil', 'Num_Filhos', 'Classe_Economica', 'Cod_Produto', 'Cat_Produto', 'Nome_Produto']
    )

    # TRANSFORM: Duplicados
    #log_and_pause('Análisar o impacto da remoção de linhas duplicadas.', False)
    #analise_duplicados(df_limpo)

    correcao_dados(df_limpo)


    # TRANSFORM: Tratamento de nulos
    #verificacao_nulos(df_limpo)
    
 
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


