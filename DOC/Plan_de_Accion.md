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
| 4 | Hub Android y Conectividad IoT | Hardware | Pendiente |
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

## FASE 4 — Hub Android y Conectividad IoT 🔲
**Objetivo:** Correr el sistema en una tablet Android real como hub central.

**Decisión de arquitectura:** La tablet Android es el hub principal del producto.
Concentra pantalla, micrófono, parlante, cámara frontal, WiFi y BT en un solo dispositivo
accesible para el usuario. Es más económica, portable y familiar que una RPi.

- [ ] Instalar Termux en la tablet (entorno Linux en Android)
- [ ] Instalar Python + dependencias en Termux
- [ ] Instalar broker MQTT (Mosquitto) en Termux
- [ ] Migrar el código de Fase 1-2 a la tablet
- [ ] Verificar que el grafo LangGraph corre correctamente
- [ ] Configurar inicio automático del sistema al encender la tablet
- [ ] Conectividad WiFi estable con el router del hogar

---

## FASE 5 — Wearable y Audio 🔲
**Objetivo:** Conectar datos reales de salud y habilitar la voz.

- [ ] Integración BLE con wearable (Bangle.js 2 o similar) vía app Android
- [ ] Recepción de FC y acelerómetro reales vía MQTT
- [ ] Pipeline de audio: micrófono de la tablet → Whisper STT → texto
- [ ] Pipeline de respuesta: texto → ElevenLabs/Azure TTS → parlante de la tablet
- [ ] Reemplazar DataSimulator por datos reales del wearable

---

## FASE 6 — Visión y Sensores mmWave 🔲
**Objetivo:** Detección de caídas y presencia sin cámara en zonas privadas.

**Nota técnica:** Los sensores mmWave usan UART. Para conectarlos a la tablet
se necesita un puente ESP32 + adaptador USB-OTG (~USD 8 adicionales).

- [ ] Configurar puente ESP32 + USB-OTG para sensores mmWave
- [ ] Integración sensor mmWave (HiLink LD2450 o Seeed MR60BHA1)
- [ ] Detección de presencia y caídas por radar
- [ ] Pipeline de cámara IP vía RTSP (TP-Link Tapo C200 o similar)
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
- [ ] Sistema de actualizaciones OTA para la tablet
- [ ] Modelo de suscripción implementado
- [ ] Pruebas de campo con usuarios reales (beta cerrada)
- [ ] Análisis de regulaciones aplicables (ANMAT en Argentina, FDA si se expande)
- [ ] Packaging y materiales de venta del kit

---

## Hardware necesario por Fase

### Para arrancar Fase 4 (mínimo indispensable)

| Componente | Especificación | Precio aprox. | Prioridad |
|------------|---------------|---------------|-----------|
| Tablet Android | 4GB+ RAM, Android 10+, WiFi + BT | Ya disponible o ~USD 100 | Alta |
| **Subtotal Fase 4** | | **~USD 0 si ya tenés una tablet** | |

> Si el cliente ya tiene una tablet compatible, el costo de entrada de la Fase 4 es cero.

### Para Fase 5 (wearable + audio)

| Componente | Especificación | Precio aprox. | Prioridad |
|------------|---------------|---------------|-----------|
| Wearable | Bangle.js 2 (open source, BLE) | USD 45 | Alta |
| **Subtotal Fase 5** | | **~USD 45** | |

> El micrófono y parlante los provee la propia tablet.

### Para Fase 6 (sensores)

| Componente | Especificación | Precio aprox. | Prioridad |
|------------|---------------|---------------|-----------|
| ESP32 + USB-OTG | Puente para sensores mmWave | USD 8 | Alta |
| Sensor mmWave | HiLink LD2450 (presencia + trayectoria) | USD 15 | Alta |
| Sensor mmWave | Seeed MR60BHA1 (FC + respiración + caídas) | USD 30 | Media |
| Cámara IP | TP-Link Tapo C200 (RTSP compatible) | USD 30 | Media |
| **Subtotal Fase 6** | | **~USD 83** | |

### Inversión total estimada para prototipo completo
**~USD 128** (sin contar tablet, que puede ser una existente).
Comparado con la alternativa RPi (~USD 257), **la tablet reduce el costo a la mitad**.

---

## Arquitectura de referencia

```
[Wearable BLE] ──────────────────────────────┐
                                              ▼
[Sensor mmWave] ──UART──► [ESP32] ──USB-OTG──► [Tablet Android]
                                              │   - Pantalla / UI
[Cámara IP] ──────────RTSP/WiFi──────────────┘   - Micrófono / Voz
                                              │   - LangGraph + Agentes
                                              ▼
                                      [Cloud / WiFi]
                                      - Claude Haiku (LLM)
                                      - Whisper (STT)
                                      - ElevenLabs (TTS)
                                      - App Familiar
```

**Principios:**
- La tablet corre offline para funciones críticas (clasificación de alertas)
- Solo usa la nube para LLM, voz y notificaciones push
- El cliente puede usar una tablet que ya tiene → baja barrera de entrada
