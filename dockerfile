FROM python:3.12-slim

# Instalar dependências do sistema para PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root para segurança
RUN groupadd -r todoapp && useradd -r -g todoapp todoapp

# Set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt requirements.txt
COPY otel.py otel.py
COPY todo_app.py todo_app.py

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Criar diretório para dados temporários e ajustar permissões
RUN mkdir -p /app/data && chown -R todoapp:todoapp /app

# Mudar para usuário não-root
USER todoapp

ENV SETUP=docker

# Expor porta da aplicação
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run todo_app.py when the container launches
ENTRYPOINT ["python", "todo_app.py"]
