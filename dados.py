import pandas as pd
from great_tables import GT
import matplotlib.pyplot as plt

class Data_Statistics:
    def __init__(self):
        df_ies = pd.read_csv('MICRODADOS_ED_SUP_IES_2024.CSV', sep=';', encoding='latin1', usecols=['CO_IES', 'NO_IES', 'SG_IES'])
        df_cursos = pd.read_csv('MICRODADOS_CADASTRO_CURSOS_2024.CSV', sep=';', encoding='latin1', usecols=['CO_IES', 'CO_CURSO', 'NO_CURSO', 'QT_SIT_DESVINCULADO', 
                                                                                                            'QT_MAT', 'TP_REDE', 'TP_MODALIDADE_ENSINO',
                                                                                                            'QT_MAT_MASC', 'QT_MAT_FEM'])
        
        self.df = pd.merge(df_cursos, df_ies, on='CO_IES')
        self.df = self.df[self.df['NO_CURSO'].str.contains(r'(^computação$)|Ciências? d[ae] computação|^Computação e Informática$', case=False, regex=True, na=False)]

        self.df = self.df.groupby('CO_CURSO').agg({
            'QT_SIT_DESVINCULADO': 'sum',
            'QT_MAT_FEM': 'sum',
            'QT_MAT': 'sum',
            'NO_CURSO': 'first',
            'NO_IES': 'first',
            'SG_IES': 'first',
            'TP_REDE': 'first',
            'TP_MODALIDADE_ENSINO': 'first'
        }).reset_index()

        self.mediana = {}
        self.q1 = {}
        self.q3 = {}
        self.iqr = {}
        self.total_cursos = {}
    
    def calc_taxas(self):
        self.df['TAXA_EVASAO'] = (self.df['QT_SIT_DESVINCULADO'] / self.df['QT_MAT']) * 100
        
        self.df['PERC_MULHERES'] = (self.df['QT_MAT_FEM'] / self.df['QT_MAT']) * 100

        self.df['TIPO_INSTITUICAO'] = self.df['TP_REDE'].map({1: 'Pública', 2: 'Privada'})
        self.df['MODALIDADE'] = self.df['TP_MODALIDADE_ENSINO'].map({1: 'EAD', 2: 'Presencial'})

        # Additionally, clean the dataframe (exclude NaN values in interested columns)

        self.df = self.df.dropna(subset=[
            'TAXA_EVASAO', 
            'PERC_MULHERES',
            'TIPO_INSTITUICAO',
            'MODALIDADE'
        ])

    def mediana_iqr(self, coluna, filtro=None):

        if filtro is None:
            df = self.df # Se não tem filtro, usa o DataFrame inteiro
        else:
            df = self.df[filtro]
        
        self.total_cursos[coluna] = df['CO_CURSO'].nunique()
        
        self.q1[coluna] = df['TAXA_EVASAO'].quantile(0.25)
        self.q3[coluna] = df['TAXA_EVASAO'].quantile(0.75)
        self.iqr[coluna] = self.q3[coluna] - self.q1[coluna]
        self.mediana[coluna] = df['TAXA_EVASAO'].median()

    def show_metrics(self, tag):
        mediana = self.mediana.get(tag, "Métrica não calculada.")
        iqr = self.iqr.get(tag, "Métrica não calculada.")
        q1 = self.q1.get(tag, "Métrica não calculada.")
        q3 = self.q3.get(tag, "Métrica não calculada.")
        total_cursos = self.total_cursos.get(tag, "Métrica não calculada.")

        print(f"Mediana {tag}: {mediana.round(2)}%.")
        print(f"IQR {tag}: {iqr.round(2)}%, variando de {q1.round(2)} a {q3.round(2)}%.")
        print(f"Total de Cursos nesta categoria: {total_cursos}.\n\n")

    def plot_boxplot(self, coluna, title, xlabel):
        self.df.boxplot(column='TAXA_EVASAO', by=coluna, widths=0.5)
        plt.xlabel(xlabel)
        plt.ylabel('')
        #plt.ylabel('Taxa de Evasão (%)')
        plt.ylim(0,600)
        plt.suptitle('')
        plt.tight_layout()
        plt.title('')
        #plt.title(title)
        plt.show()

    def comparative_table(self):
        tabela_descritiva = pd.DataFrame({
            "Categoria": [
                "Brasil Geral", 
                "Instituição Pública", 
                "Instituição Privada",
                "Modalidade EAD",
                "Modalidade Presencial",
                "Presença Feminina: Até 10%",
                "Presença Feminina: De 10% a 20%",
                "Presença Feminina: Mais de 20%"
            ],
            "N": [
                self.total_cursos["Brasil Geral"], 
                self.total_cursos["Instituição Pública"],
                self.total_cursos["Instituição Privada"],
                self.total_cursos["Modalidade EAD"],
                self.total_cursos["Modalidade Presencial"],
                self.total_cursos["Presença Feminina: Até 10%"],
                self.total_cursos["Presença Feminina: De 10% a 20%"],
                self.total_cursos["Presença Feminina: Mais de 20%"]
            ],
            "Mediana": [ # NOME SIMPLES (Sem o %)
                self.mediana["Brasil Geral"], 
                self.mediana["Instituição Pública"],
                self.mediana["Instituição Privada"],
                self.mediana["Modalidade EAD"],
                self.mediana["Modalidade Presencial"],
                self.mediana["Presença Feminina: Até 10%"],
                self.mediana["Presença Feminina: De 10% a 20%"],
                self.mediana["Presença Feminina: Mais de 20%"]
            ],
            "IQR": [ # NOME SIMPLES (Sem o %)
                self.iqr["Brasil Geral"], 
                self.iqr["Instituição Pública"],
                self.iqr["Instituição Privada"],
                self.iqr["Modalidade EAD"],
                self.iqr["Modalidade Presencial"],
                self.iqr["Presença Feminina: Até 10%"],
                self.iqr["Presença Feminina: De 10% a 20%"],
                self.iqr["Presença Feminina: Mais de 20%"]
            ]
        })

        # 3. Gerando a tabela final
        tabela_final = (
            GT(tabela_descritiva)
            .tab_header(
                title="Tabela 1: Perfil Descritivo da Evasão nos Cursos de Computação",
                subtitle="Brasil, Censo da Educação Superior 2024"
            )
            .cols_label(
                Categoria="Categoria de Análise",
                N="Número Cursos",
                Mediana="Mediana (%)", # Aqui entra a roupa bonita!
                IQR="IQR (%)"          # Aqui entra a roupa bonita!
            )
            .fmt_number(columns=["Mediana", "IQR"], decimals=2)
        )
        tabela_final.show()

