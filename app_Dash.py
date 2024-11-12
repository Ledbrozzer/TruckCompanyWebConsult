#pip install dash

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Dados de exemplo
tabela = pd.read_csv('Abastecimento_Caminhao.csv', delimiter=';', on_bad_lines='skip')
colunas_para_excluir = ["Requisição", "Hora Abast.", "Obs.", "Abast. Externo", "Combustível"]
colunas_existentes = [col for col in colunas_para_excluir if col in tabela.columns]
if colunas_existentes:
    tabela = tabela.drop(columns=colunas_existentes)

# Layout do Dash
app.layout = html.Div([
    dcc.Input(id='input-requisitante', type='text', value='GESSE', placeholder='Requisitante'),
    dcc.Input(id='input-veiculo', type='text', value='BT220', placeholder='Veículo'),
    dcc.Input(id='input-data-inicial', type='text', value='01/04/2024', placeholder='Data Inicial (DD/MM/AAAA)'),
    dcc.Input(id='input-data-final', type='text', value='31/07/2024', placeholder='Data Final (DD/MM/AAAA)'),
    dcc.Graph(id='grafico')
])

@app.callback(
    Output('grafico', 'figure'),
    [Input('input-requisitante', 'value'),
     Input('input-veiculo', 'value'),
     Input('input-data-inicial', 'value'),
     Input('input-data-final', 'value')]
)
def update_graph(requisitante, veiculo, data_inicial, data_final):
    tabela['Data Req.'] = pd.to_datetime(tabela['Data Req.'], format='%d/%m/%Y')
    data_inicial = pd.to_datetime(data_inicial, format='%d/%m/%Y')
    data_final = pd.to_datetime(data_final, format='%d/%m/%Y')

    filtro = tabela[(tabela['Requisitante'].str.contains(requisitante, case=False, na=False)) &
                    (tabela['Veículo/Equip.'].str.contains(veiculo, case=False, na=False)) &
                    (tabela['Data Req.'] >= data_inicial) &
                    (tabela['Data Req.'] <= data_final)]

    fig = px.histogram(filtro, x='Km Rodados', color='Km Rodados', title=f'Gráfico de Km Rodados para {requisitante} - {veiculo}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)