import 'package:flutter/material.dart';
import '../data/mock_data.dart';
import '../theme/app_theme.dart';

class VideocallScreen extends StatefulWidget {
  const VideocallScreen({super.key});

  @override
  State<VideocallScreen> createState() => _VideocallScreenState();
}

class _VideocallScreenState extends State<VideocallScreen> {
  bool _inCall = false;

  @override
  Widget build(BuildContext context) {
    final profile = MockData.userProfile;

    return Scaffold(
      appBar: AppBar(title: const Text('Videollamada')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircleAvatar(
                radius: 60,
                backgroundColor: AppTheme.primary.withOpacity(0.1),
                child: Text(
                  (profile['name'] as String)[0],
                  style: const TextStyle(
                      fontSize: 48,
                      fontWeight: FontWeight.bold,
                      color: AppTheme.primary),
                ),
              ),
              const SizedBox(height: 20),
              Text(profile['name'],
                  style: const TextStyle(
                      fontSize: 28, fontWeight: FontWeight.bold)),
              Text('${profile['age']} años',
                  style: const TextStyle(fontSize: 16, color: Colors.grey)),
              const SizedBox(height: 40),
              if (_inCall)
                _buildInCallUI()
              else
                _buildCallButton(),
              const SizedBox(height: 32),
              _buildContactInfo(profile),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCallButton() {
    return Column(
      children: [
        ElevatedButton.icon(
          onPressed: () => setState(() => _inCall = true),
          icon: const Icon(Icons.videocam_rounded),
          label: const Text('Iniciar videollamada'),
          style: ElevatedButton.styleFrom(
            backgroundColor: AppTheme.success,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(30)),
          ),
        ),
        const SizedBox(height: 12),
        OutlinedButton.icon(
          onPressed: () {},
          icon: const Icon(Icons.call_rounded),
          label: const Text('Solo audio'),
          style: OutlinedButton.styleFrom(
            padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
            shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(30)),
          ),
        ),
      ],
    );
  }

  Widget _buildInCallUI() {
    return Column(
      children: [
        const Text('Llamando...',
            style: TextStyle(fontSize: 16, color: Colors.grey)),
        const SizedBox(height: 20),
        FloatingActionButton(
          onPressed: () => setState(() => _inCall = false),
          backgroundColor: AppTheme.danger,
          child: const Icon(Icons.call_end_rounded, color: Colors.white),
        ),
      ],
    );
  }

  Widget _buildContactInfo(Map<String, dynamic> profile) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text('Contacto de emergencia',
                style: TextStyle(fontWeight: FontWeight.w600, color: Colors.grey)),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.person_rounded, size: 16, color: AppTheme.primary),
                const SizedBox(width: 6),
                Text(profile['familyContact'],
                    style: const TextStyle(fontWeight: FontWeight.w500)),
                const SizedBox(width: 12),
                const Icon(Icons.phone_rounded, size: 16, color: AppTheme.primary),
                const SizedBox(width: 6),
                Text(profile['familyPhone']),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
