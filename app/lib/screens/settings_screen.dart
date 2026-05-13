import 'package:flutter/material.dart';
import '../data/mock_data.dart';
import '../theme/app_theme.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late int _hrLow;
  late int _hrHigh;
  bool _pushNotifications = true;
  bool _emergencyAlerts = true;

  @override
  void initState() {
    super.initState();
    _hrLow = MockData.userProfile['hrThresholdLow'];
    _hrHigh = MockData.userProfile['hrThresholdHigh'];
  }

  @override
  Widget build(BuildContext context) {
    final profile = MockData.userProfile;

    return Scaffold(
      appBar: AppBar(title: const Text('Configuración')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _sectionTitle('Perfil del usuario'),
          Card(
            child: Column(
              children: [
                _settingRow(Icons.person_rounded, 'Nombre',
                    '${profile['name']}, ${profile['age']} años'),
                const Divider(height: 1),
                _settingRow(Icons.medical_services_rounded, 'Condición',
                    profile['condition']),
                const Divider(height: 1),
                _settingRow(Icons.medication_rounded, 'Medicación',
                    profile['medication']),
              ],
            ),
          ),
          const SizedBox(height: 20),
          _sectionTitle('Contacto familiar'),
          Card(
            child: Column(
              children: [
                _settingRow(Icons.people_rounded, 'Contacto',
                    profile['familyContact']),
                const Divider(height: 1),
                _settingRow(Icons.phone_rounded, 'Teléfono',
                    profile['familyPhone']),
              ],
            ),
          ),
          const SizedBox(height: 20),
          _sectionTitle('Umbrales de alerta'),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('FC mínima',
                          style: TextStyle(fontWeight: FontWeight.w500)),
                      Text('$_hrLow bpm',
                          style: const TextStyle(
                              color: AppTheme.primary,
                              fontWeight: FontWeight.bold)),
                    ],
                  ),
                  Slider(
                    value: _hrLow.toDouble(),
                    min: 30,
                    max: 70,
                    divisions: 40,
                    activeColor: AppTheme.primary,
                    onChanged: (v) => setState(() => _hrLow = v.round()),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('FC máxima',
                          style: TextStyle(fontWeight: FontWeight.w500)),
                      Text('$_hrHigh bpm',
                          style: const TextStyle(
                              color: AppTheme.primary,
                              fontWeight: FontWeight.bold)),
                    ],
                  ),
                  Slider(
                    value: _hrHigh.toDouble(),
                    min: 100,
                    max: 180,
                    divisions: 80,
                    activeColor: AppTheme.primary,
                    onChanged: (v) => setState(() => _hrHigh = v.round()),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          _sectionTitle('Notificaciones'),
          Card(
            child: Column(
              children: [
                SwitchListTile(
                  secondary: const Icon(Icons.notifications_rounded,
                      color: AppTheme.primary),
                  title: const Text('Notificaciones push'),
                  subtitle: const Text('Alertas en tu teléfono'),
                  value: _pushNotifications,
                  activeColor: AppTheme.primary,
                  onChanged: (v) => setState(() => _pushNotifications = v),
                ),
                const Divider(height: 1),
                SwitchListTile(
                  secondary: const Icon(Icons.warning_rounded,
                      color: AppTheme.danger),
                  title: const Text('Alertas de emergencia'),
                  subtitle: const Text('Caídas y FC crítica'),
                  value: _emergencyAlerts,
                  activeColor: AppTheme.danger,
                  onChanged: (v) => setState(() => _emergencyAlerts = v),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          ElevatedButton.icon(
            onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Cambios guardados')),
            ),
            icon: const Icon(Icons.save_rounded),
            label: const Text('Guardar cambios'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primary,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 14),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _sectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Text(title,
          style: const TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: Colors.grey,
              letterSpacing: 0.5)),
    );
  }

  Widget _settingRow(IconData icon, String label, String value) {
    return ListTile(
      leading: Icon(icon, color: AppTheme.primary, size: 20),
      title: Text(label,
          style: const TextStyle(fontSize: 13, color: Colors.grey)),
      subtitle: Text(value,
          style: const TextStyle(
              fontSize: 15, fontWeight: FontWeight.w500, color: Colors.black87)),
    );
  }
}
