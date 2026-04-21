// trust_boundary.dart — クライアントに載せてよい境界の明示（秘密は載せない）
//
// 原則:
// - 正本の辞書・ルート大表・APIキーはサーバ（Smile Friend）または認証後ストアのみ。
// - アプリ内バンドルは「薄いパイプライン + 最小オフライン辞書」まで。丸ごとコピー対策にならないが、
//   「何をクライアントに置かないか」を型で固定する。
// - Web: GLB_CLIENT_DICTIONARY_PUBLIC=false のとき 150k はブラウザに配らない（server.js ROUTES_CSV_PATH）。

/// 翻訳解決がどの層で決まったか（ログ・テレメトリ用。秘密を含まない）。
enum TranslateTrustLayer {
  /// 同一言語など、外部呼び出しなし
  noop,

  /// メモリ / session キャッシュ
  clientCache,

  /// オンデバイス辞書・テンプレ（バンドルまたは sqlite）
  localDictionary,

  /// Smile Friend 上のルート表照合（クライアントは表を持たない）
  serverRouteTable,

  /// サーバメモリキャッシュ（Google 前）
  serverCache,

  /// Cloud Translation 等の外部 API
  externalApi,
}

/// 結果に層を付与できるようにするミキシン（各パイプラインの戻りに optional で載せる想定）。
class TranslateOutcomeMeta {
  const TranslateOutcomeMeta({required this.layer, this.routeType});

  final TranslateTrustLayer layer;

  /// サーバが返す routeType 文字列と対応（任意）
  final String? routeType;
}
