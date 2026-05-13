import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../data/mock_data.dart';
import '../models/vital_status.dart';
import '../theme/app_theme.dart';
import '../widgets/status_card.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final status = MockData.currentStatus;
    final profile = MockData.userProfile;
    final alertColor = AppTheme.alertColor(status.alertLevel);

    return Scaffold(
      appBar: AppBar(
        title: const Text('SAMP — Familia'),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16),
            child: CircleAvatar(
              backgroundColor: alertColor,
              radius: 10,
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildStatusBanner(status, alertColor),
            const SizedBox(height: 20),
            Text('Signos vitales',
                style: Theme.of(context)
                    .textTheme
                    .titleMedium
                    ?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            StatusCard(
              title: 'Frecuencia cardíaca',
              value: '${status.heartRate} bpm',
              subtitle: 'Normal: 50–140 bpm',
              icon: Icons.favorite_rounded,
              color: status.heartRate > 100 ? AppTheme.warning : AppTheme.success,
            ),
            const SizedBox(height: 8),
            StatusCard(
              title: 'Última actualización',
              value: DateFormat('HH:mm').format(status.lastUpdate),
              subtitle: 'hace ${DateTime.now().difference(status.lastUpdate).inMinutes} min',
              icon: Icons.access_time_rounded,
              color: AppTheme.primary,
            ),
            const SizedBox(height: 20),
            Text('Último mensaje del asistente',
                style: Theme.of(context)
                    .textTheme
                    .titleMedium
                    ?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Icon(Icons.smart_toy_rounded,
                        color: AppTheme.primary, size: 24),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(status.lastMessage,
                          style: const TextStyle(fontSize: 15)),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            Text('Perfil',
                style: Theme.of(context)
                    .textTheme
                    .titleMedium
                    ?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    _profileRow(Icons.person_rounded, 'Nombre',
                        '${profile['name']}, ${profile['age']} años'),
                    const Divider(height: 20),
                    _profileRow(Icons.medical_services_rounded, 'Condición',
                        profile['condition']),
                    const Divider(height: 20),
                    _profileRow(Icons.medication_rounded, 'Medicación',
                        profile['medication']),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusBanner(VitalStatus status, Color color) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: color.withOpacity(0.4)),
      ),
      child: Row(
        children: [
          Icon(
            status.alertLevel == AlertLevel.normal
                ? Icons.check_circle_rounded
                : Icons.warning_rounded,
            color: color,
            size: 32,
          ),
          const SizedBox(width: 12),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Estado: ${status.alertLevelLabel}',
                  style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: color)),
              Text('Roberto está bien',
                  style: TextStyle(color: color.withOpacity(0.8))),
            ],
          ),
        ],
      ),
    );
  }

  Widget _profileRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, size: 18, color: AppTheme.primary),
        const SizedBox(width: 10),
        Text('$label: ',
            style: const TextStyle(
                fontWeight: FontWeight.w600, color: Colors.grey)),
        Expanded(child: Text(value, style: const TextStyle(fontSize: 14))),
      ],
    );
  }
}
