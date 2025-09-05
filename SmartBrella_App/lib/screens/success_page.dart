import 'package:flutter/material.dart';
import 'dart:async';

class SuccessPage extends StatefulWidget {
  final String action;
  const SuccessPage({super.key, required this.action});

  @override
  State<SuccessPage> createState() => _SuccessPageState();
}

class _SuccessPageState extends State<SuccessPage> {
  bool _showIcon = false;

  @override
  void initState() {
    super.initState();
    Timer(const Duration(milliseconds: 200), () {
      setState(() {
        _showIcon = true;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    String message = widget.action == "borrow"
        ? "Umbrella Borrowed Successfully!"
        : "Umbrella Returned Successfully!";

    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AnimatedScale(
              scale: _showIcon ? 1.0 : 0.0,
              duration: const Duration(milliseconds: 600),
              curve: Curves.elasticOut,
              child: AnimatedOpacity(
                opacity: _showIcon ? 1.0 : 0.0,
                duration: const Duration(milliseconds: 600),
                child: Container(
                  decoration: const BoxDecoration(
                    color: Colors.green,
                    shape: BoxShape.circle,
                  ),
                  padding: const EdgeInsets.all(20),
                  child: const Icon(Icons.check, size: 60, color: Colors.white),
                ),
              ),
            ),
            const SizedBox(height: 20),
            Text(
              message,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.green,
              ),
            ),
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: () => Navigator.pop(context),
              child: const Text("Back to Home"),
            ),
          ],
        ),
      ),
    );
  }
}