df_computacao = Data_Statistics()
df_computacao.calc_taxas()

categoria_geral = 'Brasil Geral'
df_computacao.mediana_iqr(categoria_geral)
df_computacao.show_metrics(categoria_geral)

categoria_pub = 'Instituição Pública'
filtro_publica = df_computacao.df['TIPO_INSTITUICAO'] == 'Pública'
df_computacao.mediana_iqr(categoria_pub, filtro=filtro_publica)
df_computacao.show_metrics(categoria_pub)

categoria_priv = 'Instituição Privada'
filtro_privada = df_computacao.df['TIPO_INSTITUICAO'] == 'Privada'
df_computacao.mediana_iqr(categoria_priv, filtro=filtro_privada)
df_computacao.show_metrics(categoria_priv)

categoria_ead = 'Modalidade EAD'
filtro_ead = df_computacao.df['MODALIDADE'] == 'EAD'
df_computacao.mediana_iqr(categoria_ead, filtro=filtro_ead)
df_computacao.show_metrics(categoria_ead)

categoria_pres = 'Modalidade Presencial'
filtro_presencial = df_computacao.df['MODALIDADE'] == 'Presencial'
df_computacao.mediana_iqr(categoria_pres, filtro=filtro_presencial)
df_computacao.show_metrics(categoria_pres)

categoria_ate_10 = 'Presença Feminina: Até 10%'
filtro_menor_10 = df_computacao.df['PERC_MULHERES'] <= 10
df_computacao.mediana_iqr(categoria_ate_10, filtro=filtro_menor_10)
df_computacao.show_metrics(categoria_ate_10)

categoria_10_20 = 'Presença Feminina: De 10% a 20%'
filtro_10_20 = (df_computacao.df['PERC_MULHERES'] > 10) & (df_computacao.df['PERC_MULHERES'] <= 20)
df_computacao.mediana_iqr(categoria_10_20, filtro=filtro_10_20)
df_computacao.show_metrics(categoria_10_20)

categoria_mais_20 = 'Presença Feminina: Mais de 20%'
filtro_mais_20 = df_computacao.df['PERC_MULHERES'] > 20
df_computacao.mediana_iqr(categoria_mais_20, filtro=filtro_mais_20)
df_computacao.show_metrics(categoria_mais_20)

# Tabela Comparativa entre principais medidas

df_computacao.comparative_table()


# Boxplot

df_computacao.df['TIPO_INSTITUICAO'] = pd.Categorical(
    df_computacao.df['TIPO_INSTITUICAO'], 
    categories=['Pública', 'Privada'], 
    ordered=True
)

df_computacao.plot_boxplot('TIPO_INSTITUICAO', 'Comparativo da Taxa de Evasão entre instituições Públicas e Privadas', '')

df_computacao.plot_boxplot('MODALIDADE', 'Comparativo da Taxa de Evasão entre modalidades EAD e Presenciais', '')

cortes = [-1, 10, 20, 100]
nomes_categorias = ['Até 10% de Mulheres', 'De 10% a 20%', 'Mais de 20% de Mulheres']
df_computacao.df['PRESENCA_FEMININA'] = pd.cut(df_computacao.df['PERC_MULHERES'], bins=cortes, labels=nomes_categorias)
df_computacao.plot_boxplot('PRESENCA_FEMININA', 'Comparativo da Taxa de Evasão pelo Nível de Mulheres nas turmas', '')