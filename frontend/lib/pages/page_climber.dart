import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/models/model_user_profile.dart';
import 'package:frontend/utils/utils_get_jwt.dart';
import 'package:frontend/widgets/widget_home_btn.dart';
import 'package:frontend/widgets/widget_side_menu.dart';
import 'package:http/http.dart' as http;


// Status message
final usernameProvider = StateProvider<String>((ref) => 'Username');
final svrresponseProvider = StateProvider<String>((ref) => 'Server response');


class PageClimber extends ConsumerStatefulWidget {
  const PageClimber({super.key});

  @override
  ConsumerState<PageClimber> createState() => _UserProfileFormState();
}

class _UserProfileFormState extends ConsumerState<PageClimber> {
  final _formKey = GlobalKey<FormState>();

  String? _vGrade;
  final _heightController = TextEditingController();
  final _weightController = TextEditingController();
  bool _shareInfo = false;

  UserProfile? _originalData;

  @override
  void initState() {
    super.initState();
    _fetchUserData(); // Get initial values from backend
  }

  Future<void> _fetchUserData() async {
    // Load the JWT saved
    final jwtToken = await getJWT();

    final response = await http.get(
      Uri.parse('http://127.0.0.1:8000/user/profile'),
      headers: {
        'Authorization': 'Bearer $jwtToken',
      },
    );
    if (response.statusCode == 200) {
      final user = UserProfile.fromJson(jsonDecode(response.body));
      // Show the username
      ref.read(usernameProvider.notifier).state = jsonDecode(response.body)['username'];
      // Set the default values to the user input
      setState(() {
        _originalData = user;
        _vGrade = user.vGrade;
        _heightController.text = user.height?.toString() ?? '';
        _weightController.text = user.weight?.toString() ?? '';
        _shareInfo = user.shareInfo;
      });
    } else {
      ref.read(svrresponseProvider.notifier).state = '❌ Error: ${response.statusCode}';
      debugPrint("❌ Error: ${response.statusCode}");
    }
  }

  void _revert() {
    if (_originalData != null) {
      setState(() {
        _vGrade = _originalData!.vGrade;
        _heightController.text = _originalData!.height?.toString() ?? '';
        _weightController.text = _originalData!.weight?.toString() ?? '';
        _shareInfo = _originalData!.shareInfo;
      });
    }
  }

  Future<void> _submit() async {
    // Load the JWT saved
    final jwtToken = await getJWT();
    final height = double.tryParse(_heightController.text);
    final weight = double.tryParse(_weightController.text);

    final updateData = {
      'v_grade': _vGrade == 'NA' ? null : _vGrade,
      'height': height,
      'weight': weight,
      'share_info': _shareInfo,
    }; 

    final response = await http.put(
      Uri.parse('http://127.0.0.1:8000/user/profile'),
      headers: {
        'Authorization': 'Bearer $jwtToken',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(updateData),
    );

    if (response.statusCode == 200) {
      ref.read(svrresponseProvider.notifier).state = '✅ Submitted\n${jsonEncode(updateData)}';
      debugPrint('✅ Submitted');
      _fetchUserData(); // Refresh
    } else {
      debugPrint('########################');
      debugPrint(jsonEncode(updateData));
      debugPrint('########################');
      debugPrint('❌ Failed: ${response.statusCode}');
      ref.read(svrresponseProvider.notifier).state = '❌ Failed: ${response.statusCode}\n${jsonEncode(updateData)}';
    }
  }

  @override
  void dispose() {
    _heightController.dispose();
    _weightController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Climber'),
        backgroundColor: Color.fromARGB(255, 117, 192, 151),
      ),
      drawer: Drawer(
        child: SideMenu(),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const SizedBox(height: 18),
                  Text(ref.watch(usernameProvider),
                  style: TextStyle(fontSize: 20),),
                  const SizedBox(height: 18),                
                ],
              ),

              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('Please entre your profile.'),
                ],
              ),
              // V-Grade Dropdown
              DropdownButtonFormField<String>(
                value: _vGrade,
                decoration: const InputDecoration(labelText: 'Max Boulder Grade'),
                items: [
                  const DropdownMenuItem(value: 'NA', child: Text('NA')),
                  ...List.generate(
                    13,
                    (index) => DropdownMenuItem(
                      value: 'V${index + 1}',
                      child: Text("V${index + 1}"),
                    ),
                  )
                ],
                onChanged: (val) => setState(() => _vGrade = val),
              ),

              const SizedBox(height: 16),

              // Height
              TextFormField(
                controller: _heightController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: "Height (cm)",
                  hintText: "Leave blank if not applicable",
                ),
              ),

              const SizedBox(height: 16),

              // Weight
              TextFormField(
                controller: _weightController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: "Weight (kg)",
                  hintText: "Leave blank if not applicable",
                ),
              ),

              const SizedBox(height: 16),

              // Share Info
              SwitchListTile(
                title: const Text("Share info (V-Grade, Height, and Weight)"),
                value: _shareInfo,
                onChanged: (val) => setState(() => _shareInfo = val),
              ),

              const SizedBox(height: 24),

              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  OutlinedButton(
                    onPressed: _revert,
                    child: const Text("Revert changes"),
                  ),
                  ElevatedButton(
                    onPressed: _submit,
                    child: const Text("Submit"),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(ref.watch(svrresponseProvider)),
                ],
              ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  HomeBtn(),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
