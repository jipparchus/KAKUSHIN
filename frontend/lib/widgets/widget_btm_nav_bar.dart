import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
// Page index
final indexProvider = StateProvider((ref) {
  return 0;
});


class BtmNavBar extends ConsumerWidget {
  const BtmNavBar({super.key});

@override
  Widget build(BuildContext context, WidgetRef ref) {
    // Index watched
    final index = ref.watch(indexProvider);
    
    return BottomNavigationBar(
  items: [
    BottomNavigationBarItem(
      icon: Icon(Icons.build),
      label: 'Trim & Holding',
    ),
    BottomNavigationBarItem(
      icon: Icon(Icons.crop),
      label: 'Wall',
    ),
    BottomNavigationBarItem(
      icon: Icon(Icons.polyline),
      label: 'Key Points',
    ),
    BottomNavigationBarItem(
      icon: Icon(Icons.view_in_ar),
      label: '3D Animation',
    ),
    BottomNavigationBarItem(
      icon: Icon(Icons.insights),
      label: 'Analysis',
    ),
  ],
  backgroundColor: const Color.fromARGB(255, 117, 192, 151),
  selectedItemColor: Colors.black,
  unselectedItemColor: const Color.fromARGB(255, 189, 186, 186),
  currentIndex: index,
  onTap: (index) {
    // Change index
    ref.read(indexProvider.notifier).state = index;
  },
  );
  }
}

