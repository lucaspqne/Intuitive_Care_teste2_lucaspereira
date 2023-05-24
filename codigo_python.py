import os
import requests
import pandas as pd
import tabula
from zipfile import ZipFile

# Definir URL e diretório
url = 'https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/Anexo_I_Rol_2021RN_465.2021_RN473_RN478_RN480_RN513_RN536_RN537_RN538_RN539_RN541_RN542_RN544_546_571_577.pdf'
diretorio = input("Digite o diretório onde salvar o arquivo PDF: ")

# Baixar o arquivo PDF
nome_arquivo = os.path.basename(url)
requisicao = requests.get(url)
caminho_arquivo = os.path.join(diretorio, nome_arquivo)
with open(caminho_arquivo, 'wb') as nv_arquivo:
    nv_arquivo.write(requisicao.content)

# Converter PDF para CSV
#caminho_arquivo = input("Digite o caminho onde se encontra o PDF a ser importado: ")
novo_arquivo = input("Digite o caminho onde deseja salvar o PDF convertido para CSV: ")
tabula.convert_into(caminho_arquivo, (novo_arquivo + "\\tabela_convertida.csv"), output_format="csv", pages='3-180')
print("Arquivo convertido com sucesso!\n")

# Abrir e formatar tabela
tabela = pd.read_csv((novo_arquivo + "\\tabela_convertida.csv"), encoding='iso8859-1')
########### BONUS #############
tabela.columns = ['PROCEDIMENTO', 'RN(alteração)', 'VIGÊNCIA', 'Seg. Odontológica', 'Seg. Ambulatorial', 'HCO', 'HSO', 'REF', 'PAC', 'DUT', 'SUBGRUPO', 'GRUPO', 'CAPÍTULO']
########### BONUS #############
df = pd.DataFrame(data=tabela)
df = df.fillna('')

 #cabeçalho estava sendo replicado para o corpo das informações
linhas_remover = df[df['PROCEDIMENTO'].str.contains("PROCEDIMENTO")].index
df = df.drop(linhas_remover)


# Formatar tabela e exportar para CSV
valores_substituir = [",","\r"]
tabela_formatada = df.replace((valores_substituir[0], valores_substituir[1]), " ", regex=True)
arquivo_final = input("Digite o diretório que deseja salvar a tabela formatada: ")
tabela_formatada.to_csv(arquivo_final + "\\Teste_{lucas_pereira}.csv", index=False, encoding='iso8859-1')
print("Tabela formatada e exportada com sucesso!")

# Compactar tabela como arquivo zip
diretorio_zip = input("Digite o diretório onde deseja salvar a tabela CSV como arquivo zip: ")
with ZipFile(diretorio_zip + '\\Teste_{lucas_pereira}.zip', 'w') as zip:
    zip.write(arquivo_final + '\\Teste_{lucas_pereira}.csv', 'TabelaCSV_Formatada(lucas_pereira).csv')
    print("Arquivo compactado com sucesso!")

# Excluir os arquivos gerados e deixar somente o arquivo ZIP
os.remove(novo_arquivo + "\\tabela_convertida.csv")
os.remove(arquivo_final + "\\Teste_{lucas_pereira}.csv")
os.remove(caminho_arquivo)
