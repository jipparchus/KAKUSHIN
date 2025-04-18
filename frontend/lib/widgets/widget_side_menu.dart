import 'package:flutter/material.dart';

class SideMenu extends StatelessWidget {
  const SideMenu({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        DrawerHeader(
          padding: const EdgeInsets.all(0),
          margin: const EdgeInsets.all(0),
          child: Container(
            color: Color.fromARGB(255, 117, 192, 151),
            alignment: Alignment.center,
            child: const Text('Gamba version 0.0.1'),
          ),
        ),
        ListTile(
          title: const Text('Climber'),
          onTap: () {
            debugPrint('Climber');
          },
        ),
        ListTile(
          title: const Text('Camera Calibration'),
          onTap: () {
            debugPrint('Camera Calibration');
          },
        ),
        ListTile(
          title: const Text('Settings'),
          onTap: () {
            debugPrint('Settings');
          },
        ),
        ListTile(
          title: const Text('About'),
          onTap: () {
            debugPrint('About');
          },
        ),
      ],
    );
  }
}