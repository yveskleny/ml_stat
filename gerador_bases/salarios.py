import pandas as pd
import numpy as np
from faker import Faker

fake = Faker('pt_BR')
np.random.seed(42)

def gerar_dados_salario_com_nulos(n_linhas=1000):
    dados = []
    cargos = ['Junior', 'Pleno', 'Senior', 'Especialista']
    
    for _ in range(n_linhas):
        idade = np.random.randint(20, 55)
        anos_experiencia = max(0, idade - np.random.randint(18, 25))
        nivel_ingles = np.random.choice(['Básico', 'Intermediário', 'Avançado'], p=[0.3, 0.5, 0.2])
        cargo = np.random.choice(cargos, p=[0.4, 0.3, 0.2, 0.1])
        
        # Correlação do Target
        salario_base = 3000
        modificador_exp = anos_experiencia * 600
        modificador_ingles = 1500 if nivel_ingles == 'Avançado' else (500 if nivel_ingles == 'Intermediário' else 0)
        modificador_cargo = cargos.index(cargo) * 2500
        ruido = np.random.normal(0, 400)
        
        salario_final = salario_base + modificador_exp + modificador_ingles + modificador_cargo + ruido
        
        # Introduzindo nulos propositais de forma controlada
        # Idade terá ~10% de nulos e Nivel_Ingles terá ~15% de nulos
        idade_final = np.nan if np.random.rand() < 0.10 else idade
        nivel_ingles_final = np.nan if np.random.rand() < 0.15 else nivel_ingles
        
        dados.append({
            'Nome': fake.name(),
            'Idade': idade_final,
            'Anos_Experiencia': anos_experiencia,
            'Nivel_Ingles': nivel_ingles_final,
            'Cargo': cargo,
            'Salario': round(max(2500, salario_final), 2)
        })
        
    return pd.DataFrame(dados)

df_salario = gerar_dados_salario_com_nulos(1000)
df_salario.to_csv('previsao_salarios_nulos.csv', index=False)
print("Base de Regressão com NULOS salva com sucesso!")
print(df_salario.isnull().sum())  # Exibe a contagem de nulos criados
