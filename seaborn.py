import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# importando os arquivos
caminho_padrao = (
    r"C:\Users\RT-000312\Documents\workspace\integration-python-powerBI"
)
vendas_df = pd.read_csv(
    os.path.join(caminho_padrao, r"Contoso - Vendas - 2017.csv"), sep=";"
)
produtos_df = pd.read_csv(
    os.path.join(caminho_padrao, r"Contoso - Cadastro Produtos.csv"), sep=";"
)
lojas_df = pd.read_csv(
    os.path.join(caminho_padrao, r"Contoso - Lojas.csv"), sep=";"
)
clientes_df = pd.read_csv(
    os.path.join(caminho_padrao, r"Contoso - Clientes.csv"), sep=";"
)

# limpando apenas as colunas que queremos
clientes_df = clientes_df[["ID Cliente", "E-mail"]]
produtos_df = produtos_df[["ID Produto", "Nome da Marca"]]
lojas_df = lojas_df[["ID Loja", "Nome da Loja"]]

# mesclando e renomeando os dataframes
vendas_df = vendas_df.merge(produtos_df, on="ID Produto")
vendas_df = vendas_df.merge(lojas_df, on="ID Loja")
vendas_df = vendas_df.merge(clientes_df, on="ID Cliente").rename(
    columns={"E-mail": "E-mail do Cliente"}
)
# print(vendas_df)

tres_lojas_df = vendas_df[vendas_df["ID Loja"].isin([86, 306, 172])]
# tres_lojas_df['Data da Venda'] = pd.to_datetime(tres_lojas_df['Data da Venda'], format='%d/%m/%Y')
# print(tres_lojas_df)

sns.set_theme(style="darkgrid")

sns.lineplot(
    x="Data da Venda",
    y="Quantidade Vendida",
    hue="Nome da Loja",
    style="event",
    data=tres_lojas_df,
)

plt.show()
