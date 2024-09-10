import tkinter as tk
from tkinter import ttk
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

# Função para obter a descrição textual com base no valor do risco
def obter_descricao_risco(valor_risco):
    if valor_risco <= 20:
        return 'Baixo'
    elif valor_risco <= 70:
        return 'Moderado'
    else:
        return 'Alto'

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

        risco_simulacao.compute()
        
        valor_risco = risco_simulacao.output['risco']
        descricao_risco = obter_descricao_risco(valor_risco)
        
        resultado.set(f"Risco: {valor_risco:.2f}% ({descricao_risco})")
    
    except KeyError as e:
        resultado.set(f"Erro ao calcular o risco. Chave não encontrada: {e}")
    except ValueError:
        resultado.set("Por favor, insira valores numéricos válidos.")
    except Exception as e:
        resultado.set(f"Ocorreu um erro inesperado: {str(e)}")

# Interface Gráfica com Tkinter
root = tk.Tk()
root.title("Sistema de Análise de Risco Bancário")
root.geometry("800x500")

# Estilo da interface
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12), padding=5)
style.configure("TEntry", font=("Helvetica", 12))

# Configuração de cores
root.configure(bg='#ffffff')  # Fundo branco
style.configure("TLabel", background='#ffffff', foreground='#000000')  # Letras pretas
style.configure("TButton", background='#000000', foreground='#000000')  # Botão preto com letras pretas
style.map("TButton", background=[('active', '#333333')])  # Botão ativo com fundo cinza escuro

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

ttk.Label(root, text=explicacao, justify="left").grid(row=0, column=0, columnspan=2, padx=10, pady=10)

ttk.Label(root, text="Histórico de Crédito (0 a 10):").grid(row=1, column=0, padx=10, pady=5, sticky="W")
ttk.Label(root, text="Renda Mensal (R$):").grid(row=2, column=0, padx=10, pady=5, sticky="W")
ttk.Label(root, text="Valor da Dívida (R$):").grid(row=3, column=0, padx=10, pady=5, sticky="W")
ttk.Label(root, text="Idade:").grid(row=4, column=0, padx=10, pady=5, sticky="W")

entry_hist = ttk.Entry(root)
entry_hist.grid(row=1, column=1, padx=10, pady=5)

entry_renda = ttk.Entry(root)
entry_renda.grid(row=2, column=1, padx=10, pady=5)

entry_divida = ttk.Entry(root)
entry_divida.grid(row=3, column=1, padx=10, pady=5)

entry_idade = ttk.Entry(root)
entry_idade.grid(row=4, column=1, padx=10, pady=5)

# Resultado do cálculo
resultado = tk.StringVar()
ttk.Label(root, textvariable=resultado, font=("Helvetica", 14, "bold")).grid(row=5, column=0, columnspan=2, padx=10, pady=20)

# Botão para calcular o risco
ttk.Button(root, text="Calcular Risco", command=calcular_risco).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
