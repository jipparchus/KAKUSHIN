import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class HomeBtn extends StatelessWidget {
  const HomeBtn({super.key});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () {context.go('/main');},
      child: const Text(
        'go back',
        style: TextStyle(
          fontSize: 15,
        ),
      ),
    );
  }
}