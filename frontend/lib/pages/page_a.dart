import 'dart:io';

import 'package:flutter/material.dart';
import 'package:frontend/utils/upload_progress_stream.dart';
import 'package:frontend/utils/utils_get_jwt.dart';
import 'package:frontend/widgets/widget_ipinput.dart';
import 'package:frontend/widgets/widget_side_menu.dart';
import 'package:frontend/widgets/widget_video_player.dart';
import 'package:frontend/widgets/widget_video_selector.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:path/path.dart';
import 'package:percent_indicator/percent_indicator.dart';



class PageA extends StatefulWidget {
  const PageA({super.key});

  @override
  State<PageA> createState() => _PageAState();
}

class _PageAState extends State<PageA> {
  File? _selectedVideo;

  String ipAddress = '';
  double _uploadProgress = 0.0;
  String _videoInfo = '1. Select the video, wall type & problem name\n2. Sende them to the server';

Future<void> _onSendVideo() async {
  if (_selectedVideo == null) return;

  final jwtToken = await getJWT(); // Get token from shared_preferences

  setState(() {
    _uploadProgress = 0.0;
    _videoInfo = '📨 Uploading...\nPlease wait.';
  });

  final request = http.MultipartRequest(
    'POST',
    Uri.parse('http://127.0.0.1:8000/upload/video'),
  );
  request.headers['Authorization'] = 'Bearer $jwtToken';

  final file = _selectedVideo!;
  final fileLength = await _selectedVideo!.length();
  final stream = UploadProgressStream(
    file.openRead(),
    fileLength,
    (sent) {
      setState(() {
        _uploadProgress = sent / fileLength;
      });
    },
  );

  request.files.add(
    http.MultipartFile(
      'video',
      http.ByteStream(stream), // wrap it here
      fileLength,
      filename: basename(file.path),
      contentType: MediaType('video', 'mp4'),
    ),
  );

  final streamedResponse = await request.send();


  final response = await http.Response.fromStream(streamedResponse);

  if (response.statusCode == 200) {
    setState(() {
      _videoInfo = '✅ Upload successful: \n${response.body}';
      _uploadProgress = 1.0;
    });
  } else {
    setState(() {
      _videoInfo = '❌ Upload failed: \n${response.statusCode}';
      _uploadProgress = 0.0;
    });
  }
}


  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('Video Upload'),
          backgroundColor: Color.fromARGB(255, 117, 192, 151),
          ),
        drawer: Drawer(
          child: SideMenu(),
          ),
        body: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              Text(
                'Original Video',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.black54,
                )
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    VideoSelectorWidget(
                      onVideoSelected: (file) {
                        setState(() {
                          _selectedVideo = file;
                        });
                      },
                    ),
                    SizedBox(
                      width: 300,
                      child: IpInputWidget(onIpChanged: (ip) => ipAddress = ip),
                    )
                  ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  if (_selectedVideo != null)
                    Padding(
                      padding: const EdgeInsets.all(5.0),
                        child: Align(
                            alignment: Alignment.topCenter,
                            child: SizedBox(
                                width: 250,
                                height:250,
                                child: VideoPlayerWidget(videoFile: _selectedVideo!),
                              ),
                          ),
                        )
                    else 
                      const ColoredBox(
                        color: Colors.grey,
                        child: SizedBox(
                                width: 250,
                                height: 250,
                                child: Center(
                                  child: Text('No video selected'),
                                  ),
                            ),
                      ),
                  Column(
                    children: [
                      const Text('Wall: '),
                      const Text('Problem: '),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _onSendVideo,
                        style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.blueAccent),
                        child: const Text('Send'),
                      ),
                    ],
                  ),
                ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Text(_videoInfo),
                  CircularPercentIndicator(
                      radius: 30.0,
                      lineWidth: 5.0,
                      percent: _uploadProgress,
                      center: Text(_uploadProgress.toStringAsFixed(2)),
                      progressColor: Colors.green,
                  ),
                ],
              ),
              Text(
                'Annotated Video',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.black54,
                )
              ),
              Text(
                'Climber & Wall 3D Model',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.black54,
                )
              ),
            ],) 
          ),
    );
  }
}
