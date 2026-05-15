#!/bin/bash
# Setup SAMP en Mini PC — Ubuntu 24.04 LTS
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[SAMP]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

PROJECT_DIR="$HOME/IA-Mayores"
VENV_DIR="$PROJECT_DIR/.venv"
SERVICE_NAME="samp"

# ─── 1. Sistema base ────────────────────────────────────────────────────────
log "Actualizando sistema..."
sudo apt-get update -qq && sudo apt-get upgrade -y -qq

log "Instalando dependencias del sistema..."
sudo apt-get install -y -qq \
    python3.11 python3.11-venv python3.11-dev \
    python3-pip git curl wget \
    portaudio19-dev libsndfile1 ffmpeg \
    bluetooth bluez bluez-tools \
    build-essential libssl-dev libffi-dev

# ─── 2. Python + dependencias del proyecto ──────────────────────────────────
log "Creando entorno virtual Python..."
python3.11 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

log "Instalando dependencias Python..."
pip install --upgrade pip -q
pip install -r "$PROJECT_DIR/requirements.txt" -q

log "Instalando dependencias de audio (Whisper + Piper)..."
pip install openai-whisper -q
pip install piper-tts -q

# ─── 3. Mosquitto MQTT ──────────────────────────────────────────────────────
log "Instalando Mosquitto MQTT broker..."
sudo apt-get install -y -qq mosquitto mosquitto-clients

sudo tee /etc/mosquitto/conf.d/samp.conf > /dev/null <<EOF
listener 1883 localhost
allow_anonymous true
EOF

sudo systemctl enable mosquitto
sudo systemctl start mosquitto
log "Mosquitto activo en puerto 1883"

# ─── 4. Ollama + modelo LLM ─────────────────────────────────────────────────
log "Instalando Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

sudo systemctl enable ollama
sudo systemctl start ollama
sleep 3

# Phi-3 mini: ~2.3GB RAM en Q4 — ideal para 8GB
log "Descargando modelo Phi-3 mini (puede tardar varios minutos)..."
ollama pull phi3:mini

log "Modelo descargado. Verificando..."
ollama list

# ─── 5. Servicio systemd ────────────────────────────────────────────────────
log "Configurando servicio systemd..."
sudo cp "$PROJECT_DIR/scripts/samp.service" /etc/systemd/system/
sudo sed -i "s|__USER__|$USER|g" /etc/systemd/system/samp.service
sudo sed -i "s|__PROJECT_DIR__|$PROJECT_DIR|g" /etc/systemd/system/samp.service
sudo sed -i "s|__VENV_DIR__|$VENV_DIR|g" /etc/systemd/system/samp.service

sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"

log "────────────────────────────────────────────"
log "Instalación completa."
log "Para iniciar SAMP: sudo systemctl start samp"
log "Para ver logs:     journalctl -u samp -f"
log "────────────────────────────────────────────"
