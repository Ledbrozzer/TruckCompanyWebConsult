#pip install streamlit
#streamlit run nome_do_seu_arquivo.py
# $ streamlit run yourscript.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
tabela = pd.read_csv('Abastecimento_Caminhao.csv', delimiter=';', on_bad_lines='skip')
colunas_para_excluir = ["Requisição", "Hora Abast.", "Obs.", "Abast. Externo", "Combustível"]
colunas_existentes = [col for col in colunas_para_excluir if col in tabela.columns]
if colunas_existentes:
    tabela = tabela.drop(columns=colunas_existentes)

# Entradas do usuário
requisitante = st.text_input('Requisitante', 'GESSE')
veiculo = st.text_input('Veículo', 'BT220')
data_inicial = st.date_input('Data inicial')
data_final = st.date_input('Data final')

# Filtrar os dados
tabela['Data Req.'] = pd.to_datetime(tabela['Data Req.'], format='%d/%m/%Y')
filtro = tabela[(tabela['Requisitante'].str.contains(requisitante, case=False, na=False)) &
                (tabela['Veículo/Equip.'].str.contains(veiculo, case=False, na=False)) &
                (tabela['Data Req.'] >= pd.to_datetime(data_inicial)) &
                (tabela['Data Req.'] <= pd.to_datetime(data_final))]

# Mostrar o gráfico
st.write("Dados Filtrados:")
st.write(filtro)
fig = px.histogram(filtro, x='Km Rodados', color='Km Rodados', title=f'Gráfico de Km Rodados para {requisitante} - {veiculo}')
st.plotly_chart(fig)