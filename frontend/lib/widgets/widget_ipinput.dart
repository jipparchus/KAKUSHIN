import 'package:flutter/material.dart';

class IpInputWidget extends StatelessWidget {
  final Function(String) onIpChanged;

  const IpInputWidget({required this.onIpChanged, super.key});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: TextField(
        decoration: const InputDecoration(
        labelText: 'Server IP (e.g. 127.0.0.1)',
        border: OutlineInputBorder(),
      ),
      keyboardType: TextInputType.number,
      onChanged: onIpChanged,
    ),
    );
  }
}
