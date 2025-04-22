import 'package:carousel_slider/carousel_slider.dart';
import 'package:flutter/material.dart';

class CarouselWidgetMemory extends StatelessWidget {
  final List<Image> images;

  const CarouselWidgetMemory({super.key, required this.images});

  @override
  Widget build(BuildContext context) {
    return CarouselSlider.builder(
      itemCount: images.length,
      options: CarouselOptions(
        height: 250,
        enableInfiniteScroll: false,
        enlargeCenterPage: true,
        viewportFraction: 0.8,
      ),
      itemBuilder: (context, index, _) {
        return Container(
          width: 250,
          height: 250,
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: Colors.grey[200],
            borderRadius: BorderRadius.circular(12),
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(12),
            child: images[index],
          ),
        );
      },
    );
  }
}
