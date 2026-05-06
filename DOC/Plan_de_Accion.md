# SAMP — Plan de Acción Completo
**Sistema de Acompañamiento y Monitoreo Proactivo**
Última actualización: 2026-05-06

---

## Resumen de Fases

| Fase | Nombre | Tipo | Estado |
|------|--------|------|--------|
| 0 | Diseño y Arquitectura | Software | Completo |
| 1 | Simulación y Agentes | Software | Completo |
| 2 | Conversación y Memoria | Software | Pendiente |
| 3 | Tests y Calidad | Software | Pendiente |
| 4 | Hub y Conectividad IoT | Hardware | Pendiente |
| 5 | Wearable y Audio | Hardware | Pendiente |
| 6 | Visión y Sensores mmWave | Hardware | Pendiente |
| 7 | App Familiar | Software | Pendiente |
| 8 | Producto y Despliegue | Infraestructura | Pendiente |

---

## FASE 0 — Diseño y Arquitectura ✅
**Objetivo:** Definir qué se construye y cómo.

- [x] Documento de diseño del sistema (Proyecto.docx)
- [x] Stack tecnológico definido
- [x] Arquitectura de tres agentes definida
- [x] Modelo de negocio B2C / B2B identificado
- [x] Segmentos de mercado: adultos mayores + hipocondría/pánico
- [x] Repositorio GitHub creado

---

## FASE 1 — Simulación y Agentes ✅
**Objetivo:** Demostrar que la lógica de agentes funciona sin hardware.

- [x] DataSimulator: genera datos de wearable (FC + acelerómetro)
- [x] AlertRouter: clasifica lecturas en normal / attention / emergency
- [x] EmpathyAgent: responde según perfil (adulto mayor / pánico)
- [x] TriageAgent: genera mensaje al usuario + relato para familiar
- [x] Grafo LangGraph que orquesta los tres agentes
- [x] Demo funcional con Claude Haiku

---

## FASE 2 — Conversación y Memoria 🔲
**Objetivo:** Que el asistente pueda mantener una charla real y recuerde al usuario.

- [ ] Loop de conversación interactiva por consola
- [ ] Historial de mensajes en la sesión (memoria corta)
- [ ] Base de datos vectorial para memoria larga (ChromaDB o similar)
- [ ] RAG: el agente recuerda preferencias, historias, nombre del usuario
- [ ] Perfil de usuario configurable (nombre, condición, contacto familiar)

---

## FASE 3 — Tests y Calidad 🔲
**Objetivo:** Garantizar que el sistema clasifica correctamente antes de conectar hardware real.

- [ ] Tests unitarios del AlertRouter (casos límite de FC, g de impacto)
- [ ] Tests de integración del grafo completo
- [ ] Validación de umbrales con datos reales de literatura médica
- [ ] Ajuste fino de prompts de los agentes

---

## FASE 4 — Hub y Conectividad IoT 🔲
**Objetivo:** Levantar el cerebro del sistema en hardware real.

**Hardware necesario (ver sección HW más abajo)**

- [ ] Configurar Raspberry Pi 5 con Linux (Raspberry Pi OS)
- [ ] Instalar dependencias Python en la RPi
- [ ] Instalar broker MQTT (Mosquitto)
- [ ] Migrar el código de Fase 1-2 a la RPi
- [ ] Verificar que el grafo LangGraph corre en la RPi
- [ ] Conectividad WiFi estable

---

## FASE 5 — Wearable y Audio 🔲
**Objetivo:** Conectar datos reales de salud y habilitar la voz.

- [ ] Integración BLE con wearable (Bangle.js 2 o similar)
- [ ] Recepción de FC y acelerómetro reales vía MQTT
- [ ] Pipeline de audio: captura de voz → Whisper STT → texto
- [ ] Pipeline de respuesta: texto → ElevenLabs/Azure TTS → audio
- [ ] Reemplazar DataSimulator por datos reales del wearable

---

## FASE 6 — Visión y Sensores mmWave 🔲
**Objetivo:** Detección de caídas y presencia sin cámara en zonas privadas.

- [ ] Integración sensor mmWave (HiLink LD2450 o Seeed MR60BHA1)
- [ ] Detección de presencia y caídas por radar
- [ ] Pipeline de cámara RTSP (TP-Link Tapo C200 o similar)
- [ ] MediaPipe sobre feed de cámara: postura "de pie" vs "en el suelo"
- [ ] Fusión de sensores: confirmar caída solo si mmWave + cámara coinciden

---

## FASE 7 — App Familiar 🔲
**Objetivo:** Interfaz para que la familia monitoree y reciba alertas.

- [ ] Definir plataforma: Flutter (iOS + Android) o React Native
- [ ] Pantalla de estado en tiempo real (FC, última actividad)
- [ ] Sistema de notificaciones push para alertas
- [ ] Historial de eventos del día
- [ ] Módulo de videollamada integrado
- [ ] Panel de configuración (umbrales, contactos, perfil del usuario)

---

## FASE 8 — Producto y Despliegue 🔲
**Objetivo:** Convertir el prototipo en un producto comercializable.

- [ ] Infraestructura cloud (AWS / GCP) para la capa de agentes
- [ ] Sistema de actualizaciones OTA para el hub
- [ ] Modelo de suscripción implementado
- [ ] Pruebas de campo con usuarios reales (beta cerrada)
- [ ] Análisis de regulaciones aplicables (ANMAT en Argentina, FDA si se expande)
- [ ] Packaging y materiales de venta del kit

---

## Hardware necesario por Fase

### Para arrancar Fase 4 (mínimo indispensable)

| Componente | Especificación | Precio aprox. | Prioridad |
|------------|---------------|---------------|-----------|
| Raspberry Pi 5 | 8GB RAM | USD 80 | Alta |
| Fuente de alimentación | USB-C 5A oficial | USD 12 | Alta |
| Cooler / disipador | Activo para RPi 5 | USD 8 | Alta |
| MicroSD | 64GB Clase 10 (Samsung/SanDisk) | USD 12 | Alta |
| **Subtotal Fase 4** | | **~USD 112** | |

### Para Fase 5 (wearable + audio)

| Componente | Especificación | Precio aprox. | Prioridad |
|------------|---------------|---------------|-----------|
| Wearable | Bangle.js 2 (open source, BLE) | USD 45 | Alta |
| Micrófono USB | Cualquier micrófono USB compacto | USD 15 | Alta |
| Parlante | USB o Jack 3.5mm | USD 10 | Media |
| **Subtotal Fase 5** | | **~USD 70** | |

### Para Fase 6 (sensores)

| Componente | Especificación | Precio aprox. | Prioridad |
|------------|---------------|---------------|-----------|
| Sensor mmWave | HiLink LD2450 (presencia + trayectoria) | USD 15 | Alta |
| Sensor mmWave | Seeed MR60BHA1 (FC + respiración + caídas) | USD 30 | Media |
| Cámara IP | TP-Link Tapo C200 (RTSP compatible) | USD 30 | Media |
| **Subtotal Fase 6** | | **~USD 75** | |

### Inversión total estimada para prototipo completo
**~USD 257** sin contar tablet ni PC de desarrollo (que ya tenés).

---

## Notas de arquitectura

- El hub (RPi 5) puede reemplazarse por una tablet Android de 4GB+ RAM en versión comercial
- Los sensores mmWave se conectan a la RPi por UART; para tablet se necesita puente ESP32
- La arquitectura está diseñada para funcionar 100% offline en caso de caída de internet,
  escalando a la nube solo para LLM y notificaciones push
