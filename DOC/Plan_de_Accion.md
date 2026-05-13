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

## FASE 4 — Mini PC Hub y Conectividad IoT 🔲
**Objetivo:** Correr el sistema en una Mini PC Linux como hub central on-premise.

**Decisión de arquitectura:** La Mini PC es el hub definitivo del producto.
Corre Linux real sin restricciones de Android, permite LLM local, procesos 24/7
sin interrupciones, y Python/LangGraph nativos sin adaptaciones.
No tiene pantalla — la interacción con el usuario es 100% por voz.

- [ ] Instalar Linux en la Mini PC (Ubuntu 24.04 LTS recomendado)
- [ ] Instalar Python + dependencias del proyecto
- [ ] Instalar broker MQTT (Mosquitto)
- [ ] Instalar Ollama + modelo LLM local (Phi-3 mini o Llama 3.2 3B)
- [ ] Migrar el código de Fase 1-2 a la Mini PC
- [ ] Configurar inicio automático del sistema como servicio (systemd)
- [ ] Verificar que el grafo LangGraph corre correctamente

**Hardware Fase 4:**
| Componente | Especificación | Precio aprox. |
|-----------|---------------|---------------|
| Mini PC | Intel i7, 16GB RAM, 256GB SSD | USD 250-300 |
| **Subtotal** | | **~USD 170** |

---

## FASE 5 — Wearable y Audio 🔲
**Objetivo:** Conectar datos reales de salud y habilitar la voz.

- [ ] Integración BLE con wearable (Bangle.js 2 o similar) vía bluetoothctl/Linux
- [ ] Recepción de FC y acelerómetro reales vía MQTT
- [ ] Pipeline STT: array mic USB → Whisper local → texto
- [ ] Pipeline TTS: texto → Piper TTS local → parlante USB
- [ ] Reemplazar DataSimulator por datos reales del wearable

**Hardware Fase 5:**
| Componente | Especificación | Precio aprox. |
|-----------|---------------|---------------|
| Wearable | Bangle.js 2 (open source, BLE) | USD 45 |
| Micrófono | ReSpeaker USB Array (campo lejano, cancelación de ruido) | USD 30 |
| Parlante | USB compacto | USD 15 |
| **Subtotal** | | **~USD 90** |

---

## FASE 6 — Visión y Sensores mmWave 🔲
**Objetivo:** Detección de caídas y presencia sin cámara en zonas privadas.

**Nota técnica:** Se usan sensores mmWave con WiFi integrado. Se conectan
directamente al router del hogar y publican datos vía MQTT. Sin cables ni intermediarios.

- [ ] Integración sensor mmWave con WiFi (HiLink LD2410C o Seeed MR60BHA1)
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

- [ ] Backend cloud mínimo para notificaciones push (Firebase)
- [ ] Sistema de actualizaciones OTA para la Mini PC (SSH / script)
- [ ] Modelo de suscripción implementado
- [ ] Pruebas de campo con usuarios reales (beta cerrada)
- [ ] Análisis de regulaciones aplicables (ANMAT en Argentina, FDA si se expande)
- [ ] Packaging y materiales de venta del kit

---

## Resumen de Hardware por Fase

| Fase | Componente | Precio aprox. |
|------|-----------|---------------|
| 4 | Mini PC (Intel i7, 16GB RAM, 256GB SSD) | USD 275 |
| 5 | Wearable Bangle.js 2 | USD 45 |
| 5 | ReSpeaker USB Array mic | USD 30 |
| 5 | Parlante USB | USD 15 |
| 6 | Sensor mmWave WiFi (HiLink LD2410C) | USD 15 |
| 6 | Sensor mmWave WiFi (Seeed MR60BHA1) | USD 30 |
| 6 | Cámara IP RTSP (TP-Link Tapo C200) | USD 30 |
| **Total** | | **~USD 335** |

> El prototipo puede arrancarse solo con la Mini PC (~USD 275) y añadir componentes fase a fase.

---

## Arquitectura de referencia

```
[Wearable BLE]       ──BT──────────────────────────────► [Mini PC Linux]
[Sensor mmWave WiFi] ──WiFi──► [Router] ──WiFi─────────► [Mini PC Linux]
[Cámara IP RTSP]     ──WiFi──► [Router] ──WiFi─────────► [Mini PC Linux]
[Micrófono USB]      ──USB──────────────────────────────► [Mini PC Linux]
[Parlante USB]       ◄──USB─────────────────────────────  [Mini PC Linux]
                                                               │
                                                    100% ON-PREMISE
                                                    - LangGraph + Agentes
                                                    - Ollama (LLM local)
                                                    - Whisper STT (local)
                                                    - Piper TTS (local)
                                                    - MQTT Broker
                                                    - MediaPipe
                                                               │
                                                    Solo notificaciones:
                                                    [App Familiar - cloud]
```

**Principios:**
- Todo corre on-premise — funciona aunque se caiga internet
- La nube solo recibe notificaciones push en caso de emergencia
- Sin pantalla — interacción 100% por voz
- Dispositivo oculto, el usuario no necesita interactuar con él
