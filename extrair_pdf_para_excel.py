import pandas as pd
import re
from PyPDF2 import PdfReader

# Função para extrair as informações do PDF
def extract_data_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    data_list = []
    
    for page in reader.pages:
        text = page.extract_text()
        # Regex para capturar DATA, DESCRIÇÃO e VALOR, ignorando o ID da operação
        matches = re.findall(r'(\d{2}-\d{2}-\d{4})\s+(.+?)\s+R\$ ([\d.,-]+)', text)
        for match in matches:
            data, descricao_completa, valor = match
            # Remove o ID da operação, se presente, da descrição
            descricao = re.sub(r'\s+\d{10,}', '', descricao_completa).strip()
            valor = valor.replace('.', '').replace(',', '.').strip()
            # Ajustando o formato da data para DD/MM/AAAA
            data = data.replace('-', '/')
            data_list.append({"DATA": data, "Descrição": descricao, "Valor": float(valor)})
    
    return data_list

# Caminho para o PDF e para o arquivo Excel
pdf_path = "/mnt/data/mp-wallet_20250120144215_ae98.pdf"
excel_path = "extrato_conta_final.xlsx"

# Extração dos dados
data_extracted = extract_data_from_pdf(pdf_path)

# Criação do DataFrame
df = pd.DataFrame(data_extracted)

# Adicionando colunas fixas no final da planilha
df["Conta, Valor MercadoPago"] = "MercadoPago"  # Valor fixo
df["Categoria Valor Validar"] = "Validar"       # Valor fixo

# Salvando os dados em uma planilha Excel
df.to_excel(excel_path, index=False)

print(f"Os dados corrigidos foram extraídos e salvos em {excel_path}")
