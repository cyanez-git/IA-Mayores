import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/event.dart';
import '../theme/app_theme.dart';

class EventTile extends StatelessWidget {
  final Event event;

  const EventTile({super.key, required this.event});

  Color get _typeColor {
    switch (event.type) {
      case EventType.emergency:
        return AppTheme.danger;
      case EventType.attention:
        return AppTheme.warning;
      case EventType.conversation:
        return AppTheme.primary;
      case EventType.normal:
        return AppTheme.success;
    }
  }

  IconData get _typeIcon {
    switch (event.type) {
      case EventType.emergency:
        return Icons.warning_rounded;
      case EventType.attention:
        return Icons.info_rounded;
      case EventType.conversation:
        return Icons.chat_bubble_rounded;
      case EventType.normal:
        return Icons.check_circle_rounded;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: _typeColor.withOpacity(0.15),
          child: Icon(_typeIcon, color: _typeColor, size: 20),
        ),
        title: Text(event.title,
            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14)),
        subtitle: Text(event.description,
            style: const TextStyle(fontSize: 13), maxLines: 2),
        trailing: Text(
          DateFormat('HH:mm').format(event.timestamp),
          style: const TextStyle(fontSize: 12, color: Colors.grey),
        ),
      ),
    );
  }
}
