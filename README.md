# Análise Descritiva da Evasão em Cursos de Computação no Brasil

Um estudo multidimensional sobre o abandono discente em cursos de tecnologia, utilizando microdados educacionais para entender o impacto das categorias administrativas, modalidades de ensino e diversidade de gênero.

## O Problema

O Brasil enfrenta um déficit projetado de mais de 500 mil profissionais de tecnologia até 2029. Apesar do aumento de matrículas na área de Computação, a retenção de alunos é um desafio crítico. Este projeto utiliza análise de dados para mapear onde o "vazamento" de talentos é mais grave, fornecendo um diagnóstico nacional embasado em dados públicos oficiais.

## Tecnologias Utilizadas

* **Python 3**
* **Pandas** (Tratamento de dados, agregações e Feature Engineering)
* **Pandas / Matplotlib** (Visualização de dados e Boxplots)

## Fonte de Dados
Os dados empíricos foram extraídos dos **Microdados do Censo da Educação Superior (2024)**, disponibilizados pelo [Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP)](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior).

## Metodologia e Processamento

Para garantir a integridade da análise e evitar a distorção por dados duplicados de polos/turnos, o pipeline de dados seguiu as seguintes etapas:
1. **Merge:** Junção das tabelas de Cadastro de Cursos e Instituições (IES) utilizando a chave primária `CO_IES`.
2. **Agregação:** Uso do método `groupby` focado na chave primária `CO_CURSO` para consolidar o número real de alunos por unidade acadêmica.
3. **Engenharia de Recursos:** Criação das taxas percentuais relativas (Taxa de Evasão e Percentual de Mulheres por turma).
4. **Estatística:** Utilização da **Mediana** e do **Intervalo Interquartil (IQR)** para contornar a alta assimetria e presença de *outliers* extremos nos dados educacionais.

## Principais Achados

* **Rede de Ensino:** A rede privada apresenta uma evasão mediana quase duas vezes superior (25,16%) em comparação à rede pública (13,08%).
* **Modalidade:** O formato EAD demonstrou alta instabilidade, atingindo uma mediana de evasão crítica de 31,82%, contra 18,75% do formato presencial.
* **Diversidade de Gênero:** Turmas com poucas mulheres (com até 10% de mulheres) registram as maiores taxas de abandono (24,71%). A presença feminina estabiliza a retenção, reforçando a importância de redes de apoio à diversidade.

## Como executar o projeto localmente

Clone o repositório e configure seu ambiente virtual (Linux):

```bash
# Clone o repositório
git clone [https://github.com/CarolB57/evasao-computacao-brasil](https://github.com/CarolB57/evasao-computacao-brasil)
cd nome-do-repositorio

# Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
