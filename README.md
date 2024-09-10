# Sistema de Análise de Risco Bancário 🚀

Bem-vindo ao **Sistema de Análise de Risco Bancário**, uma aplicação poderosa que utiliza **lógica fuzzy** para calcular o risco de crédito de clientes, com base em variáveis como **histórico de crédito**, **renda mensal** e **valor da dívida atual**. Esse sistema tem o objetivo de facilitar a tomada de decisões no setor bancário, oferecendo uma análise rápida e precisa do risco de crédito.

## 📊 Funcionalidades Principais

- **Histórico de Crédito:** Avaliação da qualidade do histórico de crédito do cliente (escala de 0 a 10).
- **Renda Mensal:** Entrada da renda mensal do cliente em reais, até um valor de R$ 50.000.
- **Valor da Dívida Atual:** Verificação do valor total da dívida do cliente, com base em uma comparação percentual com a renda mensal.
- **Idade:** Considera a idade do cliente (entre 18 e 80 anos).
- **Cálculo de Risco:** Calcula o risco de crédito com base em todas as variáveis de entrada, fornecendo um resultado em porcentagem e uma descrição do risco (baixo, moderado, alto).

## 🧠 Lógica Fuzzy em Ação

Usamos **lógica fuzzy** para lidar com incertezas e fornecer um cálculo de risco mais flexível e realista. As regras fuzzy e funções de pertinência foram configuradas para interpretar as variáveis de entrada e fornecer uma análise robusta do risco.

## 🛠 Tecnologias Utilizadas

- **Python 3.12.5:** Linguagem principal de desenvolvimento.
- **Tkinter:** Interface gráfica simples e intuitiva.
- **SciKit-Fuzzy:** Biblioteca utilizada para implementação da lógica fuzzy.
- **Numpy:** Para cálculos matemáticos precisos.

## 🚀 Como Funciona o Sistema

1. O usuário insere as seguintes informações:
   - Histórico de crédito (0 a 10)
   - Renda mensal (até R$ 50.000)
   - Dívida atual (R$)
   - Idade (18 a 80 anos)
   
2. O sistema processa os dados usando regras fuzzy, calculando automaticamente a dívida como porcentagem da renda mensal.
   
3. O resultado é exibido em porcentagem, junto com uma classificação de risco (baixo, moderado, alto).
