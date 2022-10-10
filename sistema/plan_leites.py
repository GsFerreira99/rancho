import pandas as pd


def gerar_plan(dados):
    df = pd.DataFrame(dados)
    df.to_excel("output.xlsx", index=False)
