import pandas as pd
import numpy as np
from faker import Faker

fake = Faker('pt_BR')
np.random.seed(42)

def gerar_dados_emprestimo_com_nulos(n_linhas=1000):
    dados = []
    
    for _ in range(n_linhas):
        renda_mensal = round(np.random.exponential(scale=4000) + 1500, 2)
        score_credito = np.random.randint(300, 1000)
        nome_limpo = np.random.choice([True, False], p=[0.75, 0.25])
        idade = np.random.randint(18, 70)
        
        # Correlação do Target
        pontos_risco = (score_credito * 0.5) + (renda_mensal * 0.05)
        if not nome_limpo:
            pontos_risco -= 300
            
        aprovado = 1 if pontos_risco > 400 and np.random.rand() > 0.1 else 0
        
        # Introduzindo nulos propositais
        # Renda_Mensal terá ~8% de nulos e Nome_Limpo terá ~12% de nulos
        renda_final = np.nan if np.random.rand() < 0.08 else renda_mensal
        nome_limpo_final = np.nan if np.random.rand() < 0.12 else nome_limpo
        
        dados.append({
            'Cliente': fake.name(),
            'Estado': fake.state_abbr(),
            'Idade': idade,
            'Renda_Mensal': renda_final,
            'Score_Credito': score_credito,
            'Nome_Limpo': nome_limpo_final,
            'Aprovado': aprovado
        })
        
    return pd.DataFrame(dados)

df_emprestimo = gerar_dados_emprestimo_com_nulos(1000)
df_emprestimo.to_csv('aprovacao_emprestimo_nulos.csv', index=False)
print("\nBase de Classificação Binária com NULOS salva com sucesso!")
print(df_emprestimo.isnull().sum())
