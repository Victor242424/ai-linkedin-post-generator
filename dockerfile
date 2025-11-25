# Usar imagen oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivo de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY linkedin_post_generator.py .

# Crear directorio para archivos generados
RUN mkdir -p /app/output

# Establecer variables de entorno por defecto
ENV GROQ_API_KEY=""
ENV PYTHONUNBUFFERED=1

# Comando por defecto
CMD ["python", "linkedin_post_generator.py"]
