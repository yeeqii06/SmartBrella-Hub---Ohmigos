import 'package:flutter/material.dart';
import '../main.dart'; // 👈 gives access to MainNavigation


class RegistrationPage extends StatefulWidget {
  const RegistrationPage({super.key});

  @override
  RegistrationPageState createState() => RegistrationPageState();
}

class RegistrationPageState extends State<RegistrationPage> {
  final _formKey = GlobalKey<FormState>();

  // Controllers
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _studentIdController = TextEditingController();

  // ================= Form Submission =================
  void _submitForm() {
    if (!_formKey.currentState!.validate()) return;

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text("Login successful!"),
        backgroundColor: Colors.green,
      ),
    );

    // Example navigation after login
    Future.delayed(const Duration(seconds: 1), () {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const MainNavigation()),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFE3F2FD), Color(0xFFBBDEFB)], // light blue tones
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Card(
                elevation: 6,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                color: Colors.white.withOpacity(0.9),
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        // Title
                        const Text(
                          "SmartBrella Hub",
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.blue,
                            letterSpacing: 1.2,
                          ),
                        ),
                        const SizedBox(height: 20),

                        // Logo Image
                        Container(
                          width: 120,
                          height: 120,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            border: Border.all(color: Colors.blue, width: 2),
                          ),
                          child: ClipOval(
                            child: Image.asset(
                              "assets/logo.png",
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                        const SizedBox(height: 20),

// Slogan
                        const Text(
                          "Rain or Shine, We’ve Got You Covered.",
                          style: TextStyle(
                            fontSize: 16,
                            fontStyle: FontStyle.italic,
                            color: Colors.black54,
                          ),
                        ),
                        const Divider(thickness: 1, height: 30),

                        // FULL NAME
                        Align(
                          alignment: Alignment.centerLeft,
                          child: const Text(
                            "FULL NAME",
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                              color: Colors.blue,
                            ),
                          ),
                        ),
                        const SizedBox(height: 5),
                        TextFormField(
                          controller: _nameController,
                          decoration: const InputDecoration(
                            filled: true,
                            fillColor: Color(0xFFF5F9FF),
                            border: OutlineInputBorder(),
                            contentPadding: EdgeInsets.symmetric(
                                horizontal: 10, vertical: 12),
                          ),
                          validator: (value) => value == null || value.isEmpty
                              ? "Please enter your name"
                              : null,
                        ),
                        const SizedBox(height: 15),

                        // STUDENT ID
                        Align(
                          alignment: Alignment.centerLeft,
                          child: const Text(
                            "STUDENT ID",
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                              color: Colors.blue,
                            ),
                          ),
                        ),
                        const SizedBox(height: 5),
                        TextFormField(
                          controller: _studentIdController,
                          decoration: const InputDecoration(
                            filled: true,
                            fillColor: Color(0xFFF5F9FF),
                            border: OutlineInputBorder(),
                            contentPadding: EdgeInsets.symmetric(
                                horizontal: 10, vertical: 12),
                          ),
                          validator: (value) => value == null || value.isEmpty
                              ? "Please enter your student ID"
                              : null,
                        ),
                        const SizedBox(height: 25),

                        // LOGIN Button
                        SizedBox(
                          width: double.infinity,
                          child: ElevatedButton(
                            onPressed: _submitForm,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.blue,
                              padding:
                                  const EdgeInsets.symmetric(vertical: 15),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                              ),
                            ),
                            child: const Text(
                              "LOG IN",
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

// ================= Main Page After Login =================
// class MainPage extends StatelessWidget {
//   const MainPage({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(title: const Text("Main Page")),
//       body: const Center(
//         child: Text(
//           "Welcome to the Main Page!",
//           style: TextStyle(fontSize: 20),
//         ),
//       ),
//     );
//   }
// }