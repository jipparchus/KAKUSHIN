import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

class VideoSelectorWidget extends StatefulWidget {
  final Function(File) onVideoSelected;

  const VideoSelectorWidget({required this.onVideoSelected, super.key});

  @override
  State<VideoSelectorWidget> createState() => _VideoSelectorWidgetState();
}

class _VideoSelectorWidgetState extends State<VideoSelectorWidget> {
  String? fileName;

  Future<void> _pickVideo() async {
    final result = await FilePicker.platform.pickFiles(type: FileType.video);
    if (result != null && result.files.single.path != null) {
      final file = File(result.files.single.path!);
      widget.onVideoSelected(file);
      setState(() {
        fileName = file.path.split('/').last;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ElevatedButton.icon(
          onPressed: _pickVideo,
          icon: const Icon(Icons.video_library),
          label: const Text('Select Video'),
        ),
        // if (fileName != null)
        //   Text(
        //     '$fileName',
        //     style: const TextStyle(fontSize: 12),
        //   ),
      ],
    );
  }
}