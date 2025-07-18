# Usa imagem Python leve
FROM python:3.11-slim

# Define diretório de trabalho no container
WORKDIR /app

# Variáveis de ambiente para evitar cache e buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências mínimas do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências do projeto
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando padrão para iniciar com Gunicorn
CMD ["gunicorn", "Anime_API.wsgi:application", "--bind", "0.0.0.0:8000"]