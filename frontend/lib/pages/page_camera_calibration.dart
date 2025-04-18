import 'package:flutter/material.dart';
import 'package:frontend/widgets/widget_side_menu.dart';

class PageCameraCalibration extends StatelessWidget {
  const PageCameraCalibration({super.key});

  @override
  Widget build(BuildContext context) {
    // Drawer
    const drawer = Drawer(
      child: SideMenu(),
    );

    // Bar to show the current page
    final appBar = AppBar(
      title: const Text('Camera Calibration'),
      backgroundColor: Color.fromARGB(255, 117, 192, 151),
    );

    return Scaffold(
      appBar: appBar,
      drawer: drawer
    );
  }
}