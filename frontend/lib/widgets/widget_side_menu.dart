import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/pages/page_auth.dart';

// State providers
// Authentication state
final isAuthenticatedProvider = StateProvider<bool>((ref) => false);


class SideMenu extends ConsumerWidget {
  const SideMenu({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
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
        ListTile(
          title: const Text('LogOut'),
          onTap: () {
            // Unauthenticate and send to the AuthPage.
            ref.read(isAuthenticatedProvider.notifier).state = false;
            debugPrint('Logging out...');
            if (context.mounted) {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (_) => const AuthPage(),  // App main page
                ),
              );
            }
          },
        ),
      ],
    );
  }
}