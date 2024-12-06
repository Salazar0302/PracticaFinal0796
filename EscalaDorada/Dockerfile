# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de dependencias (requirements.txt)
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto en el que la aplicación escucha
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]
