150k.csv（ルート辞書）
====================

- 形式: source,target,from,to（1行1エントリ）。Web の tryLocalRoute / サーバ tryServerRoute と同一キー。

公開サイトでの扱い（2026-04 以降）
----------------------------------
- index*.html は既定で GLB_CLIENT_DICTIONARY_PUBLIC=false のため、GitHub Pages 上では
  このファイルをブラウザが読みにいかない。辞書の「丸ごとコピー」リスクを下げるため。
- 照合は Smile Friend（ne-mode-server）の環境変数 ROUTES_CSV_PATH でサーバに載せた CSV が正本。

ローカル開発
------------
- ブラウザで従来どおりクライアントに 150k を載せたい場合: DevTools で
    localStorage.setItem('glb_dev_csv', '1')
  を実行してからリロード。

リポジトリに 150k を残すか
-------------------------
- 公開リポジトリに含めるとクローンは可能。完全に隠すには private リポジトリ・
  別バケット配布・CI のみでイメージに焼く、に移行してください。
