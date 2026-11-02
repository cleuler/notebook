# CDE DPP - 2026.2
**Data:** 01/11/2026  
**Disciplina/Projeto:** Trabalho Final: Simulação

---

## Contexto: O País de Zircônia

Em um suposto país chamado Zircônia, vive uma população predominantemente de baixa renda, com Índice de Gini igual a 0,9. Nos últimos 10 anos, essa população vem se estabilizando e hoje já apresenta a mesma proporção de jovens e de idosos, com tendência futura de predomínio dos idosos.

Estima-se que na Zircônia vive uma população atual de 100 milhões de habitantes, com uma taxa de mortalidade infantil de cerca de 13,20 mortos para cada 1000 nascidos vivos.

O sistema público de saúde da Zircônia, o ZUS, promove em média 26,9 milhões de atendimentos gerais por semana. O número médio de internações hospitalares por semana é estimado em 104,2 mil.

O gasto público per capita anual com o ZUS encontra-se no seguinte intervalo de confiança: $750 \le x \le \$1000$ Zircônias (a moeda corrente do país, considere que $1Z = R\$ 2,40$), com nível de confiança de 95%, o que representa cerca de 4,2% do PIB do país.

Em razão de constantes e demoradas filas para internações hospitalares no ZUS, cerca de 50% da população de baixa renda busca a Defensoria Pública da Zircônia para garantir seu acesso à saúde. Isso ocorre seja pelo sistema de regulação do ZUS, seja na rede privada (neste caso, custeado por recursos públicos por meio de sequestro de verba pública que, segundo entendimento da Corte Superior da Zircônia, deveria seguir a tabela de custos do ZUS).

---

## Problemas de Pesquisa

1. **Acesso à Saúde e Justiça:** Uma pesquisa pretende estudar se há diferenças no acesso à saúde entre a parcela da população carente com e sem acesso ao sistema de justiça por meio da Defensoria Pública (que não se encontra capilarizada entre as 20 regiões e 5.000 municípios da Zircônia).
   * **Indicador:** Um dos indicadores que poderia ser mobilizado seria a proporção da população carente com e sem esses acessos, estratificado segundo variáveis como: domicílio, idade, sexo, renda familiar per capita, grau de instrução escolar e cor da pele (branca, parda, preta, amarela e indígena), que são periodicamente levantadas por amostras colhidas por Pesquisas Nacionais Domiciliares Contínuas da Zircônia.

2. **Controvérsia da Tabela de Custos:** Outro ponto controvertido é a pretensão dos Hospitais da rede particular junto ao judiciário da Zircônia ao pagamento da diferença entre a tabela de custos do ZUS e a tabela do governo para os Planos Privados de Saúde, quando seus beneficiários usam a rede pública, que é estimada em Z$ 12 bilhões por ano.

3. **Corte Orçamentário:** Um terceiro aspecto relevante é a decisão do governo zirconês de aplicar um corte orçamentário de Z$ 6 bilhões para os próximos 12 meses. A pesquisa pretende propor um indicador de impacto desse corte orçamentário sobre a parcela da população carente (com e sem os acessos à saúde pública e ao sistema de justiça), segundo os mesmos estratos já apontados anteriormente.

---

## 1. Simulação de Dados

O objetivo deste Trabalho Final é descrever as populações a serem pesquisadas, bem como suas unidades amostrais. Deve-se conceber um Quadro de Variáveis e seu respectivo Dicionário de Dados capazes de promover uma coleta adequada de dados que permita responder às três questões de interesse da pesquisa.

* **Variáveis Ocultas:** Promover uma reflexão sobre possíveis variáveis ocultas ou não observadas que poderiam interferir na validade externa e na descrição do fenômeno que se quer observar.
* **Dicionário de Dados:** Deve descrever minuciosamente todas as variáveis que serão observadas, apontando seu: nome abreviado, significado, tipo, escala de medição, unidade de medida, tipo Python adequado, papel ou função, exemplos, dentre outros aspectos necessários para a compreensão do ou dos conceitos que cada uma delas busca mobilizar.
* **Modelagem Numérica:** Para cada variável, segundo o contexto da Zircônia que foi apresentado, deve ser escolhido um modelo adequado de distribuição de probabilidade que, com base na literatura especializada ou uma amostra piloto ($n=50$) colhida de fontes de dados abertas, permita simular o mais próximo possível da realidade da Zircônia para geração de grandes amostras ($n \ge 1000$) realisticamente simuladas.
* **Qualidade dos Dados:** Também deverão ser simuladas unidades amostrais repetidas, faltantes e/ou com dados faltantes para algumas das variáveis observadas.

---

## 2. Objetivo Geral deste Trabalho Final

O principal objetivo do presente roteiro metodológico é servir de modelo a ser utilizado como guia para cada aluno realizar uma simulação adequada de dados aplicada ao seu projeto de pesquisa.

**O que lhe é exigido:**
* Conceber seu Quadro de Variáveis e Dicionário de Dados adequados ao seu problema de pesquisa já bem delimitado;
* Refletir sobre variáveis ocultas ou não observadas no contexto de sua pesquisa;
* Criar critérios de escolha realísticos sobre os modelos que serão utilizados para simular dados adequados ao fenômeno pesquisado.

## 3. Arquitetura e Estrutura de Dados
Seguir a Arquitetura e Estrutura de coleta, tratamento, curadoria e checagem dos dados coletados a partir desse processo cuidadoso e realístico de simulação, tomando por base os Estudos Dirigidos n. 2 e 3.

## 4. Aprofundamento do Trabalho Final
Aprofundar o detalhamento do seu Trabalho Final com relação às seguintes seções previstas no pipeline do seu PLANO customizado para a sua pesquisa junto ao PPGDP:
* Testes de Hipóteses adequados;
* Hipóteses da Modelagem, a partir dos dados;
* Critérios de escolha entre Modelos;
* Análise dos Resíduos;
* Testes de Hipóteses adequados para apoiar as escolhas nesse processo de Modelagem dos dados;
* Determinação do Tamanho da Amostra considerando erro tipo I, poder e o tamanho do efeito a ser detectado;
* Um inventário inicial dos outputs a serem produzidos pela sua pesquisa empírica.

## 5. Delineamento da Pesquisa
Ao final, pretende-se que cada aluno alcance, em seu Trabalho Final, uma composição do seu Delineamento da Pesquisa e seu Desenho Amostral, detalhados numa sequência de etapas e com um grau de aprofundamento que servirão como base para incrementar a validade interna e externa dos conceitos e construtos que foram mobilizados no seu Projeto de Pesquisa.

## 6. Depósito em Repositório
Permitir que esse Protocolo customizado e aprofundado da sua Pesquisa Empírica seja depositado em um Repositório reconhecido para garantir uma coleta de dados válidos, fidedignos e replicáveis, antes de iniciar qualquer coleta de campo.