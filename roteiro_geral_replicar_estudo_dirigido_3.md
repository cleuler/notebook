# Roteiro Geral Básico - Estudo Dirigido n. 3

**Tema:** Identificação de Litigância Abusiva Predatória nos 14 JEC de Natal-RN  
**Público-alvo:** Alunos (com exceção do Rafael)  
**Data:** 18/10/2026  
**Autor:** Cleuler  

Agora indico os passos a seguir como roteiro básico para replicar o Estudo Dirigido n. 3 para os demais alunos.

---

## 1. Preparação do Modelo de Referência

1. Baixe o arquivo `EstudoCaso1_RafaelCosta.zip`.
2. Descompacte e salve o conteúdo no diretório raiz do seu ambiente Python padronizado para gerar notebooks.
3. Este arquivo servirá de modelo de referência para você gerar um notebook similar ao dele, mas agora voltado para o estudo dirigido n. 3.

---

## 2. Estruturação de Diretórios e Documentos

Você precisará baixar e fazer o upload dos documentos produzidos pela autora da pesquisa, Hadja Rayanne Holanda de Alencar, estruturando seu ambiente da seguinte forma:

### 2.1. Pasta de Textos (`txt/`)
Na pasta `txt` do diretório raiz, insira os seguintes arquivos:
* `ProjetoHadja_FinalCorrigidoBanca_9mar2026.docx`
* `26_08_MonografiaFinal_Hadja.docx`

### 2.2. Pasta de Dados (`dat/`)
Na pasta `dat` do diretório raiz, crie a subpasta `dat/estcaso_lide_pred` para armazenar os seguintes arquivos:
* `casos_novos_JEC_Natal_chamado_S1392344_21.05.2025.xlsx`: Data set com dados brutos (86.964 × 30) obtido por solicitação deferida pelo TJ-RN.
* `PlanilhaPreenchidaVariaveisCorrigida_CN_JE_S1422934_Mestrado_03_02.xlsx`: Amostra probabilística (595 × 34) coletada pela autora. Explore também outras abas deste arquivo (ex: resultado da amostragem, quadro de variáveis, número de casos novos por ano).
> *Nota:* A autora ainda não cruzou esses dados com o Datajud do CNJ para verificar eventuais problemas de subcobertura.

### 2.3. Pasta de Código Fonte (`src/`)
Caso ainda não exista, crie a pasta `src` no diretório raiz, com a subpasta `src/estcaso_lide_pred`. 
Aqui serão armazenados os arquivos Python gerados (`.py`) para execução de tarefas específicas (ex: `secao01_ambiente.py` e `build_notebook.py`). O `build_notebook.py`, ao ser executado após a geração de 10 seções consecutivas, irá gerar o seu notebook final.

### 2.4. Pasta de Imagens (`fig/`)
Baixe e salve na pasta `fig` do diretório raiz as seguintes imagens (renomeie-as exatamente como indicado antes do upload):
* `ParticaoS.jpg`
* `fig5.4_BayesTheorem.JPG`
* `Teorema_bayes.jpeg`

---

## 3. Planejamento com IA Generativa (O "Arquiteto")

Escolha uma IA generativa apropriada (ex: Claude Opus 4.6) para criar o roteiro de replicação da arquitetura do `EstudoCaso1_RafaelCosta`, com o objetivo de replicar os capítulos 3 e 4 da monografia de Hadja.

### 3.1. Prompt de Planejamento Sugerido:

> "Partindo dos seguintes arquivos:
> 'txt\ProjetoHadja_FinalCorrigidoBanca.docx'
> 'txt\26_08_MonografiaFinal_Hadja.docx', em especial seus capítulos 3 e 4,
> 'dat\estcaso_lide_pred\casos_novos_JEC_Natal_chamado_S1392344_21.05.2025.xlsx'
> e, em especial, 'dat\estcaso_lide_pred\PlanilhaPreenchidaVariaveisCorrigida_CN_JE_S1422934_Mestrado_03_02.xlsx'.
> 
> E considerando como modelo de partida os arquivos 'EstudoCaso1_RafaelCosta\README.md' e especialmente o arquivo 'EstudoCaso1_RafaelCosta\rafaelcc_ed1.ipynb' como uma boa prática de análise de tratamento, de exploração descritiva e de testes de hipótese e de elaboração de modelos a partir de dados empíricos, observando que esse projeto modelo se apoia nos arquivos Python armazenados na sua subpasta 'EstudoCaso1_RafaelCosta\src'.
> 
> Elaborar um planejamento, a ser utilizado pelo Claude Sonnet 4.6, para criar um novo arquivo 'estcaso_lide_pred.ipynb' e subpastas necessárias, no diretório raiz, para replicar todos os gráficos, tabelas, testes e modelos que constam dos capítulo 3 e 4 do arquivo 'txt\26_08_MonografiaFinal_Hadja.docx'."

