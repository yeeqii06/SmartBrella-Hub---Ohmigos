import 'package:flutter/material.dart';
import 'dart:async';
import 'success_page.dart';

class LoadingPage extends StatefulWidget {
  final String action;
  const LoadingPage({super.key, required this.action});

  @override
  State<LoadingPage> createState() => _LoadingPageState();
}

class _LoadingPageState extends State<LoadingPage>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();

    // umbrella spinning
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat();

    // after 2s go to success page
    Timer(const Duration(seconds: 2), () {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => SuccessPage(action: widget.action),
        ),
      );
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            RotationTransition(
              turns: _controller,
              child: Icon(
                Icons.umbrella, // 🌂 umbrella icon
                size: 100,
                color: Colors.blueAccent,
              ),
            ),
            const SizedBox(height: 30),
            const Text(
              "Processing...",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.w500),
            ),
          ],
        ),
      ),
    );
  }
}
