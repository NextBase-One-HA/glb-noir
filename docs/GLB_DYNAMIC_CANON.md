# GLB_DYNAMIC_CANON

## STATE
GLB_REVENUE_FIRST / PROTECTED_ARCHITECTURE / FEATURE_REDUCTION

## GOAL
GLBを公開可能な収益プロダクトとして仕上げる。
内部ロジック（無料枠・辞書・API削減）はブラックボックス化し、公開UIは初見5秒で理解できる状態まで削る。

## DISCLOSURE_POLICY

### 外に出すもの（公開OK）
- 翻訳結果（Friendレイヤー）
- UI（Speak / Show / Travel体験）
- 価格（Free / $2.99 / $14.99）
- 機能説明（音声・翻訳・旅行モード）
- 「無料で1日10回試せる」
- 「オフラインでも一部使える」などの体験表現

### 絶対に出さないもの（非公開）
- 無料枠の内部判定ロジック
- API削減ロジックの優先順位
- 辞書ヒット判定アルゴリズム
- キャッシュ構造
- pivot翻訳ロジック
- Smile Friend Engineの内部仕様
- 課金状態判定の仕組み
- localStorageキー設計

→ ユーザーには体験と条件だけ見せる
→ 内部実装はDev以外には説明しない

## FREE_TRIAL_RULE

公開仕様:
- 無料枠は1日10回翻訳
- 表現は「無料で1日10回試せます」に統一

内部仕様:
- 日次回数判定は内部処理
- 判定方法、保存場所、リセット方法は非公開
- Core誘導は自然文で行う

禁止:
- 内部キー名の露出
- 判定コードの説明
- API削減と無料枠の関係説明

## FEATURE_REDUCTION_RULE

公開前は機能を増やさない。
出すために削る。
初見ユーザーが5秒で理解できない機能は後回し。

### 残す機能
index.html:
- 無料で1日10回翻訳
- Core $2.99
- Travel Pass $14.99
- 価格導線

index.next.html:
- 翻訳入力
- 翻訳結果
- 言語選択
- 音声/TTS
- Core購入導線
- Travel Pass導線

travel.html:
- 話す / Speak
- 見せる / Show
- 必須カード / Essentials
- 戻る

### 後回し・削ってよい機能
- Stats
- Referral
- Share
- 過剰な履歴
- Scene prediction
- 複雑なタブ
- 多すぎる小ボタン
- 説明しすぎるブロック
- 過剰アニメーション

## API_REDUCTION_PROTECTION

公開表現:
- "高速翻訳"
- "一部オフライン対応"

内部実態（非公開）:
- 辞書 → キャッシュ → API の優先順
- 完全一致 / 近似一致ロジック
- セッションキャッシュキー

ルール:
- APIを呼ばない理由はUIに出さない
- 速度は"速い"で統一

## ON_DEVICE_ABSTRACTION

公開:
- "オフラインでも一部使える"

非公開:
- 辞書構造
- カテゴリ設計
- phrase優先処理

## SMILE_FRIEND_RULE

- 出口は常にFriend
- 内部処理は完全遮断

NG:
- 内部処理の説明

OK:
- ユーザーに伝わる表現のみ

## FINAL_RULE

GLBは
"考えなくていい体験"
として提供する。

公開するのは価値、条件、価格、使い方。
隠すのは内部ロジック、原価構造、API削減、辞書、キャッシュ、判定処理。

公開前は足さない。
迷わせるものは削る。

## UPDATE_RULE
このファイルは上書き更新のみ。
