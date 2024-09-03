import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Variáveis de entrada
historico_credito = ctrl.Antecedent(np.arange(0, 11, 1), 'historico_credito')
renda_mensal = ctrl.Antecedent(np.arange(0, 10001, 1), 'renda_mensal')
divida_atual = ctrl.Antecedent(np.arange(0, 101, 1), 'divida_atual')

# Variável de saída
risco = ctrl.Consequent(np.arange(0, 101, 1), 'risco')

# Funções de pertinência para Histórico de Crédito
historico_credito['ruim'] = fuzz.trapmf(historico_credito.universe, [0, 0, 2, 4])
historico_credito['regular'] = fuzz.trimf(historico_credito.universe, [3, 5, 7])
historico_credito['bom'] = fuzz.trimf(historico_credito.universe, [6, 8, 10])
historico_credito['excelente'] = fuzz.trapmf(historico_credito.universe, [8, 9, 10, 10])

# Funções de pertinência para Renda Mensal
renda_mensal['baixa'] = fuzz.trapmf(renda_mensal.universe, [0, 0, 2000, 4000])
renda_mensal['media'] = fuzz.trimf(renda_mensal.universe, [3000, 5000, 7000])
renda_mensal['alta'] = fuzz.trapmf(renda_mensal.universe, [6000, 8000, 10000, 10000])

# Funções de pertinência para Dívida Atual
divida_atual['baixa'] = fuzz.trapmf(divida_atual.universe, [0, 0, 20, 40])
divida_atual['moderada'] = fuzz.trimf(divida_atual.universe, [30, 50, 70])
divida_atual['alta'] = fuzz.trapmf(divida_atual.universe, [60, 80, 100, 100])

# Funções de pertinência para Risco
risco['baixo'] = fuzz.trapmf(risco.universe, [0, 0, 20, 40])
risco['moderado'] = fuzz.trimf(risco.universe, [30, 50, 70])
risco['alto'] = fuzz.trapmf(risco.universe, [60, 80, 100, 100])

rule1 = ctrl.Rule(historico_credito['excelente'] & divida_atual['baixa'], risco['baixo'])
rule2 = ctrl.Rule(historico_credito['ruim'] & divida_atual['alta'], risco['alto'])
rule3 = ctrl.Rule(historico_credito['bom'] & renda_mensal['media'] & divida_atual['moderada'], risco['moderado'])
rule4 = ctrl.Rule(historico_credito['regular'] & divida_atual['moderada'], risco['moderado'])

# Outras regras podem ser adicionadas conforme necessário

# Criando o sistema de controle
risco_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
risco_simulacao = ctrl.ControlSystemSimulation(risco_ctrl)

# Exemplo de valores de entrada
risco_simulacao.input['historico_credito'] = 6  # Bom
risco_simulacao.input['renda_mensal'] = 5000  # Média
risco_simulacao.input['divida_atual'] = 50  # Moderada

# Computando o risco
risco_simulacao.compute()

# Resultado
print(risco_simulacao.output['risco'])
