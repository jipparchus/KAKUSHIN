
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/pages/page_a.dart';
import 'package:frontend/pages/page_b.dart';
import 'package:frontend/pages/page_c.dart';
import 'package:frontend/pages/page_d.dart';
import 'package:frontend/pages/page_e.dart';
import 'package:frontend/providers/nav_provider.dart';
import 'package:frontend/widgets/widget_btm_nav_bar.dart';
import 'package:frontend/widgets/widget_side_menu.dart';

// Page index
// final indexProvider = StateProvider((ref) {
//   return 0;
// });
// final indexProvider = StateProvider<int>((ref) => 0);

// After Authenticated
class PageMain extends ConsumerWidget {
  const PageMain({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Index watched
    final index = ref.watch(indexProvider);

    const pages = [
      PageA(),
      PageB(),
      PageC(),
      PageD(),
      PageE(),
    ];

    return Scaffold(
      drawer: Drawer(
        child: SideMenu(),
      ),
      body: pages[index],
      bottomNavigationBar: BtmNavBar()
    );
  }
}
