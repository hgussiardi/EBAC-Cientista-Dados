#programa teste Streamlit
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date, datetime


def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig=plt)
    return None



# Configuração da página
st.set_page_config(page_title = 'SINASC Rondônia', 
                    page_icon='https://upload.wikimedia.org/wikipedia/commons/f/fa/Bandeira_de_Rond%C3%B4nia.svg',
                    layout='wide')

# Cabeçalho
st.title('__Benvindo a Primeira Aplicação__')
st.write('----')
st.header('Dados de Nascimento')
st.subheader('SINASC Rondônia')



st.sidebar.image('./rondonia.png')


data_atual = datetime.now()
st.sidebar.write(data_atual,primaryColor="purple")
st.sidebar.write('_Escolher Intervalo de Análise_')

#Leitura do arquivo
#DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#        'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
#data = pd.read_csv(DATA_URL, nrows=5)
#st.write(data)

data_load_state = st.text('Loading data...')
df = pd.read_csv('SINASC_RO_2019.csv')
data_load_state.text('Loading data...done!')


#Escolha de data
df.DTNASC = pd.to_datetime(df.DTNASC)
min_data = df.DTNASC.min()
max_data = df.DTNASC.max()

dt_inicial = st.sidebar.date_input('Data Inicial',
                             value = min_data,
                             min_value = min_data,
                             max_value = max_data)

dt_final = st.sidebar.date_input('Data Final',
                           value = max_data,
                           min_value = min_data,
                           max_value = max_data)

#Escolha da idade
idade = df['IDADEMAE'].unique()
idade_min = int(df.IDADEMAE.min())
idade_max = int(df.IDADEMAE.max())
idade_med = int(round(df.IDADEMAE.mean(),0))


idade_to_filter = st.sidebar.slider('idade',idade_min, idade_max, idade_med)  # min: 0h, max: 23h, default: 17h

df = df[(df['DTNASC'] >= pd.to_datetime(dt_inicial)) & (df['DTNASC'] <= pd.to_datetime(dt_final)) & (df['IDADEMAE'] <= idade_to_filter )]

#Print da tabela
#st.write(df)
if st.checkbox('Oculta Tabela de Dados',value=True):
    st.subheader('Tabela de Dados')
    #st.write(data)
    st.dataframe(df)

#Gráfico
st.write('----')
st.subheader('Estatistica de Peso do Bebê por Sexo')
plota_pivot_table(df, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')

#Histograma
st.write('----')
st.subheader('Histograma APGAR5')
hist_values = np.histogram(
    df['APGAR5'], bins=10, range=(0,10))[0]
  #  DATE_COLUMN
st.bar_chart(hist_values)

#Mapas
lst = [["Rondonia",-8.76183,-63.902]]
df_mapa = pd.DataFrame(lst, columns = ['Estado','lat','lon'])
st.write('-----')
st.subheader('Mapa Rondônia')
st.map(df_mapa)