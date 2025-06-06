class UserProfile {
  final String? vGrade;
  final double? height;
  final double? weight;
  final bool shareInfo;

  UserProfile({
    required this.vGrade,
    required this.height,
    required this.weight,
    required this.shareInfo,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      vGrade: json['v_grade'],    // Dart will automatically treat it as a nullable String?
      height: (json['height'] as num?)?.toDouble(),
      weight: (json['weight'] as num?)?.toDouble(),
      shareInfo: json['share_info'] ?? false,
    );
  }
}
