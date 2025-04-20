import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

Future<String?> getJWT() async {
  // Load the saved JWT
  final prefs = await SharedPreferences.getInstance();
  final token = prefs.getString("jwt_token");
  debugPrint("JWT loaded: $token");
  return token;
}


