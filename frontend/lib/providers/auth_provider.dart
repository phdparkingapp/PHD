import 'dart:async';
import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../services/api_service.dart';
import '../models/app_user.dart';

class AuthProvider extends ChangeNotifier {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  User? firebaseUser;
  AppUser? appUser;
  StreamSubscription<User?>? _sub;
  bool loading = true;

  AuthProvider() {
    _sub = _auth.authStateChanges().listen((u) => _onAuthChanged(u));
  }

  Future<void> _onAuthChanged(User? u) async {
    firebaseUser = u;
    if (u != null) {
      // Get Firebase ID token and set it in ApiService
      try {
        final token = await u.getIdToken();
        if (token != null) {
          ApiService.setToken(token);
        }
        
        // Call backend login to sync/retrieve profile
        final data = await ApiService.login();
        appUser = AppUser.fromJson(data);
      } catch (e) {
        appUser = null;
        debugPrint("Backend login error: $e");
      }
    } else {
      appUser = null;
    }
    loading = false;
    notifyListeners();
  }

  Future<void> disposeProvider() async {
    await _sub?.cancel();
  }

  // helper to force refresh token + backend sync
  Future<void> refreshBackendProfile() async {
    if (firebaseUser == null) return;
    final token = await firebaseUser!.getIdToken();
    if (token != null) {
      ApiService.setToken(token);
    }
    final data = await ApiService.login();
    appUser = AppUser.fromJson(data);
    notifyListeners();
  }
}
