from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_auth

USUARIOS = {
    "Portela": "123456",
}

app = Dash(__name__)  # criando o seu aplicativo Dash
auth = dash_auth.BasicAuth(app, USUARIOS)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")

lista_marcas = list(df["Marca"].unique())
lista_marcas.append("Todas")

lista_paises = list(df["País"].unique())
lista_paises.append("Todos")

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
            options=lista_marcas,
            value="Todas",
            id="selecao_marcas",
            inline=True,
            style={"color": "SlateGrey", "font-size": 20},
        ),
        html.Div(
            children=[
                dcc.Dropdown(
                    options=lista_paises,
                    value="Todos",
                    id="selecao_pais",
                    style={"color": "SlateGrey", "font-size": 20},
                ),
                html.Div(id="pais_selecionado"),
            ],
            style={"width": "50%", "margin": "auto"},
        ),
        dcc.Graph(id="vendas_por_loja"),
        dcc.Graph(id="vendas_distribuidas"),
    ],
    style={"text-align": "center"},
)


@app.callback(
    Output("selecao_pais", "options"),
    Input("selecao_marcas", "value"),
)
def opcoes_pais(marca):
    # criar uma lógica que diga qual a lista de paises que ele vai pegar
    if marca == "Todas":
        nova_lista_paises = list(df["País"].unique())
        nova_lista_paises.append("Todos")
    else:
        df_filtrada = df.loc[df["Marca"] == marca, :]
        nova_lista_paises = list(df_filtrada["País"].unique())
        nova_lista_paises.append("Todos")
    return nova_lista_paises


# callbacks -> dar funcionalidade pro nosso dashboard (conecta os botões com os gráficos)
@app.callback(
    Output(
        "subtitulo", "children"
    ),  # eu quero modificar (eu quero que o botão do input modifique)
    Output("vendas_por_loja", "figure"),
    Output("vendas_distribuidas", "figure"),
    Input(
        "selecao_marcas", "value"
    ),  # quem está modificando/de onde eu quero pegar a informacao/que tá fazendo um filtro
    Input("selecao_pais", "value"),
)
def selecionar_marca(marca, pais):
    if marca == "Todas" and pais == "Todos":
        texto = "Vendas de cada Produto por Loja"
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
    else:
        df_filtrada = df
        if marca != "Todas":
            # filtrar de acordo com a marca
            df_filtrada = df_filtrada.loc[df_filtrada["Marca"] == marca, :]
        if pais != "Todos":
            # filtrar de acordo com o pais
            df_filtrada = df_filtrada.loc[df_filtrada["País"] == pais, :]

        texto = (
            f"Vendas de cada Produto por Loja da Marca {marca} e do País"
            f" {pais}"
        )
        fig_bar = px.bar(
            df_filtrada,
            x="Produto",
            y="Quantidade",
            color="ID Loja",
            barmode="group",
        )
        fig_scatter = px.scatter(
            df_filtrada,
            x="Quantidade",
            y="Valor Final",
            color="Produto",
            size="Valor Unitário",
            size_max=60,
        )
    return texto, fig_bar, fig_scatter


@app.callback(
    Output("pais_selecionado", "children"),
    Input("selecao_pais", "value"),
)
def update_output(value):
    return f"Você selecionou o País: {value}"


# colocando o seu site (seu dashboard) no ar
if __name__ == "__main__":
    app.run_server(debug=True)
