import 'package:flutter/material.dart';
import 'screens/home_page.dart';
import 'screens/orders_page.dart';
import 'screens/station_store.dart';
import 'screens/order_store.dart';
import 'screens/register_page.dart';

void main() {
  // Initialize singleton stores
  WidgetsFlutterBinding.ensureInitialized();
  StationStore(); // Ensure single instance
  OrderStore(); // Ensure single instance

  runApp(const UPMbrellaApp());
}

  @override 
  Widget build(BuildContext context) { 
    return MaterialApp( 
      title: 'SmartBrella Registration', 
      theme: ThemeData( 
        primarySwatch: Colors.blue, 
      ), 
      home: const RegistrationPage(), // start at registration page 
    ); 
  } 

class UPMbrellaApp extends StatelessWidget {
  const UPMbrellaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Smart Umbrella System",
      theme: ThemeData(
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: Colors.grey[100],
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
 debugShowCheckedModeBanner: false,
  home: const RegistrationPage(),   // 👈 Start here
  routes: {
    "/main": (_) => const MainNavigation(),  // 👈 after login/register
  },
    );
  }
}

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _selectedIndex = 0;

  // Pages for each tab (not const because they rely on stores and auto-update)
  final List<Widget> _pages = [
    const HomePage(),
    const OrdersPage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_selectedIndex], // Show selected page
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: "Home",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.assignment),
            label: "Details",
          ),
        ],
      ),
    );
  }
}


