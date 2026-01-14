import 'package:firebase_auth/firebase_auth.dart';
import 'api_service.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  Stream<User?> get authStateChanges => _auth.authStateChanges();

  Future<User?> signIn(String email, String password) async {
    final cred = await _auth.signInWithEmailAndPassword(email: email, password: password);
    final user = cred.user;
    
    if (user != null) {
      // Get Firebase ID token and set it in ApiService
      final token = await user.getIdToken();
      if (token != null) {
        ApiService.setToken(token);
        // Call backend login endpoint to sync user
        try {
          await ApiService.login();
        } catch (e) {
          // Log error but don't fail login if backend sync fails
          print('Backend login sync error: $e');
        }
      }
    }
    
    return user;
  }

  Future<User?> register(String email, String password, {String? displayName}) async {
    final cred = await _auth.createUserWithEmailAndPassword(email: email, password: password);
    final user = cred.user;
    if (user != null && displayName != null) {
      await user.updateDisplayName(displayName);
      await user.reload();
    }
    
    // Sync with backend after registration
    if (user != null) {
      final token = await user.getIdToken();
      if (token != null) {
        ApiService.setToken(token);
        try {
          await ApiService.login();
        } catch (e) {
          print('Backend registration sync error: $e');
        }
      }
    }
    
    return user;
  }

  Future<void> sendPasswordReset(String email) async => await _auth.sendPasswordResetEmail(email: email);

  Future<void> signOut() async {
    // Call backend logout first
    try {
      await ApiService.logout();
    } catch (e) {
      print('Backend logout error: $e');
    }
    
    // Then sign out from Firebase
    await _auth.signOut();
  }
}
