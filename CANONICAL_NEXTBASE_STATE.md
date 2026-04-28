# NEXTBASE CANONICAL STATE (LATEST)

## GOAL
GLBを“迷わず使える導線”で公開し、2.99課金が成立する状態を維持する。

## CURRENT FLOW (LOCKED)
index.html → index.next.html → 2.99 modal → Stripe → index.2.99.html

## HARD RULES
- 2.99は必ずmodal経由（直リンク禁止）
- 14.99はindex.premium.htmlのみ
- 未課金はpremium侵入不可
- travel.html参照禁止

## USER EXPERIENCE CORE
- 1秒理解
- 迷いゼロ
- 恐怖ゼロ（自動更新なし明示）

## SYSTEM STRUCTURE
Smile = entry (index.html)
Core = processing (index.next / 2.99)
Friend = output (travel / UI)

## DO NOT EXPOSE
- NE
- layer structure
- optimization logic

## NEXT PHASE
- Travel phrases強化
- Emergency即表示

## STATUS
PR #1 merged
Flow stable
Ready for first user validation
