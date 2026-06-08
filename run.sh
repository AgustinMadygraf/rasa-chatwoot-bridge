#!/bin/bash

# Función para mostrar ayuda
mostrar_ayuda() {
    echo "Uso: ./run.sh [PUERTO] [OPCIONES]"
    echo ""
    echo "Opciones:"
    echo "  --prod          Ejecutar en modo producción (desactiva auto-reload)"
    echo "  --clean         Elimina archivos .log antes de iniciar"
    echo "  -h, --help      Muestra este mensaje de ayuda"
    echo ""
    echo "Ejemplo: ./run.sh 8080 --prod"
}

# Valores por defecto
PUERTO_POR_DEFECTO=5004
MODO_RELOAD="--reload"
LIMPIAR_LOGS=false
PUERTO_ARG=""

# Procesar argumentos
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --prod) MODO_RELOAD=""; shift ;;
        --clean) LIMPIAR_LOGS=true; shift ;;
        -h|--help) mostrar_ayuda; exit 0 ;;
        [0-9]*) PUERTO_ARG=$1; shift ;;
        *) echo "Error: Argumento desconocido: $1"; mostrar_ayuda; exit 1 ;;
    esac
done

# 1. Verificar dependencias básicas
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado en el sistema."
    exit 1
fi

# Asegurar que el script se ejecute desde su propio directorio
cd "$(dirname "$0")"

# 2. Verificar y activar entorno virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Error: Entorno virtual (.venv) no encontrado. Por favor, créelo antes de continuar."
    exit 1
fi

# 3. Verificar si uvicorn está disponible en el entorno
if ! command -v uvicorn &> /dev/null; then
    echo "Error: uvicorn no encontrado. Instale las dependencias con 'pip install -r requirements.txt'."
    exit 1
fi

# 4. Determinar puerto (Prioridad: Argumento > .env > Defecto)
if [ -n "$PUERTO_ARG" ]; then
    PORT=$PUERTO_ARG
elif [ -f ".env" ]; then
    # Extraer puerto de .env ignorando comentarios y limpiando espacios/comillas
    PORT=$(grep '^PORT=' .env | sed 's/#.*//' | cut -d '=' -f2 | xargs | tr -d '"' | tr -d "'")
    # Extraer nivel de log para uvicorn
    LOG_LEVEL_ENV=$(grep '^LOG_LEVEL=' .env | sed 's/#.*//' | cut -d '=' -f2 | xargs | tr '[:upper:]' '[:lower:]')
fi

if [ -z "$PORT" ]; then
    echo "Puerto no definido, usando $PUERTO_POR_DEFECTO por defecto."
    PORT=$PUERTO_POR_DEFECTO
fi

# 5. Verificar disponibilidad del puerto
if command -v lsof &> /dev/null; then
    # Capturar PIDs y normalizarlos a una sola línea con xargs
    PID_BUSY=$(lsof -Pi :$PORT -sTCP:LISTEN -t | xargs)
    if [ -n "$PID_BUSY" ]; then
        # ps -p acepta múltiples PIDs separados por comas; sort -u elimina duplicados
        PROC_NAMES=$(ps -p ${PID_BUSY// /,} -o comm= | sort -u | xargs)
        echo "Puerto $PORT ocupado por: '$PROC_NAMES' (PID: $PID_BUSY). Liberando puerto..."
        kill -9 $PID_BUSY 2>/dev/null
    fi
fi

# Liberar procesos de ngrok residuales para evitar conflictos de túnel (ERR_NGROK_334)
if pgrep -x "ngrok" > /dev/null; then
    echo "Limpiando procesos de ngrok existentes..."
    pkill -9 -x "ngrok" 2>/dev/null
fi
sleep 1

# 6. Limpiar logs si se solicita
if [ "$LIMPIAR_LOGS" = true ]; then
    echo "Limpiando archivos de log..."
    rm -f *.log
    if [ -d "logs" ]; then
        rm -f logs/*.log
    fi
fi

# 7. Iniciar la aplicación
if [ -n "$MODO_RELOAD" ]; then
    echo "Modo: DESARROLLO (reload activado)"
else
    echo "Modo: PRODUCCIÓN"
fi

echo "Iniciando aplicación en el puerto $PORT..."

# Exportar PORT para que la configuración de Python y Ngrok la reconozcan
export PORT="$PORT"

uvicorn src.infraestructura.fastapi.app:app \
    --host 127.0.0.1 \
    --port "$PORT" \
    --log-level "${LOG_LEVEL_ENV:-info}" \
    --no-access-log \
    $MODO_RELOAD
