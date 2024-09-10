import tkinter as tk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Configuração das variáveis fuzzy
historico_credito = ctrl.Antecedent(np.arange(0, 11, 1), 'historico_credito')
renda_mensal = ctrl.Antecedent(np.arange(0, 50001, 1), 'renda_mensal')  # Renda até 50.000
divida_atual = ctrl.Antecedent(np.arange(0, 501, 1), 'divida_atual')  # Dívida até 500% da renda
idade = ctrl.Antecedent(np.arange(18, 81, 1), 'idade')  # Idade de 18 a 80 anos

# Definindo a variável de saída
risco = ctrl.Consequent(np.arange(0, 101, 1), 'risco')

# Funções de pertinência para Histórico de Crédito
historico_credito['ruim'] = fuzz.trapmf(historico_credito.universe, [0, 0, 2, 4])
historico_credito['regular'] = fuzz.trimf(historico_credito.universe, [3, 5, 7])
historico_credito['bom'] = fuzz.trimf(historico_credito.universe, [6, 8, 10])
historico_credito['excelente'] = fuzz.trapmf(historico_credito.universe, [8, 9, 10, 10])

# Funções de pertinência para Renda Mensal
renda_mensal['baixa'] = fuzz.trapmf(renda_mensal.universe, [0, 0, 5000, 10000])
renda_mensal['media'] = fuzz.trimf(renda_mensal.universe, [8000, 15000, 25000])
renda_mensal['alta'] = fuzz.trapmf(renda_mensal.universe, [20000, 30000, 50000, 50000])

# Funções de pertinência para Dívida Atual (% da renda)
divida_atual['baixa'] = fuzz.trapmf(divida_atual.universe, [0, 0, 50, 100])
divida_atual['moderada'] = fuzz.trimf(divida_atual.universe, [80, 150, 250])
divida_atual['alta'] = fuzz.trapmf(divida_atual.universe, [200, 300, 500, 500])

# Funções de pertinência para Idade
idade['jovem'] = fuzz.trapmf(idade.universe, [18, 18, 25, 35])
idade['meia_idade'] = fuzz.trimf(idade.universe, [30, 45, 60])
idade['idoso'] = fuzz.trapmf(idade.universe, [55, 65, 80, 80])

# Funções de pertinência para Risco
risco['baixo'] = fuzz.trapmf(risco.universe, [0, 0, 20, 40])
risco['moderado'] = fuzz.trimf(risco.universe, [30, 50, 70])
risco['alto'] = fuzz.trapmf(risco.universe, [60, 80, 100, 100])

# Regras Fuzzy
rule1 = ctrl.Rule(historico_credito['excelente'] & divida_atual['baixa'], risco['baixo'])
rule2 = ctrl.Rule(historico_credito['ruim'] & divida_atual['alta'], risco['alto'])
rule3 = ctrl.Rule(historico_credito['bom'] & renda_mensal['media'] & divida_atual['moderada'], risco['moderado'])
rule4 = ctrl.Rule(historico_credito['regular'] & divida_atual['moderada'], risco['moderado'])
rule5 = ctrl.Rule(historico_credito['bom'] & renda_mensal['alta'], risco['baixo'])
rule6 = ctrl.Rule(historico_credito['ruim'] & renda_mensal['baixa'], risco['alto'])
rule7 = ctrl.Rule(historico_credito['ruim'] | renda_mensal['baixa'], risco['alto'])  # Fallback
rule8 = ctrl.Rule(historico_credito['excelente'] & renda_mensal['alta'] & divida_atual['baixa'], risco['baixo'])
rule9 = ctrl.Rule(historico_credito['bom'] & divida_atual['alta'], risco['alto'])
rule10 = ctrl.Rule(idade['jovem'] & renda_mensal['alta'] & divida_atual['baixa'], risco['baixo'])  # Jovem com alta renda e dívida baixa
rule11 = ctrl.Rule(idade['idoso'] & divida_atual['alta'], risco['alto'])  # Idoso com alta dívida tem maior risco

# Sistema de Controle Fuzzy
risco_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11])
risco_simulacao = ctrl.ControlSystemSimulation(risco_ctrl)

# Função para calcular o risco
def calcular_risco():
    try:
        hist = float(entry_hist.get())
        renda = float(entry_renda.get())
        divida = float(entry_divida.get())
        idade_valor = float(entry_idade.get())

        # Cálculo automático do percentual da dívida em relação à renda
        divida_percent = (divida / renda) * 100
        if divida_percent > 100:
            divida_percent = 100
        elif divida_percent < 0:
            divida_percent = 0

        # Verificação de intervalos
        if not (0 <= hist <= 10):
            resultado.set("Histórico de crédito fora do intervalo permitido.")
            return
        if not (0 <= renda <= 50000):
            resultado.set("Renda fora do intervalo permitido.")
            return
        if not (18 <= idade_valor <= 80):
            resultado.set("Idade fora do intervalo permitido.")
            return

        # Defina as variáveis fuzzy com os valores calculados
        risco_simulacao.input['historico_credito'] = hist
        risco_simulacao.input['renda_mensal'] = renda
        risco_simulacao.input['divida_atual'] = divida_percent
        risco_simulacao.input['idade'] = idade_valor

        # Adicionando debug para verificar o input
        print(f"Valores inseridos - Histórico: {hist}, Renda: {renda}, Dívida (%): {divida_percent}, Idade: {idade_valor}")

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

# Explicação inicial
explicacao = """
Bem-vindo ao Sistema de Análise de Risco Bancário!

Aqui estão as instruções para inserir os valores:

- Histórico de Crédito: Um valor de 0 a 10. Quanto maior o número, melhor o histórico de crédito.
- Renda Mensal: Insira sua renda mensal em reais, entre R$0 e R$50.000.
- Dívida: Insira o valor total de sua dívida atual em reais. A dívida é comparada com sua renda mensal.
- Idade: Insira sua idade (entre 18 e 80 anos).

Com base nesses dados, o sistema calculará o risco de crédito, variando de baixo a alto.
"""

tk.Label(root, text=explicacao, justify="left").grid(row=0, column=0, columnspan=2, padx=10, pady=10)

tk.Label(root, text="Histórico de Crédito (0 a 10):").grid(row=1)
tk.Label(root, text="Renda Mensal (R$):").grid(row=2)
tk.Label(root, text="Valor da Dívida (R$):").grid(row=3)
tk.Label(root, text="Idade (18 a 80):").grid(row=4)

entry_hist = tk.Entry(root)
entry_renda = tk.Entry(root)
entry_divida = tk.Entry(root)
entry_idade = tk.Entry(root)

entry_hist.grid(row=1, column=1)
entry_renda.grid(row=2, column=1)
entry_divida.grid(row=3, column=1)
entry_idade.grid(row=4, column=1)

resultado = tk.StringVar()
tk.Label(root, textvariable=resultado).grid(row=6, column=1)

btn_calcular_risco = tk.Button(root, text="Calcular Risco", command=calcular_risco)
btn_calcular_risco.grid(row=5, column=1, pady=10)

root.mainloop()
