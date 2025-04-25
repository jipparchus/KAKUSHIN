import 'dart:io';

import 'package:carousel_slider/carousel_slider.dart';
import 'package:flutter/material.dart';

class CarouselWidget extends StatelessWidget {
  final List<File> images;
  final void Function(int index) onRemoveImage;

  const CarouselWidget({
    super.key,
    required this.images,
    required this.onRemoveImage,
  });

  void _showRemoveDialog(BuildContext context, int index) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Remove Image?'),
        content: const Text('Do you want to remove this image?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            style: ButtonStyle(
              backgroundColor: WidgetStateProperty.all(Colors.redAccent)
            ),
            onPressed: () {
              onRemoveImage(index);
              Navigator.pop(context);
            },
            child: const Text(
              'Remove',
              style: TextStyle(
                color: Colors.white70
              ),
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return CarouselSlider.builder(
      itemCount: images.length,
      options: CarouselOptions(
        height: 250,
        viewportFraction: 0.55,
        enableInfiniteScroll: false,
        enlargeCenterPage: true,
      ),
      itemBuilder: (context, index, realIndex) {
        return GestureDetector(
          onLongPress: () => _showRemoveDialog(context, index),
          child: Container(
            width: 250,
            height: 250,
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.grey,
              borderRadius: BorderRadius.circular(16),
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: FittedBox(
                fit: BoxFit.contain, // 👈 keeps aspect ratio, no cropping
                child: SizedBox(
                  // width: images[index].width.toDouble(), // optional
                  // width: Image.file(images[index]).width, // optional
                  child: Image.file(images[index]),
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
