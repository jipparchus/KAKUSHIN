import 'package:flutter_riverpod/flutter_riverpod.dart';

final indexProvider = StateProvider<int>((ref) => 0);
// AuthN state
final isAuthenticatedProvider = StateProvider<bool>((ref) => false);