import 'package:flutter/material.dart';
import 'package:frontend/widgets/widget_home_btn.dart';
import 'package:frontend/widgets/widget_side_menu.dart';

class PageAbout extends StatelessWidget {
  const PageAbout({super.key});

  @override
  Widget build(BuildContext context) {
    // Drawer
    const drawer = Drawer(
      child: SideMenu(),
    );

    // Bar to show the current page
    final appBar = AppBar(
      title: const Text('About'),
      backgroundColor: Color.fromARGB(255, 117, 192, 151),
    );

    return Scaffold(
      appBar: appBar,
      drawer: drawer,
      body:
        Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('About'),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                HomeBtn(),
              ],
            )
          ],
        )
    );
  }
}