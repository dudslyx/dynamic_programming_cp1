# ---------------------------
# RM's: 
# André Mateus Yoshimori - (563310), 
# Eduardo Francisco Mauro Gonçalves - (561969), 
# João Pedro Vieira Goés - (564459), 
# Mateus Nunes Araújo - (562008), 
# Matheus Henrique Ferreira Camargo da Silva - (566232).
#---------------------------

# IMPORTS
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # NOVO
import random

# ---------------------------
# 1. BASE DE DISTÂNCIAS (SIMULADA)
# ---------------------------
distancias = {
    ("SP", "RJ"): 430,
    ("SP", "MG"): 590,
    ("SP", "PR"): 410,
    ("SP", "BA"): 1960,
}

# ---------------------------
# 2. DICIONÁRIOS (CLIENTES E REGIÕES) 
# ---------------------------
clientes = {
    1: "Empresa A",
    2: "Empresa B",
    3: "Empresa C",
    4: "Empresa D",
    5: "Empresa E"
}

regioes = {
    "Sudeste": ["SP", "RJ", "MG"],
    "Sul": ["PR"],
    "Nordeste": ["BA"]
}

def identificar_regiao(destino):
    for regiao, estados in regioes.items():
        if destino in estados:
            return regiao
    return "Desconhecida"

# ---------------------------
# 3. LISTA DE CARGAS (TUPLAS)
# ---------------------------
cargas = [
    (1, "SP", "RJ", 2.5, 2, 5),
    (2, "SP", "MG", 2.0, 3, 3),
    (3, "SP", "PR", 1.8, 2, 4),
    (4, "SP", "BA", 3.0, 7, 1),
    (5, "SP", "RJ", 2.2, 1, 5),
]

# ---------------------------
# 4. FUNÇÕES
# ---------------------------
def obter_distancia(origem, destino):
    return distancias.get((origem, destino), 1000)

def calcular_frete(carga):
    _, origem, destino, custo_km, _, _ = carga
    km = obter_distancia(origem, destino)
    return km * custo_km

def simular_atraso(prazo):
    atraso = random.choice([0, 1])
    return prazo + atraso

def calcular_prioridade(carga):
    _, _, _, _, prazo, criticidade = carga
    frete = calcular_frete(carga)
    return (criticidade * 3) + (1 / prazo) + (1 / frete)

# ---------------------------
# 5. PREPARAÇÃO DOS DADOS
# ---------------------------
dados = []

for carga in cargas:
    frete = calcular_frete(carga)
    prazo_real = simular_atraso(carga[4])
    prioridade = calcular_prioridade(carga)
    
    dados.append({
        "ID": carga[0],
        "Cliente": clientes[carga[0]],  # uso do dicionário
        "Origem": carga[1],
        "Destino": carga[2],
        "Regiao": identificar_regiao(carga[2]),  # uso do dicionário
        "Frete": frete,
        "Prazo": carga[4],
        "Prazo_Real": prazo_real,
        "Criticidade": carga[5],
        "Prioridade": prioridade
    })

# ---------------------------
# 6. DATAFRAME
# ---------------------------
df = pd.DataFrame(dados)

# ---------------------------
# 7. ORDENAÇÃO
# ---------------------------
df = df.sort_values(by="Prioridade", ascending=False)

print("\nRanking de entregas:")
print(df)

# ---------------------------
# 8. DEQUE (FILA)
# ---------------------------
fila = deque(df.to_dict("records"))

print("\nProcessando entregas...\n")

while fila:
    entrega = fila.popleft()
    
    status = "NO PRAZO"
    if entrega["Prazo_Real"] > entrega["Prazo"]:
        status = "ATRASADA"
    
    print(f"Carga {entrega['ID']} ({entrega['Cliente']}) -> {entrega['Destino']} | {status}")

# ---------------------------
# 9. GRÁFICOS (MATPLOTLIB + SEABORN) ✅
# ---------------------------

# Frete por carga
plt.figure()
sns.barplot(x=df["ID"], y=df["Frete"])
plt.title("Custo de Frete por Carga")
plt.show()

# Prioridade
plt.figure()
sns.barplot(x=df["ID"], y=df["Prioridade"])
plt.title("Prioridade das Entregas")
plt.show()

# Frete por região 
plt.figure()
sns.barplot(data=df, x="Regiao", y="Frete")
plt.title("Frete por Região")
plt.show()

# ---------------------------
# 10. RECURSÃO
# ---------------------------
def soma_frete(lista, index=0):
    if index == len(lista):
        return 0
    return lista[index]["Frete"] + soma_frete(lista, index + 1)

total_frete = soma_frete(df.to_dict("records"))
print("\nCusto total de frete:", total_frete)