import tkinter as tk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Configuração das variáveis fuzzy
historico_credito = ctrl.Antecedent(np.arange(0, 11, 1), 'historico_credito')
renda_mensal = ctrl.Antecedent(np.arange(0, 10001, 1), 'renda_mensal')
divida_atual = ctrl.Antecedent(np.arange(0, 101, 1), 'divida_atual')

# Definindo a variável de saída
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

# Funções de pertinência para Dívida Atual (% da renda)
divida_atual['baixa'] = fuzz.trapmf(divida_atual.universe, [0, 0, 20, 40])
divida_atual['moderada'] = fuzz.trimf(divida_atual.universe, [30, 50, 70])
divida_atual['alta'] = fuzz.trapmf(divida_atual.universe, [60, 80, 100, 100])

# Funções de pertinência para Risco
risco['baixo'] = fuzz.trapmf(risco.universe, [0, 0, 20, 40])
risco['moderado'] = fuzz.trimf(risco.universe, [30, 50, 70])
risco['alto'] = fuzz.trapmf(risco.universe, [60, 80, 100, 100])

# Regras Fuzzy baseadas na entrevista
rule1 = ctrl.Rule(historico_credito['excelente'] & divida_atual['baixa'], risco['baixo'])
rule2 = ctrl.Rule(historico_credito['ruim'] & divida_atual['alta'], risco['alto'])
rule3 = ctrl.Rule(historico_credito['bom'] & renda_mensal['media'] & divida_atual['moderada'], risco['moderado'])
rule4 = ctrl.Rule(historico_credito['regular'] & divida_atual['moderada'], risco['moderado'])
rule5 = ctrl.Rule(historico_credito['bom'] & renda_mensal['alta'], risco['baixo'])  
rule6 = ctrl.Rule(historico_credito['ruim'] & renda_mensal['baixa'], risco['alto'])   
rule7 = ctrl.Rule(historico_credito['ruim'] | renda_mensal['baixa'], risco['alto'])  # Regra de fallback

# Adicionando uma regra de fallback para garantir que o sistema sempre tenha uma saída
rule_fallback = ctrl.Rule(antecedent=~(historico_credito['excelente'] & renda_mensal['alta'] & divida_atual['baixa']),
                          consequent=risco['alto'])

risco_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule_fallback])
risco_simulacao = ctrl.ControlSystemSimulation(risco_ctrl)

# Função para calcular o risco
def calcular_risco():
    try:
        hist = float(entry_hist.get())
        renda = float(entry_renda.get())
        divida = float(entry_divida.get())

        # Cálculo automático do percentual da dívida em relação à renda
        divida_percent = (divida / renda) * 100
        print(f"Divida Percentual: {divida_percent}")

        # Verificação de intervalos
        if not (0 <= hist <= 10):
            resultado.set("Histórico de crédito fora do intervalo permitido.")
            return
        if not (0 <= renda <= 10000):
            resultado.set("Renda fora do intervalo permitido.")
            return
        if divida_percent > 100:
            divida_percent = 100  # Limitar o percentual de dívida a 100%
        elif divida_percent < 0:
            divida_percent = 0

        # Defina as variáveis fuzzy com os valores calculados
        risco_simulacao.input['historico_credito'] = hist
        risco_simulacao.input['renda_mensal'] = renda
        risco_simulacao.input['divida_atual'] = divida_percent

        # Adicionando debug para verificar o input
        print(f"Valores inseridos - Histórico: {hist}, Renda: {renda}, Dívida (%): {divida_percent}")

        risco_simulacao.compute()
        
        resultado.set(f"Risco: {risco_simulacao.output['risco']:.2f}%")
    
    except KeyError as e:
        resultado.set(f"Erro ao calcular o risco. Chave não encontrada: {e}")
    except ValueError:
        resultado.set("Por favor, insira valores numéricos válidos.")
    except Exception as e:
        resultado.set(f"Ocorreu um erro inesperado: {str(e)}")

# Interface Gráfica com Tkinter
root = tk.Tk()
root.title("Sistema de Análise de Risco Bancário")

tk.Label(root, text="Histórico de Crédito (0 a 10):").grid(row=0)
tk.Label(root, text="Renda Mensal (R$):").grid(row=1)
tk.Label(root, text="Valor da Dívida (R$):").grid(row=2)

entry_hist = tk.Entry(root)
entry_renda = tk.Entry(root)
entry_divida = tk.Entry(root)

entry_hist.grid(row=0, column=1)
entry_renda.grid(row=1, column=1)
entry_divida.grid(row=2, column=1)

resultado = tk.StringVar()
tk.Label(root, textvariable=resultado).grid(row=4, column=1)

btn_calcular_risco = tk.Button(root, text="Calcular Risco", command=calcular_risco)
btn_calcular_risco.grid(row=3, column=1)

root.mainloop()
