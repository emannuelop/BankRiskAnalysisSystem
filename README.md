# Sistema de Análise de Risco Bancário

Este projeto é um Sistema de Análise de Risco Bancário que utiliza lógica fuzzy para determinar o risco de crédito de um cliente. O sistema considera três variáveis de entrada: histórico de crédito, renda mensal e valor da dívida atual. Com base nessas informações, ele calcula o risco de crédito associado ao cliente.

## Funcionalidades

- **Histórico de Crédito:** Avalia a qualidade do histórico de crédito do cliente em uma escala de 0 a 10.
- **Renda Mensal:** Considera a renda mensal do cliente em reais (R$), com um limite de até R$ 10.000.
- **Valor da Dívida:** Considera o valor atual da dívida do cliente em reais (R$).
- **Cálculo do Risco:** Com base nas variáveis de entrada, o sistema calcula o risco de crédito do cliente, expressando-o como uma porcentagem.

## Tecnologias Utilizadas

- **Python 3.12.5**
- **Tkinter:** Utilizado para a interface gráfica.
- **SciKit-Fuzzy:** Biblioteca utilizada para a lógica fuzzy e a criação do sistema de controle.
