# Usa a imagem oficial do Python 3.11 slim
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia o requirements.txt e instala dependências
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar o servidor Django (modo dev, escutando todas interfaces)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
