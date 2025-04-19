import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/routes/router.dart';

// AuthN state
final isAuthenticatedProvider = StateProvider<bool>((ref) => false);

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: appRouter,
      debugShowCheckedModeBanner: false,
    );
  }
}









// void main() {
//   runApp(
//     const ProviderScope(
//       child: RootApp(),
//     ),
//   );
// }


// class RootApp extends ConsumerWidget {
//   const RootApp({super.key});

//   @override
//   Widget build(BuildContext context, WidgetRef ref) {
//     final isAuthenticated = ref.watch(isAuthenticatedProvider);

//     return MaterialApp(
//       home: isAuthenticated ? const MyApp() : const AuthPage(),
//     );
//   }
// }



















// // After Authenticated
// class MyApp extends ConsumerWidget {
//   const MyApp({super.key});

//   @override
//   Widget build(BuildContext context, WidgetRef ref) {
//     // If authenticated
//     // final isAuthenticated = ref.watch(isAuthenticatedProvider);
//     // Index watched
//     final index = ref.watch(indexProvider);
//     // Items
//     const items = [
//       BottomNavigationBarItem(
//         icon: Icon(Icons.build),
//         label: 'Trim & Holding',
//       ),
//       BottomNavigationBarItem(
//         icon: Icon(Icons.crop),
//         label: 'Wall',
//       ),
//       BottomNavigationBarItem(
//         icon: Icon(Icons.polyline),
//         label: 'Key Points',
//       ),
//       BottomNavigationBarItem(
//         icon: Icon(Icons.view_in_ar),
//         label: '3D Animation',
//       ),
//       BottomNavigationBarItem(
//         icon: Icon(Icons.insights),
//         label: 'Analysis',
//       ),
//     ];

//     final bar = BottomNavigationBar(
//       items: items,
//       backgroundColor: const Color.fromARGB(255, 117, 192, 151),
//       selectedItemColor: Colors.black,
//       unselectedItemColor: const Color.fromARGB(255, 189, 186, 186),
//       currentIndex: index,
//       onTap: (index) {
//         // Change index
//         ref.read(indexProvider.notifier).state = index;
//       },
//     );

//     const pages = [
//       PageA(),
//       PageB(),
//       PageC(),
//       PageD(),
//       PageE(),
//     ];

//     // Drawer
//     const drawer = Drawer(
//       child: SideMenu(),
//     );

//     return Scaffold(
//       drawer: drawer,
//       body: pages[index],
//       bottomNavigationBar: bar,
//     );
//   }
// }
