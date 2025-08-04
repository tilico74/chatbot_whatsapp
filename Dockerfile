# Usa imagem Python oficial
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando de inicialização do app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
