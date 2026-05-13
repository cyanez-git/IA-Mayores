enum EventType { normal, attention, emergency, conversation }

class Event {
  final String id;
  final DateTime timestamp;
  final EventType type;
  final String title;
  final String description;

  const Event({
    required this.id,
    required this.timestamp,
    required this.type,
    required this.title,
    required this.description,
  });

  String get typeLabel {
    switch (type) {
      case EventType.normal:
        return 'Normal';
      case EventType.attention:
        return 'Atención';
      case EventType.emergency:
        return 'Emergencia';
      case EventType.conversation:
        return 'Conversación';
    }
  }
}
