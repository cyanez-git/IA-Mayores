enum AlertLevel { normal, attention, emergency }

class VitalStatus {
  final int heartRate;
  final double lastImpact;
  final bool fallDetected;
  final DateTime lastUpdate;
  final AlertLevel alertLevel;
  final String lastMessage;

  const VitalStatus({
    required this.heartRate,
    required this.lastImpact,
    required this.fallDetected,
    required this.lastUpdate,
    required this.alertLevel,
    required this.lastMessage,
  });

  String get alertLevelLabel {
    switch (alertLevel) {
      case AlertLevel.normal:
        return 'Normal';
      case AlertLevel.attention:
        return 'Atención';
      case AlertLevel.emergency:
        return 'Emergencia';
    }
  }
}
