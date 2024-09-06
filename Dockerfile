# Use uma imagem oficial do Python como base
FROM python:3.12

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Copie o arquivo requirements.txt para o container
COPY requirements.txt /app/

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do projeto para o container
COPY . /app/

# Exponha a porta onde o Django vai rodar (por padrão, 8000)
EXPOSE 8000

# Comando para rodar o servidor de desenvolvimento do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
