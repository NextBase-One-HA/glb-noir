# GLB_DYNAMIC_CANON

## STATE
GLB_REVENUE_FIRST / PROTECTED_ARCHITECTURE

## GOAL
収益化と同時に、内部ロジック（0円・辞書・API削減）を完全にブラックボックス化し、外部から推測不可能な構造を維持する。

## DISCLOSURE_POLICY

### 外に出すもの（公開OK）
- 翻訳結果（Friendレイヤー）
- UI（Speak / Show / Travel体験）
- 価格（$0 / $2.99 / $14.99）
- 機能説明（音声・翻訳・旅行モード）
- 「オフラインでも一部使える」などの体験表現

### 絶対に出さないもの（非公開）
- 0円ロジックの具体条件
- API削減ロジックの優先順位
- 辞書ヒット判定アルゴリズム
- キャッシュ構造
- pivot翻訳ロジック
- Smile Friend Engineの内部仕様
- 課金状態判定の仕組み
- localStorageキー設計

→ ユーザーには一切見せない
→ Dev以外には説明しない

## ZERO_YEN_PROTECTION

目的:
- 価値体験は提供
- 仕組みは隠す

実装原則:
- 回数制限はUIに直接出さない（曖昧表示）
- 日次リセットは内部処理のみ
- 判定は分散（単一条件にしない）
- Core誘導は自然文で行う

禁止:
- 固定回数の明示
- カウントUI表示
- ロジック説明

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
- "オフラインでも使える"

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
として提供する

ロジックは全て裏に隠す

## UPDATE_RULE
このファイルは上書き更新のみ
