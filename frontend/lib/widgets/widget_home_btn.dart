import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

final svrresponseProvider = StateProvider<String>((ref) => 'Server response');

class HomeBtn extends ConsumerWidget {
  const HomeBtn({super.key});

  @override
  Widget build(BuildContext context,  WidgetRef ref) {
    return ElevatedButton(
      onPressed: () {
        context.go('/main');
        ref.read(svrresponseProvider.notifier).state = 'Server response';
        },
      child: const Text(
        'go back',
        style: TextStyle(
          fontSize: 15,
        ),
      ),
    );
  }
}