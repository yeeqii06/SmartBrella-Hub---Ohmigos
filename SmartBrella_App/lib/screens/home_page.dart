import 'package:flutter/material.dart';
import 'loading_page.dart';
import 'map_screen.dart';
import 'order_store.dart';
import 'order_model.dart';
import 'station_store.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _studentIdController = TextEditingController();

  /// Step 1: Choose Station
  void _chooseStationDialog(String action) {
    showDialog(
      context: context,
      builder: (context) => SimpleDialog(
        title: Text("${action == "borrow" ? "Borrow" : "Return"} from which station?"),
        children: StationStore().stations.keys.map((station) {
          return SimpleDialogOption(
            onPressed: () {
              Navigator.pop(context);
              _showBorrowReturnDialog(action, station);
            },
            child: Text(station),
          );
        }).toList(),
      ),
    );
  }

  /// Step 2: Enter Student ID
  void _showBorrowReturnDialog(String action, String station) {
    _studentIdController.clear();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text("${action == "borrow" ? "Borrow" : "Return"} Umbrella"),
        content: TextField(
          controller: _studentIdController,
          decoration: const InputDecoration(
            labelText: "Enter Student ID",
            border: OutlineInputBorder(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Cancel"),
          ),
          ElevatedButton(
            onPressed: () {
              final studentId = _studentIdController.text.trim();
              if (studentId.isEmpty) return;

              // ✅ Save order record
              final order = Order(
                studentId: studentId,
                station: station,
                status: action == "borrow" ? "Borrowed" : "Returned",
                borrowedAt: DateTime.now(),
              );
              OrderStore().addOrder(order);

              // ✅ Update umbrella counts
              if (action == "borrow") {
                StationStore().borrowUmbrella(station);
              } else {
                StationStore().returnUmbrella(station);
              }

              setState(() {}); // Refresh UI

              Navigator.pop(context);
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => LoadingPage(action: action),
                ),
              );
            },
            child: const Text("Confirm"),
          ),
        ],
      ),
    );
  }

  Widget _buildStationCard(String name) {
    final available = StationStore().stations[name]!;
    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      elevation: 3,
      child: ListTile(
        leading: const Icon(Icons.umbrella, color: Colors.blueAccent),
        title: Text(name),
        subtitle: Text("$available umbrellas available"),
        trailing: const Icon(Icons.arrow_forward_ios),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const MapScreen()),
          );
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Smart Umbrella System"),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Weather forecast
            Card(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
              color: Colors.blue[50],
              elevation: 2,
              child: const Padding(
                padding: EdgeInsets.all(16.0),
                child: Text(
                  "☀️ Today's Weather: Sunny, 32°C",
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w500),
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Umbrella Stations
            Card(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Text(
                      "Umbrella Stations",
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 10),

                    _buildStationCard("Library Station"),
                    _buildStationCard("Cafeteria Station"),
                    _buildStationCard("Hostel Station"),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Borrow Button (Green)
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                padding: const EdgeInsets.symmetric(vertical: 18),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
              ),
              onPressed: () => _chooseStationDialog("borrow"),
              child: const Text(
                "Borrow Umbrella",
                style: TextStyle(color: Colors.white, fontSize: 18),
              ),
            ),
            const SizedBox(height: 12),

            // Return Button (Red)
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red,
                padding: const EdgeInsets.symmetric(vertical: 18),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
              ),
              onPressed: () => _chooseStationDialog("return"),
              child: const Text(
                "Return Umbrella",
                style: TextStyle(color: Colors.white, fontSize: 18),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
