# 対訳表（用語集）の翻訳手順

PC用RPG「Avadon: The Black Fortress」の固有名詞・用語の対訳表を作ります。
作業フォルダ: `L:\SteamLibrary\steamapps\common\Avadon The Black Fortress\_jp_mod`（以下 `_jp_mod`）

## 読むもの
1. `_jp_mod\trans\STYLE.md` — 翻訳方針（特に 5. 固有名詞と用語、6. 共通語彙、4. 長さの制限）
2. `_jp_mod\trans\gloss_in\<担当名>.json` — 訳す語の一覧。各要素:
   - `en`: 英語の語
   - `cat`: 種類（creature / person / item / ability / object / skill / quest title / term in text など）
   - `example`: 使用例の文（`cat` が名前欄のときはファイル名）
   - `max_bytes`（あれば）: 訳の上限バイト数（全角1文字＝2バイト、半角＝1バイト）。19 なら全角9文字、25 なら全角12文字まで
3. `_jp_mod\trans\gloss_out\core.json`（あれば） — 既に決まった主要語の訳。**ここにある語の訳と矛盾しないこと**
   （例: core で Gryfyn =「グリフィン」なら、Duke Gryfyn は「グリフィン公」、Gryfyn's Guard は「グリフィンの衛兵」）。

## 方針
- 人名・地名は英語読みのカタカナ。意味のある名前は意訳する（Beast's Woods →「獣の森」）。
- 複合語は部品の訳をそろえる（同じ担当の中でも、core とも）。
- 称号・役職の位置は STYLE.md 5 に従う（Duke Gryfyn →「グリフィン公」、Hand Gavin →「ハンドのギャヴィン」）。
- アイテム・能力・怪物の名前は、ゲームらしい簡潔な日本語。`max_bytes` を必ず守る（超えるなら言い換えて短く）。
- 一般的な英単語（Level、Council など）は文脈に合う日本語にする。
- 判断できない語も必ず何か訳を付ける。
- 決定済みの訳語: 蜘蛛の Widow は「ゴケグモ」（Cave Widow →「洞窟ゴケグモ」）。盟約・ケレムなどの軍の部隊・階級は
  Blade「十人隊」/ Watcher「十人長」/ Lance「百人隊」/ Monitor「百人長」（役職名は名前の後ろ: Watcher Zaren →「ザレン十人長」）。
  ただし武器の Lance（Seeking Lance など）は「ランス」。

## 出力
`_jp_mod\trans\gloss_out\<担当名>.json` に、入力と同じ順番で UTF-8 の JSON を書く（Write ツール）:
```json
[
{"en": "Avadon", "ja": "アヴァドン", "keep": true},
{"en": "Hand of Avadon", "ja": "アヴァドンのハンド", "keep": true}
]
```
- 入力のすべての語を含めること。`keep` は常に true。訳に `"` と `\` を使わない。

## 最後に
処理した語数と、判断に迷った語（最大10件、英語→訳と理由）を短く報告する。
