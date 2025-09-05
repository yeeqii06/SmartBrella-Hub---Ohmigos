import 'package:flutter/material.dart';

class BorrowReturnScreen extends StatelessWidget {
  const BorrowReturnScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Borrow / Return Umbrella')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => _promptStudentId(context, 'Borrow'),
              child: const Text('Borrow Umbrella'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => _promptStudentId(context, 'Return'),
              child: const Text('Return Umbrella'),
            ),
          ],
        ),
      ),
    );
  }

  void _promptStudentId(BuildContext context, String action) {
    final controller = TextEditingController();
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text('$action Umbrella'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(labelText: 'Enter Student ID'),
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('$action confirmed for ID: ${controller.text}')),
              );
            },
            child: const Text('Confirm'),
          ),
        ],
      ),
    );
  }
}
