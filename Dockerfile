# Usa uma imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do aplicativo para o diretório de trabalho
COPY . .

# Expõe a porta 5000 para o contêiner
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["python", "rss2json.py"]