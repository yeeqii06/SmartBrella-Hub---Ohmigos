import 'order_model.dart';

class OrderStore {
  static final OrderStore _instance = OrderStore._internal();
  factory OrderStore() => _instance;
  OrderStore._internal();

  final List<Order> _orders = [];

  List<Order> get orders => _orders;

  void addOrder(Order order) {
    _orders.insert(0, order); // add newest on top
  }
}
