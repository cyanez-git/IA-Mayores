import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../data/mock_data.dart';
import '../models/event.dart';
import '../widgets/event_tile.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final events = MockData.todayEvents;
    final byType = {
      EventType.emergency: events.where((e) => e.type == EventType.emergency).length,
      EventType.attention: events.where((e) => e.type == EventType.attention).length,
      EventType.conversation: events.where((e) => e.type == EventType.conversation).length,
      EventType.normal: events.where((e) => e.type == EventType.normal).length,
    };

    return Scaffold(
      appBar: AppBar(
        title: Text('Historial — ${DateFormat('d MMM', 'es').format(DateTime.now())}'),
      ),
      body: Column(
        children: [
          _buildSummary(byType),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.only(top: 8, bottom: 16),
              itemCount: events.length,
              itemBuilder: (_, i) => EventTile(event: events[i]),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSummary(Map<EventType, int> byType) {
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.symmetric(vertical: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _summaryChip('Emergencias', byType[EventType.emergency]!, Colors.red),
          _summaryChip('Atenciones', byType[EventType.attention]!, Colors.orange),
          _summaryChip('Charlas', byType[EventType.conversation]!, Colors.blue),
          _summaryChip('Normales', byType[EventType.normal]!, Colors.green),
        ],
      ),
    );
  }

  Widget _summaryChip(String label, int count, Color color) {
    return Column(
      children: [
        Text('$count',
            style: TextStyle(
                fontSize: 22, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
      ],
    );
  }
}
