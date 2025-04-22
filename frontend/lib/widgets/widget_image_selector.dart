import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

class ImageSelectorWidget extends StatefulWidget {
  final void Function(List<File> files) onImagesSelected;

  const ImageSelectorWidget({super.key, required this.onImagesSelected});

  @override
  State<ImageSelectorWidget> createState() => _ImageSelectorWidgetState();
}

class _ImageSelectorWidgetState extends State<ImageSelectorWidget> {
  List<String> fileNames = [];

  Future<void> _pickImages() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.image,
      allowMultiple: true, // ✅ allow selecting multiple images
    );

    if (result != null && result.files.isNotEmpty) {
      final files = result.paths.map((p) => File(p!)).toList();

      widget.onImagesSelected(files); // ✅ send all selected files

      setState(() {
        fileNames = files.map((f) => f.path.split('/').last).toList();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton.icon(
          onPressed: _pickImages,
          icon: const Icon(Icons.collections),
          label: const Text('Select Images'),
        ),
        // if (fileNames.isNotEmpty)
        //   Text(
        //     'Selected: ${fileNames.join(", ")}',
        //     style: const TextStyle(fontSize: 12),
        //   ),
      ],
    );
  }
}
