import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'order_store.dart';

class OrdersPage extends StatelessWidget {
  const OrdersPage({super.key});

  @override
  Widget build(BuildContext context) {
    final orders = OrderStore().orders;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Orders / Borrowings'),
        backgroundColor: Colors.blueAccent,
      ),
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: orders.isEmpty
            ? const Center(child: Text('No borrowings found'))
            : ListView.builder(
                itemCount: orders.length,
                itemBuilder: (ctx, i) {
                  final o = orders[i];
                  final borrowed = o.status == 'Borrowed';
                  return Card(
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12)),
                    elevation: 3,
                    child: ListTile(
                      title: Text('${o.studentId} — ${o.station}'),
                      subtitle: Text(
                        'At: ${DateFormat('yyyy-MM-dd HH:mm').format(o.borrowedAt)}',
                      ),
                      trailing: Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 6),
                        decoration: BoxDecoration(
                          color: borrowed
                              ? Colors.orange.shade100
                              : Colors.green.shade100,
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Text(
                          o.status,
                          style: TextStyle(
                            fontWeight: FontWeight.w600,
                            color: borrowed
                                ? Colors.orange.shade900
                                : Colors.green.shade900,
                          ),
                        ),
                      ),
                    ),
                  );
                },
              ),
      ),
    );
  }
}
