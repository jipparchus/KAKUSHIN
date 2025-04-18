import 'dart:io';

import 'package:chewie/chewie.dart';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

class VideoPlayerWidget extends StatefulWidget {
  final File videoFile;

  const VideoPlayerWidget({required this.videoFile, super.key});

  @override
  State<VideoPlayerWidget> createState() => _VideoPlayerWidgetState();
}

class _VideoPlayerWidgetState extends State<VideoPlayerWidget> {
  late VideoPlayerController _controller;
  ChewieController? _chewieController;

  @override
  void initState() {
    super.initState();
    initializePlayer();
  }

  Future<void> initializePlayer() async {
    _controller = VideoPlayerController.file(widget.videoFile);
    await _controller.initialize();

    _chewieController = ChewieController(
      videoPlayerController: _controller,
      autoPlay: true,
      looping: true,
      showControls: true,
    );

    setState(() {});
  }

  @override
  void dispose() {
    _controller.dispose();
    _chewieController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final chewie = _chewieController;

    if (chewie == null || !_controller.value.isInitialized) {
      return const Center(child: CircularProgressIndicator());
    }

    return Chewie(controller: chewie);
  }
}



// import 'package:chewie/chewie.dart';
// import 'package:flutter/material.dart';
// import 'package:video_player/video_player.dart';

// class VideoPlayerWidget extends StatefulWidget {
//   const VideoPlayerWidget({super.key});

//   @override
//   State<VideoPlayerWidget> createState() => _VideoPlayerWidgetState();
// }

// class _VideoPlayerWidgetState extends State<VideoPlayerWidget> {
  
//   late VideoPlayerController _controller;
//   ChewieController? _chewieController;

//   @override
//   void initState() {
//     initializePlayer();
//     super.initState();
//   }

//   Future<void> initializePlayer () async {
//     _controller = VideoPlayerController.asset('assets/videos/1StarChoss_trimmed.mp4');
//     await _controller.initialize();
//     _chewieController = ChewieController(
//       videoPlayerController: _controller,
//       autoPlay: true,
//       looping: true,
//       showControls: true,
//     );
//     setState(() {});
//   }
  
//   @override
//   void dispose() {
//     _controller.dispose();
//     _chewieController?.dispose();
//     super.dispose();
//   }

//   @override
//   Widget build(BuildContext context) {
//     return LayoutBuilder(
//       builder: (context, constraints) {
//         final chewieController = _chewieController;
//         if (chewieController != null) {
//           return Chewie(controller: chewieController,
//           );
//         } else {
//           return SizedBox();
//         }
//       },
//       );
//   }

// }