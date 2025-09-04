import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

class MapScreen extends StatelessWidget {
  final double? highlightLat;
  final double? highlightLng;
  final String? highlightName;

  const MapScreen({super.key, this.highlightLat, this.highlightLng, this.highlightName});

  @override
  Widget build(BuildContext context) {
    const LatLng upmCenter = LatLng(2.9956, 101.7077);

    const List<Map<String, dynamic>> stations = [
      {"name": "Library Station", "position": LatLng(2.9960, 101.7072)},
      {"name": "Cafeteria Station", "position": LatLng(2.9948, 101.7080)},
      {"name": "Engineering Block", "position": LatLng(2.9942, 101.7068)},
    ];

    final List<Marker> markers = stations.map((station) {
      bool isHighlight = highlightLat != null &&
          highlightLng != null &&
          highlightLat == station["position"].latitude &&
          highlightLng == station["position"].longitude;

      return Marker(
        point: station["position"] as LatLng,
        width: 50,
        height: 50,
        child: GestureDetector(
          // onTap: () {
          //   ScaffoldMessenger.of(context).showSnackBar(
          //     SnackBar(content: Text("${station["name"]} tapped!")),
          //   );
          // },
          child: Icon(
            Icons.location_on,
            color: isHighlight ? Colors.green : Colors.red,
            size: 40,
          ),
        ),
      );
    }).toList();

    final LatLng mapCenter = (highlightLat != null && highlightLng != null)
        ? LatLng(highlightLat!, highlightLng!)
        : upmCenter;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Nearby Umbrellas"),
        backgroundColor: Colors.blueAccent,
      ),
      body: Stack(
        children: [
          FlutterMap(
            options: MapOptions(
              initialCenter: mapCenter,
              initialZoom: 17,
              maxZoom: 25,
            ),
            children: [
              TileLayer(
                urlTemplate: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                userAgentPackageName: 'com.example.upmbrella',
              ),
              MarkerLayer(markers: markers),
            ],
          ),
          // OSM Attribution overlay
          Positioned(
            bottom: 4,
            right: 4,
            child: Container(
              color: Colors.white70,
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
              child: const Text(
                "© OpenStreetMap contributors",
                style: TextStyle(fontSize: 10),
              ),
            ),
          ),
        ],
      ),
    );
  }
}