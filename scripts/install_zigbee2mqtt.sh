#!/bin/bash
# Instalación de Zigbee2MQTT en la Mini PC para usar con Sonoff ZBDongle-E (EFR32MG21)
# Pre-requisitos: Node.js 20+, Mosquitto MQTT, dongle USB conectado.

set -e

Z2M_DIR="/opt/zigbee2mqtt"
USER_NAME="${SUDO_USER:-$USER}"

echo "==> Verificando pre-requisitos..."
command -v node >/dev/null || { echo "Falta Node.js — instalalo primero"; exit 1; }
command -v npm >/dev/null  || { echo "Falta npm";   exit 1; }
systemctl is-active --quiet mosquitto || { echo "Falta Mosquitto activo"; exit 1; }

echo "==> Verificando dongle Sonoff..."
DONGLE_PATH=$(ls /dev/serial/by-id/ 2>/dev/null | grep -i "sonoff.*zigbee" | head -1)
if [ -z "$DONGLE_PATH" ]; then
    echo "WARN: no se detecta el dongle Sonoff. Conectalo y volvé a correr el script."
    echo "Listando dispositivos seriales:"
    ls /dev/serial/by-id/ 2>/dev/null || echo "  (ninguno)"
    exit 1
fi
DONGLE_FULL="/dev/serial/by-id/$DONGLE_PATH"
echo "    Dongle: $DONGLE_FULL"

echo "==> Agregando $USER_NAME al grupo dialout (acceso serial)..."
sudo usermod -aG dialout "$USER_NAME"

echo "==> Clonando Zigbee2MQTT..."
sudo mkdir -p "$Z2M_DIR"
sudo chown -R "$USER_NAME":"$USER_NAME" "$Z2M_DIR"
if [ ! -d "$Z2M_DIR/.git" ]; then
    git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git "$Z2M_DIR"
else
    echo "    Ya existe, actualizando..."
    cd "$Z2M_DIR" && git pull
fi

echo "==> Instalando dependencias npm (puede tardar 5-10 min)..."
cd "$Z2M_DIR"
npm ci

echo "==> Generando configuración para ZBDongle-E..."
mkdir -p "$Z2M_DIR/data"
cat > "$Z2M_DIR/data/configuration.yaml" <<EOF
version: 4
homeassistant:
  enabled: false
mqtt:
  base_topic: zigbee2mqtt
  server: mqtt://localhost:1883
serial:
  port: $DONGLE_FULL
  adapter: ember
advanced:
  log_level: info
  channel: 15
frontend:
  enabled: true
  host: 0.0.0.0
  port: 8080
permit_join: false
EOF
echo "    Config en $Z2M_DIR/data/configuration.yaml"

echo "==> Creando servicio systemd..."
sudo tee /etc/systemd/system/zigbee2mqtt.service > /dev/null <<EOF
[Unit]
Description=Zigbee2MQTT
After=network.target mosquitto.service

[Service]
ExecStart=/usr/bin/npm start
WorkingDirectory=$Z2M_DIR
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$USER_NAME

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable zigbee2mqtt
sudo systemctl start zigbee2mqtt

echo ""
echo "==> Instalación lista."
echo "    Frontend Z2M:    http://$(hostname -I | awk '{print $1}'):8080"
echo "    Logs:            sudo journalctl -u zigbee2mqtt -f"
echo ""
echo "Próximo paso:"
echo "  1. Abrí el frontend en cualquier navegador de la LAN"
echo "  2. Tocá 'Permit join (All)' arriba a la derecha"
echo "  3. Reseteá un sensor ZY-M100 (botón 5s) — se va a auto-detectar"
echo "  4. Renombralo (ej: mmwave_living) en la pestaña del dispositivo"
