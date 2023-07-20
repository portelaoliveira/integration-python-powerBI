from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)  # criando o seu aplicativo Dash

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")

# plotly
fig_bar = px.bar(
    df, x="Produto", y="Quantidade", color="ID Loja", barmode="group"
)
fig_scatter = px.scatter(
    df,
    x="Quantidade",
    y="Valor Final",
    color="Produto",
    size="Valor Unitário",
    size_max=60,
)

lista_marcas = list(df["Marca"].unique())
lista_marcas.append("Todas")

# css
app.layout = html.Div(
    children=[
        html.H1(
            children="Meu Dashboard",
            style={"font-family": " Arial, Helvetica, sans-serif"},
        ),
        html.Div(children="""
        Dashboard de Vendas em Python
    """),
        html.H3(children="Vendas de cada Produto por Loja", id="subtitulo"),
        dcc.RadioItems(
            lista_marcas,
            value="Todas",
            id="selecao_marcas",
            inline=True,
            style={"color": "SlateGrey", "font-size": 20},
        ),
        dcc.Graph(id="vendas_por_loja", figure=fig_bar),
        dcc.Graph(id="vendas_distribuidas", figure=fig_scatter),
    ],
    style={"text-align": "center"},
)


# callbacks -> dar funcionalidade pro nosso dashboard (conecta os botões com os gráficos)
@app.callback(
    Output(
        "subtitulo", "children"
    ),  # eu quero modificar (eu quero que o botão do input modifique)
    Input(
        "selecao_marcas", "value"
    ),  # quem está modificando/de onde eu quero pegar a informacao/que tá fazendo um filtro
)
def selecionar_marca(marca):
    if marca == "Todas":
        texto = "Vendas de cada Produto por Loja"
    else:
        texto = f"Vendas de cada Produto por Loja da Marca {marca}"
    return texto


# colocando o seu site (seu dashboard) no ar
if __name__ == "__main__":
    app.run_server(debug=True)