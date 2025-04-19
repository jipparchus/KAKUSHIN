import 'package:frontend/pages/page_about.dart';
import 'package:frontend/pages/page_auth.dart';
import 'package:frontend/pages/page_camera_calibration.dart';
import 'package:frontend/pages/page_climber.dart';
import 'package:frontend/pages/page_main.dart';
import 'package:frontend/pages/page_settings.dart';
import 'package:go_router/go_router.dart';

// go_router setting
final appRouter = GoRouter(
  // initial path
  initialLocation: '/auth', // Always show AuthPage first
  routes:[
    GoRoute(
      path: '/auth',
      builder: (context, state) => AuthPage(),
    ),
    GoRoute(
      path: '/main',
      builder: (context, state) => PageMain(),
    ),
    GoRoute(
      path: '/climber',
      builder: (context, state) => PageClimber(),
    ),
    GoRoute(
      path: '/cam_calibration',
      builder: (context, state) => PageCameraCalibration(),
    ),
    GoRoute(
      path: '/settings',
      builder: (context, state) => PageSettings(),
    ),
    GoRoute(
      path: '/about',
      builder: (context, state) => PageAbout(),
    ),
  ]

);
