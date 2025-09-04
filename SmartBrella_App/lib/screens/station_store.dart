// lib/data/station_store.dart
class StationStore {
  static final StationStore _instance = StationStore._internal();
  factory StationStore() => _instance;
  StationStore._internal();

  // Initial umbrella counts at stations
  final Map<String, int> _stations = {
    "Library Station": 10,
    "Cafeteria Station": 7,
    "Hostel Station": 5,
  };

  Map<String, int> get stations => _stations;

  /// Deduct 1 umbrella when borrowed
  void borrowUmbrella(String station) {
    if (_stations.containsKey(station) && _stations[station]! > 0) {
      _stations[station] = _stations[station]! - 1;
    }
  }

  /// Add 1 umbrella when returned
  void returnUmbrella(String station) {
    if (_stations.containsKey(station)) {
      _stations[station] = _stations[station]! + 1;
    }
  }
}
