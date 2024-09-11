# Sistema de Análise de Risco Bancário 🚀

Bem-vindo ao **Sistema de Análise de Risco Bancário**, uma aplicação poderosa que utiliza **lógica fuzzy** para calcular o risco de crédito de clientes, com base em variáveis como **histórico de crédito**, **renda mensal**, **valor da dívida atual** e **idade**. Esse sistema foi criado para facilitar a tomada de decisões no setor bancário, oferecendo uma análise rápida e precisa do risco de crédito.

## 📊 Funcionalidades Principais

- **Histórico de Crédito**: Avaliação da qualidade do histórico de crédito do cliente, variando de 0 a 10.
- **Renda Mensal**: Entrada da renda mensal do cliente em reais (até R$ 50.000).
- **Valor da Dívida Atual**: Verificação do valor total da dívida do cliente, comparando-o com a renda mensal.
- **Idade**: Considera a idade do cliente (entre 18 e 80 anos).
- **Cálculo de Risco**: O sistema calcula o risco de crédito, fornecendo um resultado em porcentagem e uma descrição do risco (baixo, moderado, alto).

## 🛠 Tecnologias Utilizadas

- **Python 3.12.5**: Linguagem principal de desenvolvimento.
- **Tkinter**: Interface gráfica simples e intuitiva.
- **SciKit-Fuzzy**: Biblioteca utilizada para implementação da lógica fuzzy.
- **NumPy**: Para cálculos matemáticos precisos.

## 🧠 Lógica Fuzzy em Ação

A lógica fuzzy é utilizada para lidar com incertezas e fornecer um cálculo de risco mais flexível e realista. As variáveis de entrada (histórico de crédito, renda mensal, dívida atual e idade) são processadas por funções de pertinência e regras fuzzy, que geram um resultado em termos de risco (baixo, moderado ou alto).

### Variáveis de Entrada

1. **Histórico de Crédito**: De 0 (pior) a 10 (melhor).
2. **Renda Mensal**: De R$ 0 a R$ 50.000.
3. **Valor da Dívida Atual**: Representado como percentual da renda mensal, de 0% a 500%.
4. **Idade**: De 18 a 80 anos.

### Regras Fuzzy

- Se o **histórico de crédito** é excelente e a **dívida** é baixa, o **risco** é baixo.
- Se o **histórico de crédito** é ruim e a **dívida** é alta, o **risco** é alto.
- Se a **renda** é alta e a **dívida** é baixa, o **risco** é baixo.
- Outras combinações de variáveis afetam o risco de forma moderada ou alta, conforme as regras estabelecidas.

### Exemplo de Uso

1. O usuário insere um **histórico de crédito** de 8, **renda mensal** de R$ 30.000, **dívida** de R$ 5.000 e **idade** de 35 anos.
2. O sistema calcula a dívida como 16.67% da renda mensal.
3. Com base nas regras fuzzy, o sistema gera um **risco de 50%**, classificado como **moderado**.

## 🚀 Como Executar o Sistema

### Pré-requisitos

- Python 3.12.5 instalado.
- Bibliotecas necessárias: `tkinter`, `numpy`, `skfuzzy`.

### Instalação

1. Clone este repositório:
   git clone <https://github.com/emannuelop/BankRiskAnalysisSystem>
    cd BankRiskAnalysisSystem

2. Instale as dependências:
    pip install numpy scikit-fuzzy

### Execução

1. No terminal, execute o seguinte comando para iniciar o sistema:
    python sistema_risco_bancario.py

2. Uma interface gráfica será aberta. Insira os dados solicitados (histórico de crédito, renda, dívida e idade), e clique em "Calcular Risco" para visualizar o resultado.
