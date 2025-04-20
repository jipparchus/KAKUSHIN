import 'dart:convert';

import 'package:http/http.dart' as http;

Future auth(String authtype, String username, String password) async {
  // authtypes are 'register' or 'login'
  final uri = Uri.parse('http://127.0.0.1:8000/auth/$authtype');

  final response = await http.post(
    uri,
    headers: {
      'Content-Type': 'application/json',
    },
    body: jsonEncode({
      'username': username,
      'password': password,
    }),
  );
  return response;
}