import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
// import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:frontend/utils/utils_get_jwt.dart';
import 'package:frontend/widgets/widget_home_btn.dart';
import 'package:frontend/widgets/widget_image_carousel.dart';
import 'package:frontend/widgets/widget_image_selector.dart';
import 'package:frontend/widgets/widget_side_menu.dart';
import 'package:http/http.dart' as http;
import 'package:path/path.dart';

// Monitoring variables
// final imgsubmissionProvider = StateProvider<String>((ref) => '-- Image Submission Status --');
// final camcalibrationProvider = StateProvider<String>((ref) => '-- Camera Calibration Status --');

class PageCameraCalibration extends StatefulWidget {
  const PageCameraCalibration({super.key});

  @override
  State<PageCameraCalibration> createState() => _PageCameraCalibrationState();
}

class _PageCameraCalibrationState extends State<PageCameraCalibration> {
  String _submissionInfo = 'Select the calibration images and submit them';
  String _calibrationInfo = '';

  final List<File> _selectedImages = [];

  void _addImages(List<File> newImages) {
    setState(() {
      _selectedImages.addAll(newImages);
    });
  }

  void _removeImage(int index) {
    setState(() {
      _selectedImages.removeAt(index);
    });
  }

  Future<void> _submitImages() async {
    if (_selectedImages.isEmpty) return;
    final jwtToken = await getJWT(); // Get token from shared_preferences

    final request = http.MultipartRequest(
      'POST',
      Uri.parse('http://127.0.0.1:8000/upload/images'),
    );
    // Add JWTT
    request.headers['Authorization'] = 'Bearer $jwtToken';
    // Add mode for image upload request
    request.headers['mode'] = 'cam_calibration';

    for (var image in _selectedImages) {
      request.files.add(
        await http.MultipartFile.fromPath(
          'images',
          image.path,
          filename: basename(image.path),
        ),
      );
    }

    final response = await request.send();
    final responseText = await response.stream.bytesToString();
    final responseBody = jsonDecode(responseText);


    if (response.statusCode == 200) {
      debugPrint('✅ Upload and calibration successful');
      setState(() {
        _submissionInfo = '✅ Upload successful';
        _calibrationInfo = '✅ Calibration successful';
        _selectedImages.clear();
      });
    } else {
      debugPrint('❌ Upload failed: ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Camera Calibration'),
        backgroundColor: Color.fromARGB(255, 117, 192, 151),
      ),
      drawer: const Drawer(
        child: SideMenu(),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ImageSelectorWidget(
                  onImagesSelected: (files) {
                    setState(() {
                      _addImages(files);
                    });
                  }
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (_selectedImages.isNotEmpty)
              CarouselWidget(
                images: _selectedImages,
                onRemoveImage: _removeImage,
              )
            else
            Row (
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                  ColoredBox(
                    color: Colors.grey,
                    child: SizedBox(
                            width: 250,
                            height: 250,
                            child: Center(
                              child: Text('No Images selected'),
                            ),
                      ),
                  ),
              ]
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: _submitImages,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                  ),
                  child: const Text(
                    'Submit Images & Start Calibration',
                    style: TextStyle(
                      color: Colors.white70
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(_submissionInfo),
              ],
            ),
            const SizedBox(height: 16),

            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(_calibrationInfo),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const HomeBtn(),
              ],
            ),
            const SizedBox(height: 16),            
          ],
        ),
      ),
    );
  }
}
