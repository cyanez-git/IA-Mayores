import '../models/vital_status.dart';
import '../models/event.dart';

class MockData {
  static final VitalStatus currentStatus = VitalStatus(
    heartRate: 72,
    lastImpact: 0.3,
    fallDetected: false,
    lastUpdate: DateTime.now().subtract(const Duration(minutes: 2)),
    alertLevel: AlertLevel.normal,
    lastMessage: 'Buenos días Roberto, ¿cómo te sentís hoy?',
  );

  static final List<Event> todayEvents = [
    Event(
      id: '1',
      timestamp: DateTime.now().subtract(const Duration(minutes: 2)),
      type: EventType.normal,
      title: 'Saludo matutino',
      description: 'El asistente saludó a Roberto y preguntó sobre su estado.',
    ),
    Event(
      id: '2',
      timestamp: DateTime.now().subtract(const Duration(hours: 1)),
      type: EventType.conversation,
      title: 'Conversación',
      description: 'Roberto habló sobre su dolor de rodilla de ayer.',
    ),
    Event(
      id: '3',
      timestamp: DateTime.now().subtract(const Duration(hours: 2)),
      type: EventType.attention,
      title: 'FC elevada',
      description: 'Frecuencia cardíaca en 118 bpm por 3 minutos. Roberto confirmó que estaba caminando.',
    ),
    Event(
      id: '4',
      timestamp: DateTime.now().subtract(const Duration(hours: 4)),
      type: EventType.normal,
      title: 'Recordatorio medicación',
      description: 'Recordatorio de Enalapril enviado. Roberto confirmó que lo tomó.',
    ),
    Event(
      id: '5',
      timestamp: DateTime.now().subtract(const Duration(hours: 6)),
      type: EventType.conversation,
      title: 'Conversación',
      description: 'Charla sobre el partido de fútbol de anoche.',
    ),
  ];

  static const Map<String, dynamic> userProfile = {
    'name': 'Roberto',
    'age': 74,
    'condition': 'Hipertensión controlada',
    'medication': 'Enalapril 10mg',
    'familyContact': 'María (hija)',
    'familyPhone': '+54 9 11 5555-1234',
    'hrThresholdLow': 50,
    'hrThresholdHigh': 140,
  };
}
