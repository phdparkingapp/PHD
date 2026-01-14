import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'screens/splash/splash_screen.dart';
import 'utils/constants.dart';

import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  try {
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
  } catch (e) {
    print("Firebase init failed: $e");
    // Continue running app even if Firebase fails
  }
  runApp(const HeirsPrivParkApp());
}

class HeirsPrivParkApp extends StatelessWidget {
  const HeirsPrivParkApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'HeirsPrivPark',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: AppColors.primary,
        colorScheme: ColorScheme.fromSeed(seedColor: AppColors.primary),
        useMaterial3: true,
        textTheme: const TextTheme(
          bodyLarge: AppTextStyles.body, // instead of bodyMedium
          labelLarge: AppTextStyles.button,
        ),
      ),
      home: const SplashScreen(),
    );
  }
}
