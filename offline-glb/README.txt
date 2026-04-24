オフラインGLB（Tomori Public v0.2）— glb-noir 取り込み
================================================

元フォルダ: Mac Desktop/オフラインGLB
  - ロジック/index.UI系/*.dart … オフライン翻訳パイプライン（Flutter/Dart）
  - 指示.txt / 備考.txt / ロジックオフライン*.txt … 開発用（リポジトリには含めない）

このディレクトリ（公開してよい範囲）
--------------
dart/          … 上記 Dart 核のコピー（参照用）
trust_boundary.dart … クライアントに載せる層の型（秘密・大表は載せない前提）
glb_tomori_web.js … ブラウザ用。core_pipeline の normalize/post と揃えた薄い層

Web（Core 正本 index.next）では API の前に glbTomoriNormalize を通し、
応答表示前に glbTomoriPostRewrite を通す。

ロジックコード内外装 2.zip
--------------------------
ネストした zip の集合体で、index.UI系 と重複が多い。実体は ロジック/index.UI系 を正とした。

公開しないもの（.gitignore）
--------------------------
- Desktop の「アルゴリズム系」「主力データ」、オンデバイス／翻訳アプリのメモ一式
  … クライアントや GitHub Pages に載せるとコピーされるため、リポジトリに入れない。
- 重いアルゴリズム・辞書・ルーティングの正本はスマイルフレンド（Cloud Run 等）側で
  保持し、クライアントには API 応答だけ渡す想定。

※ ローカル開発用に Desktop からファイルをコピーした場合も、git add されないよう
  リポジトリルートの .gitignore を維持すること。
