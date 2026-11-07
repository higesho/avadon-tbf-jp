# exe 内 UI 文字列の翻訳手順

PC用RPG「Avadon: The Black Fortress」の、プログラム（exe）に埋め込まれた UI 文字列を日本語にします。
作業フォルダ: `L:\SteamLibrary\steamapps\common\Avadon The Black Fortress\_jp_mod`（以下 `_jp_mod`）

## 最初に読むもの
1. `_jp_mod\trans\STYLE.md` — 翻訳方針（特に 3章の記号、5章の固有名詞、6章の共通語彙、7章の決定事項）
2. `_jp_mod\trans_exe\jobs\<担当名>.json` — `glossary`（対訳表。必ずこの訳を使う）と `known`（訳し済みの文字列）
3. `_jp_mod\trans_exe\chunks\<担当名>.json` — 翻訳する文字列。各要素:
   - `id`: 文字列のアドレス（出力のキー）
   - `kind`: 使われ方（下表）
   - `en`: 原文。`\n` は改行の記号なので、訳でも同じ位置に `\n` と書く
   - `usage`（あれば）: **この文字列が、ほかの文字列・名前・数値とどうつながって表示されるか**。`[名前など]` `[数値]` は実行時に入る値
   - `specs`（あれば）: 書式指定子（%d、%s など）
   - `max_bytes`（あれば）: 上限バイト数（全角1文字＝2バイト）

## 種類ごとの文体
| kind | 使われ方 | 文体 |
|---|---|---|
| message | 画面下のメッセージ欄 | 常体の短い文（「扉を開けた。」）。「Get Items: 〜」のようなラベルは「アイテム取得: 〜」と半角コロン＋半角スペース |
| sprintf | 書式付き文字列、またはつなぎ合わせる部品 | `usage` を見て決める |
| float | キャラクターの頭上に浮かぶ文字 | 全角19文字以内の短い語（「受け流し！」） |
| draw / label / button / tooltip | 画面のラベル・ボタン・ツールチップ | 体言止めで短く（ボタンは特に短く） |
| tutorial / help / 0x4d2870 など長い説明文 | 画面の説明・チュートリアル | です・ます調 |
| town | 地名 | 対訳表に従う |
| loading | 読み込み画面 | 「〜を読み込み中」 |
| その他 | 内容で判断 | |

**開発者向けのデバッグ文**（"NULL item given to ability engine." "abil_can_target_this_char called prematurely." "script failure: Invalid identifier" のように、プログラムの内部名やエラー内容を述べるもの）は**訳さず、原文をそのままコピー**する。

## 書式指定子（必ず守る）
- `%d` `%s` `%%` などは、**原文と同じ種類・同じ個数**を残す。`%%` は「%」記号の表示。
- 日本語の語順のために順番を入れ替えたいときは、**すべて**を `%1$s` `%2$d` のような順番指定にする（番号は原文での出現順）。通常の `%s` と混ぜない。
  例: 原文 `"%s gives %d gold."` → 訳 `"%1$sは%2$dゴールドをくれた。"`、入れ替えるなら `"%2$dゴールドを%1$sがくれた。"`

## つなぎ合わせる部品（`usage` がある文字列）
- 英語では「名前 + " attacks " + 名前」のように部品をつないで文を作っています。**並び順は変えられない**ので、日本語として自然に読めるよう部品を訳す。
  日本語は「主語 + は/が + 目的語 + を + 動詞」の順なので、多くはそのまま当てはまる:
  - `[名前] + ' overwhelms ' + [名前] + ' with terror.'` → `' overwhelms '`=「は」、`' with terror.'`=「を恐怖で圧倒した。」
  - `[名前] + ' is wounded by spines.'` → 「はトゲで傷ついた。」
  - どうしても語順が合わないときは記号を使う: `[名前A] + ' attacks ' + [名前B] + '. (' + [数値] + '%)'` → `' attacks '`=「の攻撃→」、`'. ('`=「（」、`'%)'`=「%）」
- **同じ部品が複数の `usage` に出てくるときは、すべての並びで自然になる訳にする**（例: `'. ('` は攻撃と状態異常の両方で使われる）。
- 名前のすぐ後ろにつながる部品は、先頭の半角スペースを**取り除いて**、助詞から始める（`' takes no damage.'` → 「にはダメージがない。」）。
  名前の前につながる部品は、末尾の半角スペースを取り除く（`'You gain an item: '` → 「アイテムを得た: 」のように区切りの後のスペースは残してよい）。
- 行頭の字下げ（`'  Costs %d.'` の先頭の2スペース）は残す。
- `usage` に出てくる `None` や、`[数値]` の後ろに何も書かれていない位置には、半角の「.」（ピリオド）が付くことが多い。この「.」は**変えられない**ので、
  「〜の回復: 15.」「〜はレベル5になった.」のように、後ろに「.」が来ても読める形にする（文末を「。」で終えて「。.」とならないよう注意）。
- coins / gold は「ゴールド」。

## 決まっている UI 用語（本文の翻訳と統一）
難易度: カジュアル / ノーマル / ハード / トーメント。
Health: 体力。Vitality: 活力（能力を使うと減る）。Experience: 経験値。Level: レベル。
Strength 筋力 / Dexterity 器用さ / Intelligence 知力 / Endurance 持久力。
Scarab: スカラベ。Codex: コーデックス。Medals: メダル。Pylon: 転送柱。
Inventory: 所持品。Junk Bag: 雑品袋。Quick Use Items: クイック使用アイテム。Quickspell: クイック呪文。
Abilities: 能力。Skills: 技能。Settings: 設定。Journal: 日誌。Quest: クエスト。Save / Load: セーブ / ロード。
クラス名: Blademaster 剣士 / Shadowwalker 影歩き / Shaman 呪術師 / Sorceress 妖術師。

## 出力と検査
1. `_jp_mod\trans_exe\ja\<担当名>.json` に UTF-8 の JSON で書く（Write ツール）: `{"0x5cbddc": "訳", ...}`。キーは `id`。全 `id` を含める。
   原文の `\n` は JSON では `"\\n"` と書く。
2. Bash で検査する:
   `cd "/l/SteamLibrary/steamapps/common/Avadon The Black Fortress/_jp_mod" && python -I tools/check_exe_chunk.py trans_exe <担当名>`
   エラー（E）が0になるまで直す。警告（W）も、訳し忘れや対訳表の不使用なら直す。
3. 最後に、処理件数、残った警告、自分で決めた訳語、判断に迷った箇所（最大5件）を短く報告する。
