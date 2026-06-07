#!/bin/bash

# Verificar si el entorno virtual existe y activarlo
if [ -d ".venv" ]; then
    echo "Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "Entorno virtual no encontrado. Asegúrese de haberlo creado."
fi

# Cargar el puerto desde el archivo .env
if [ -f ".env" ]; then
    # Lee el valor de PORT del archivo .env
    PORT=$(grep '^PORT=' .env | cut -d '=' -f2)
    
    # Si no se encuentra el puerto, usa 8000 por defecto
    if [ -z "$PORT" ]; then
        echo "Puerto no definido en .env, usando 5004 por defecto."
        PORT=5004
    fi
else
    echo "Archivo .env no encontrado, usando 5004 por defecto."
    PORT=5004
fi

echo "Iniciando aplicación en el puerto $PORT..."
uvicorn src.infraestructura.fastapi.app:app --host 127.0.0.1 --port $PORT --reload
