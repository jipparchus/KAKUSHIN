import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:url_launcher/url_launcher.dart';

class MarkdownWidget extends StatefulWidget {
  final String assetPath;
  final String title;

  const MarkdownWidget({super.key, required this.assetPath, required this.title});

  @override
  State<MarkdownWidget> createState() => _MarkdownWidgetState();
}

class _MarkdownWidgetState extends State<MarkdownWidget> {
  String _markdownContent = "";

  @override
  void initState() {
    super.initState();
    _loadMarkdown();
  }

  Future<void> _loadMarkdown() async {
    final content = await rootBundle.loadString(widget.assetPath);
    setState(() {
      _markdownContent = content;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.title,
          style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                  color: Colors.black54,
                )
          ),
        backgroundColor: Color.fromARGB(255, 117, 192, 151),
      ),
      body: Markdown(
        data: _markdownContent,
        selectable: true,
        padding: const EdgeInsets.all(16),
        styleSheet: MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
          p: const TextStyle(fontSize: 16),
        ),
        onTapLink: (text, href, title) {
          if (href != null) {
            launchUrl(Uri.parse(href)); // Add url_launcher for this
          }
        },
      ),
    );
  }
}
