# シナリオデータ（AvScenData.dat）の文字列の翻訳手順

PC用RPG「Avadon: The Black Fortress」の、ゾーン（地域）のデータに入っている文字列を日本語にします。
作業フォルダ: `L:\SteamLibrary\steamapps\common\Avadon The Black Fortress\_jp_mod`（以下 `_jp_mod`）

## 最初に読むもの
1. `_jp_mod\trans\STYLE.md` — 翻訳方針（特に 3章の記号、5章の固有名詞、6章の共通語彙、7章の決定事項）
2. `_jp_mod\trans_scen\jobs\<担当名>.json` — `glossary`（対訳表。**ここにある語は必ずこの訳を使う**）
3. `_jp_mod\trans_scen\chunks\<担当名>.json` — 翻訳する文字列。各要素: `id`、`kind`、`en`（原文）、`max_bytes`（上限。全角1文字＝2バイト、半角1文字＝1バイト）
## 種類ごとの訳し方
| kind | 画面での使われ方 | 訳し方 |
|---|---|---|
| zone name | ゾーン（地域）の名前。地図や移動の画面に出る | 地名。対訳表に従う |
| zone area | その場所に入ったときに出る場所の名前（「Burial Cells」「Keeper's Crypt」） | 体言止めの短い地名・部屋名 |
| zone label | 地図上のラベル（「To Dungeons」「Miranda's Office」） | 体言止めの短い語 |

- **`max_bytes`（39バイト＝全角19文字）を必ず守る**。
- 方角: North＝北、South＝南、East＝東、West＝西。Stairs/Stairway＝階段、Ladder＝はしご、Trapdoor＝落とし戸、Pylon＝転送柱、Portal＝転移門。
- 人名の部屋・家は「〜の部屋」「〜の家」「〜の執務室」など（Miranda's Office →「ミランダの執務室」）。


## 出力と検査
1. `_jp_mod\trans_scen\ja\<担当名>.json` に UTF-8 の JSON で書く（Write ツール）: `{"name0001": "訳", ...}`。キーは `id`。全 `id` を含める。
2. Bash で検査する:
   `cd "/l/SteamLibrary/steamapps/common/Avadon The Black Fortress/_jp_mod" && python -I tools/scen_tool.py check trans_scen <担当名>`
   エラー（E）が0になるまで直す。警告（W）も、訳し忘れや対訳表の不使用なら直す。
3. 最後に、処理件数、残った警告、自分で決めた訳語、判断に迷った箇所（最大5件）を短く報告する。
