# CURSOR_SYNC_PROTOCOL

STATE:
Mac = production mainline
Windows = isolated verification

Mac owns:
- travel.html
- index.html
- index.next.html
- index.premium.html
- Stripe links
- GitHub Pages release
- GLB production fixes

Windows owns:
- smile_friend/mythos_overmatch/
- mythos_generation_canonical
- attack scenarios
- test harness
- verification logs

Forbidden:
- Windows must not edit travel.html
- Windows must not edit index.next.html
- Windows must not edit index.premium.html
- Windows must not push production UI changes
- Gemini and Cursor must not directly connect

Sync flow:
1. Windows runs isolated tests
2. Windows outputs raw logs
3. GPT Tomori audits logs
4. NORI-san approves
5. Mac re-implements approved design if needed
6. Mac pushes production changes

Required Windows report:
- git status --short
- git diff --stat HEAD
- unittest result
- forbidden term search
- production non-interference diff

Required Mac report:
- git status --short
- release files changed
- launch readiness
- production URL check
- Stripe URL check

Final authority:
NORI-san
