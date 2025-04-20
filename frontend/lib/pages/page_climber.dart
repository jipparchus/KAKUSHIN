import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/models/model_user_profile.dart';
import 'package:frontend/utils/utils_get_jwt.dart';
import 'package:frontend/widgets/widget_home_btn.dart';
import 'package:frontend/widgets/widget_side_menu.dart';
import 'package:http/http.dart' as http;


class PageClimber extends ConsumerStatefulWidget {
  const PageClimber({super.key});

  @override
  ConsumerState<PageClimber> createState() => _UserProfileFormState();
}

class _UserProfileFormState extends ConsumerState<PageClimber> {
  final _formKey = GlobalKey<FormState>();

  int? _vGrade;
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
      // Set the default values to the user input
      setState(() {
        _originalData = user;
        _vGrade = user.vGrade;
        _heightController.text = user.height?.toString() ?? '';
        _weightController.text = user.weight?.toString() ?? '';
        _shareInfo = user.shareInfo;
      });
    } else {
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
      'v_grade': _vGrade,
      'height': height,
      'weight': weight,
      'share_info': _shareInfo,
    };

    final response = await http.put(
      Uri.parse('http://127.0.0.1:8000/user/profile'),
      headers: {
        'Authorization': 'Bearer $jwtToken',
      },
      body: jsonEncode(updateData),
    );

    if (response.statusCode == 200) {
      debugPrint('✅ Updated');
      _fetchUserData(); // Refresh
    } else {
      debugPrint('❌ Failed: ${response.statusCode}');
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
                  Text('Please entre your profile.'),
                ],
              ),
              // V-Grade Dropdown
              DropdownButtonFormField<int>(
                value: _vGrade,
                decoration: const InputDecoration(labelText: 'V-Grade'),
                items: [
                  const DropdownMenuItem(value: null, child: Text('NA')),
                  ...List.generate(
                    13,
                    (index) => DropdownMenuItem(
                      value: index + 1,
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
                    child: const Text("Update"),
                  ),
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
