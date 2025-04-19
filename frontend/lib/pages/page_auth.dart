import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/pages/page_main.dart';
import 'package:frontend/utils/utils_auth_request.dart';

// State providers
// Authentication state
final isAuthenticatedProvider = StateProvider<bool>((ref) => false);
// Password visibility state
final passwordVisibleProvider = StateProvider<bool>((ref) => false);
// Status message
final statusmessageProvider = StateProvider<String>((ref) => 'Please login');


class AuthPage extends ConsumerStatefulWidget {
  const AuthPage({super.key});

  @override
  ConsumerState<AuthPage> createState() => _AuthPageState();
}

class _AuthPageState extends ConsumerState<AuthPage> {
  final _formKey = GlobalKey<FormState>();

  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _onAuthRequest(String authtype) async {
    
    if (_formKey.currentState!.validate()) {
      final username = _usernameController.text.trim();
      final password = _passwordController.text;

      try {
        final response = await auth(authtype, username, password);
        if (response == 200) { // Authenticated
          ref.read(isAuthenticatedProvider.notifier).state = true;
          ref.read(statusmessageProvider.notifier).state = '';
          if (context.mounted) {
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(
                builder: (_) => const MyApp(),  // App main page
              ),
            );
          }
        } else if (response == 400) {
          ref.read(isAuthenticatedProvider.notifier).state = false;
          ref.read(statusmessageProvider.notifier).state = '🙈 Username already exists';
        } else if (response == 401) {
          ref.read(isAuthenticatedProvider.notifier).state = false;
          ref.read(statusmessageProvider.notifier).state = '🙊 Invalid credentials';
        } else {
          ref.read(isAuthenticatedProvider.notifier).state = false;
          ref.read(statusmessageProvider.notifier).state = '🐒 Invalid credentials';
        }
      } catch (e, st) {
        debugPrint('🦥 Login error: $e');
          ref.read(isAuthenticatedProvider.notifier).state = false;
        ref.read(statusmessageProvider.notifier).state = '🦥 Invalid credentials';
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final passwordVisible = ref.watch(passwordVisibleProvider);


    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Sign In / Sign Up',
          style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.black54,
                )
          ),
        backgroundColor: Color.fromARGB(255, 117, 192, 151),
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              // Status Code to from the server
              Text(
                ref.watch(statusmessageProvider),
                style: TextStyle(
                  fontSize: 20
                ),
              ),
              const SizedBox(height: 16),
              // Username
              TextFormField(
                controller: _usernameController,
                decoration: const InputDecoration(
                  labelText: 'Username',
                  border: OutlineInputBorder(),
                ),
                validator: (val) {
                  if (val == null || val.isEmpty) return 'Username is required';
                  return null;
                },
              ),
              const SizedBox(height: 16),

              // Password
              TextFormField(
                controller: _passwordController,
                obscureText: !passwordVisible,
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(passwordVisible
                        ? Icons.visibility
                        : Icons.visibility_off),
                    onPressed: () {
                      ref.read(passwordVisibleProvider.notifier).state =
                          !passwordVisible;
                    },
                  ),
                ),
                validator: (val) {
                  if (val == null || val.isEmpty) return 'Password is required';
                  if (val.length < 8) return 'Minimum 8 characters';
                  if (!val.contains(RegExp(r'[!@#$%^&*(),.?":{}|<>]'))) {
                    return 'Add at least 1 special character';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ElevatedButton(
                    onPressed: () => _onAuthRequest('register'),
                    child: const Text(
                      'Register',
                      style: TextStyle(
                        fontSize: 15,
                      ),
                    ),
                  ),
                  ElevatedButton(
                    onPressed: () =>_onAuthRequest('login'),
                    child: const Text(
                      'Login',
                      style: TextStyle(
                          fontSize: 15,
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