Este prompt gerará o sequenciamento detalhado. Ele é qualificado por aproveitar o esforço de pesquisa da autora e a arquitetura validada pelo Rafael.

---

## 4. Validação e Comparação do Planejamento

Compare o roteiro obtido pela sua IA com o planejamento gerado pelo professor (arquivo `PLANO_estcaso_lide_pred.html`). 
*Importante: Não forneça este arquivo html para a sua IA antecipadamente para não quebrar a independência do seu aprendizado. Refine seus prompts criativamente.*

---

## 5. Geração e Execução dos Códigos Python (O "Engenheiro")

Inicie a sequência de geração dos 10 arquivos `.py` utilizando uma IA voltada para código (ex: Claude Sonnet 4.6). 
O primeiro arquivo esperado é o `src/estcaso_lide_pred/__init__.py`. 

### 5.1. O Prompt Iterativo (Recomendado)

Não peça tudo de uma vez. Siga a abordagem iterativa validada pelo Gemini Pro:

> "Atue como um Engenheiro de Dados e Analista de Dados Sênior. Sua tarefa é executar rigorosamente o planejamento detalhado no arquivo 'PLANO_estcaso_lide_pred.md', aproveitando outros códigos parciais gerados até aqui pelo Opus 4.6.
> 
> Como o projeto é extenso (10 seções, 12 gráficos, 17 tabelas), NÃO tente gerar tudo de uma vez. Vamos trabalhar de forma iterativa, seguindo estritamente a arquitetura de módulos (.py dentro de src/) detalhada na Seção 1 e a sequência da Seção 7 do plano.
> 
> Diretrizes globais para todas as suas gerações:
> 1. Comentar passo a passo todos os códigos gerados.
> 2. Utilizar encode UTF-8 compatível com Português do Brasil.
> 3. Em cada módulo, incluir os blocos que formarão as células Markdown com ricas análises em Português: tratamentos de dados, interpretação de gráficos/tabelas/testes de hipóteses, análises dos resultados, e a conclusão final com as limitações da pesquisa empírica (estudo observacional retrospectivo).
> 4. Incluir rigorosamente os asserts de validação mencionados na Seção 5 do plano.
> 
> Para começarmos, leia o arquivo e gere apenas o código referente ao Prompt 1 e Prompt 2 da Seção 7 (ou seja, _init_.py, secao01_ambiente.py e secao02_curadoria.py). Aguarde minha confirmação para prosseguir para as próximas seções."

### 5.2. Testes Contínuos

* Mantenha o arquivo com seus prompts (`Prompt_estcaso_lide_pred.txt`) acessível.
* **REGRA DE OURO:** Teste cada arquivo Python imediatamente após ser gerado utilizando scripts de validação (ex: `_inspecionar_colunas.py`, `_validar_secao06.py`). Esses testes previnem a quebra do notebook final.

---

## 6. Geração Final e Validação do Notebook

Uma vez finalizada a sequência iterativa:
1. Gere o arquivo final `estcaso_lide_pred.ipynb`.
2. Abra-o e execute célula por célula.
3. Confira os gráficos, tabelas e testes comparando com o relatório de pesquisa da Rayanne.

*(Para o Rafael, foi gerado adicionalmente o roteiro específico `estcaso_3_roteiro_atividades_rafael.md`).*

**Objetivo Final:** Para todos os demais alunos, a tarefa é seguir este passo a passo para ambientar-se com nosso processo de geração de códigos assistido por IA, essencial para a produção do trabalho final da disciplina.