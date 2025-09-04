class Order {
  final String studentId;
  final String station;
  final String status; // "Borrowed" or "Returned"
  final DateTime borrowedAt;

  Order({
    required this.studentId,
    required this.station,
    required this.status,
    required this.borrowedAt,
  });
}
