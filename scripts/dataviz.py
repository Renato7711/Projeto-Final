import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 
import sqlite3
#from io import StringIO
#import requests

#Lendo o banco de dados
try:
    conn = sqlite3.connect('banco.db')
    query = "SELECT * FROM dados"
    df = pd.read_sql_query(query, conn)
except:
    db_path = '/mount/src/projeto-final/scripts/banco.db'
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM dados"
    df = pd.read_sql_query(query, conn)

#Filtros para a responsividade
st.sidebar.header('**Fitros**')
estado = df['uf'].drop_duplicates()
estado_escolhido = st.sidebar.selectbox('Selecione o Estado', estado)

ano = df['ano'].drop_duplicates()
ano_escolhido = st.sidebar.selectbox('Selecione o ano', ano)

df2 = df.loc[df['uf']==estado_escolhido]
df3 = df.loc[(df['uf'] == estado_escolhido) & (df['ano'] == ano_escolhido)]
df4 = df.loc[df['ano'] == ano_escolhido]

#Cabeçalho
st.title('*Dados Brasileiros de Arrecadação de Impostos*')
st.write('Dados da arrecadação de impostos e contribuições federais administrados pela Secretaria Especial da Receita Federal do Brasil (RFB).')


#Infos Gerais
expander1 = st.expander('Informações Gerais Sobre os Impostos Arrecadados (2000 - 2024)')

with expander1:
    total_arrecadado = df.valor.sum()
    total_ano = df['ano'].nunique()
    col1, col2 = st.columns(2)
    col1.metric("Média Anual", 
                value = (total_arrecadado/total_ano))
    col2.metric("Total", 
                value = df.valor.sum())
    
    #Complemento da responsividade (CORREÇÃO SUGERIDA PELO PROFESSOR):
    media = df3['valor'].mean()
    mediana = df3['valor'].median()
    dp = np.std(df3['valor'])
    st.write(f'Analisando os dados do estado {estado_escolhido} no ano {ano_escolhido}, notamos que a média de arrecadação de impostos ficou em {media} (mediana: {mediana}), com um desvio de {dp}.')


univariadas = st.expander('Análise Univariada Por Estado (2000 - 2024)')

with univariadas:

    total_arrecadado = df2.valor.sum()
    total_ano = df['ano'].nunique()
    col1, col2 = st.columns(2)
    col1.metric("Média Anual", 
                value = (total_arrecadado/total_ano))
    col2.metric("Total", 
                value = df2.valor.sum())
    
    #Distribuição dos valores de imposto
    st.write('**Distribuição dos Valores de Imposto Por Estado (Em Bilhões)**')
    fig = px.box(df2, x='valor')
    st.plotly_chart(fig)

    # Evolução dos valores dos impostos
    meses_ordenados = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho',
                        'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    df2['mês'] = pd.Categorical(df2['mês'], categories=meses_ordenados, ordered=True)
    # Agrupar os dados por mês e calcular a soma dos valores
    df_grouped = df2.groupby('mês')['valor'].sum().reset_index()
    # Ordenar os dados agrupados
    df_grouped = df_grouped.sort_values('mês')
    # Criar um gráfico de linha para visualizar a evolução dos valores de imposto ao longo dos meses
    plt.figure(figsize=(10, 6))
    plt.plot(df_grouped['mês'], df_grouped['valor'], marker='o')
    plt.xlabel('Mês')
    plt.ylabel('Valor do Imposto')
    plt.title('Evolução dos Valores de Imposto ao Longo dos Meses por Estado (Em Bilhões)')
    plt.grid(True)
    st.pyplot(plt)

    # Agrupar os dados por estado e calcular a soma dos valores
    df_grouped = df.groupby('uf')['valor'].sum().reset_index()
    # Criar um gráfico de barras para comparar os valores de imposto por estado
    plt.figure(figsize=(10, 6))
    plt.bar(df_grouped['uf'], df_grouped['valor'])
    plt.xlabel('Estado')
    plt.ylabel('Valor do Imposto')
    plt.title('Comparação dos Valores de Imposto por Estado')
    plt.grid(True)

    st.pyplot(plt)


multivariadas = st.expander('Análise Multivariada')

with multivariadas:
    st.write('Valores Fitrados por Estado e Ano:')
    total_arrecadado_ano = df3.valor.sum()
    total_mes = df['mês'].nunique()
    col1, col2 = st.columns(2)
    col1.metric("Média Mensal", 
                value = (total_arrecadado_ano/total_mes))
    col2.metric("Total", 
                value = df3.valor.sum())
    

    # Criar um gráfico de calor
    df_pivot = df2.pivot_table(values='valor', index='ano', columns='mês', aggfunc='sum')
    fig = px.imshow(df_pivot, title='Correlação entre os Valores de Imposto, Ano e Mês Por Estado Selecionado')
    st.plotly_chart(fig)


    # Definir a ordem correta dos meses
    meses_ordenados = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    df4['mês'] = pd.Categorical(df4['mês'], categories=meses_ordenados, ordered=True)
    # Agrupar os dados por estado e mês, somando os valores de imposto
    df_grouped = df4.groupby(['uf', 'mês'])['valor'].sum().reset_index()
    # Criar um gráfico de linhas múltiplas
    fig = px.line(df_grouped, x='mês', y='valor', color='uf', title='Evolução dos Valores de Imposto ao Longo dos Meses para os Diferentes Estados Por Ano')
    st.plotly_chart(fig)

    
    # Criar um gráfico de dispersão para visualizar a relação entre o valor do imposto e o ano por 
    fig = px.scatter(df, x='ano', y='valor', color='uf', title='Relação entre o Valor do Imposto e o Ano')
    st.plotly_chart(fig)



    