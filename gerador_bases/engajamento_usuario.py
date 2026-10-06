import pandas as pd
import numpy as np
from faker import Faker

fake = Faker('pt_BR')
np.random.seed(42)

def gerar_dados_engajamento_com_nulos(n_linhas=1000):
    dados = []
    
    for _ in range(n_linhas):
        dias_ativo_mes = np.random.randint(0, 31)
        minutos_assistidos = dias_ativo_mes * np.random.randint(5, 120)
        suporte_acionado = np.random.randint(0, 6)
        
        # Correlação do Target
        score_engajamento = (dias_ativo_mes * 3) + (minutos_assistidos * 0.01) - (suporte_acionado * 10)
        
        if score_engajamento < 25:
            categoria_engajamento = 'Baixo'
        elif score_engajamento < 70:
            categoria_engajamento = 'Médio'
        else:
            categoria_engajamento = 'Alto'
            
        # Introduzindo nulos propositais
        # Dias_Ativo_Mes terá ~7% de nulos e Minutos_Assistidos terá ~10% de nulos
        dias_final = np.nan if np.random.rand() < 0.07 else dias_ativo_mes
        minutos_final = np.nan if np.random.rand() < 0.10 else minutos_assistidos
        
        dados.append({
            'ID_Usuario': fake.uuid4(),
            'Email_Provedor': fake.free_email_domain(),
            'Dias_Ativo_Mes': dias_final,
            'Minutos_Assistidos': minutos_final,
            'Suporte_Acionado': suporte_acionado,
            'Engajamento': categoria_engajamento
        })
        
    return pd.DataFrame(dados)

df_engajamento = gerar_dados_engajamento_com_nulos(1000)
df_engajamento.to_csv('engajamento_clientes_nulos.csv', index=False)
print("\nBase Multiclasse com NULOS salva com sucesso!")
print(df_engajamento.isnull().sum())
