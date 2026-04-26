# GLB_DYNAMIC_CANON

## STATE
GLB_REVENUE_FIRST

## GOAL
GLBを収益化する。
まずMaintenance表示を消し、入口ページとTravel Pass導線を完成させる。

## CURRENT_PRIORITY
1. Maintenance表示を全ページで初期非表示にする
2. index.htmlをGLB共通入口に整える
3. index.next.htmlをCore $2.99モードとして整理
4. index.premium.htmlをTravel Pass $14.99説明・購入ページとして整理
5. travel.htmlを購入後の本体UIとして完成
6. Stripe導線を確認する

## URLS
- Entry:
https://nextbase-one-ha.github.io/nextbase-world/index.html

- Core $2.99:
https://nextbase-one-ha.github.io/nextbase-world/index.next.html

- Travel Pass $14.99 LP:
https://nextbase-one-ha.github.io/nextbase-world/index.premium.html

- Travel Pass App:
https://nextbase-one-ha.github.io/nextbase-world/travel.html

## PRODUCT_STRUCTURE
- index.html = 共通入口 / 無料体験 / オンボーディング
- index.next.html = Core $2.99 / 基本翻訳
- index.premium.html = Travel Pass $14.99 / 説明・購入
- travel.html = Travel Pass購入後の本体UI

## PRICING
- Core = $2.99 / 月額
- Travel Pass = $14.99 / 30日買い切り / 自動更新なし
- 旅行が終わればCoreへ戻る思想
- また旅行が決まればTravel Passを買う

## CURRENT_UI_RULE
- 黒背景
- 白太文字
- 細いゴールド枠
- 大きいボタン
- 説明は最小
- 初期画面は迷わせない

## TRAVEL_HTML_RULE
travel.html は説明ページではない。
購入後に使う本体UI。

初期表示:
- 話す / Speak
- 見せる / Show
- 必須カード / Essentials

禁止:
- 小さいボタンだらけ
- 旧UIの初期表示
- Maintenance表示
- Survival / 生存 / 命を守る / 守護 / 聖域 / お守り

## MAINTENANCE_RULE
全ページで maintenance overlay は初期非表示。

対象:
- index.html
- index.next.html
- index.premium.html
- travel.html

必須:
- style="display:none;"
- aria-hidden="true"
- hidden
- maintenance_mode=falseなら表示しない

## WORK_ENVIRONMENT
- Mac = GLB本線
- Windows = 後回し検証用
- Claude = 外部レビュー補助
- Cursor = 実装
- ChatGPT = 正本整理・監査
- NORI-san = 最終判断

## FORBIDDEN
- 古い前提で進めない
- 未確認の完了宣言をしない
- 正本にない作業を始めない
- Mythosを今GLBへ混ぜない
- Windows成果物をMac本線へ混ぜない
- Stripeを勝手に変更しない
- GitHub反映済みと未確認で断定しない

## STATE_CHECK_TEMPLATE
STATE:
GOAL:
BLOCKER:
NEXT_ACTION:
EVIDENCE:
IRREVERSIBLE:
OUTPUT:

## UPDATE_RULE
このファイルは追記ではなく上書き。
古いSTATEは残さない。
現在の正本だけを書く。
