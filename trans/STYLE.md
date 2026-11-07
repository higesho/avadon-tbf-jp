# Avadon: The Black Fortress 翻訳スタイルガイド

ダークファンタジーRPGです。戦乱の地「リネウス（Lynaeus）」で、諸国の同盟「盟約（the Pact）」を守る秘密組織の本拠地
「アヴァドン（Avadon）―黒の要塞（The Black Fortress）」に仕える工作員「ハンド（Hand）」が主人公です。
直訳調を避け、日本のPCゲームとして自然に読める日本語にしてください。意味の追加・省略はしないこと。

## 1. 文の種類ごとの文体
| 種類 | 見分け方 | 文体 |
|---|---|---|
| 地の文（描写・ナレーション） | `text`、`lib`、`print_str*`、`set_top_string` などの説明文 | 常体（だ・である）。主語「あなた」は必要なときだけ使い、省略してよい |
| NPCの台詞 | 英文の `_...._` の部分 | 「」で囲む。口調は話し手に合わせる（下記2） |
| 主人公の発言（選択肢） | `question` | 「」で囲む。性別を感じさせない簡潔な常体。例：「なぜ迎えに来なかったんだ？」「詳しく教えてくれ。」 「〜ぞ」「〜ぜ」「〜わ」「〜だな」など性別や癖の強い語尾は避ける |
| 話題名だけの選択肢 | `question` が名詞だけ（"Andrew" など） | 名詞のまま。かぎかっこを付けない |
| ゲームの操作説明 | 英文全体が ( ) で囲まれた文、`textdocs`、`texthints` | です・ます調。( ) は全角（ ）にする |
| クエスト名・実績名・アイテム名など | 名前だけの短い語 | 体言止め。末尾の "." は付けない |
| クエストの説明・コーデックス | `textquests`、`textcodex` の長い文 | 常体 |
| 頭上の吹き出し | `give_char_text_bubble`、`create_text_bubble` | 短い話し言葉。「」は付けない |

英語の "you" は通常、主人公（ハンド一人）を指します（仲間を含めた一行を指すこともある）。訳では「あなた」と書くか、主語を省略します。
主人公の性別はクラスによって決まり、男性の場合も女性の場合もあるので、主人公を指す語は性別に中立にすること（「彼」「彼女」を使わない）。

## 2. NPCの口調
- 話し手の身分・性格・状況に合わせて決め、**同じ人物の口調はファイル全体で統一**すること。
- 目安：
  - 役人・商人・初対面の一般市民：です・ます（一人称「私」）
  - 兵士・ならず者・荒くれ者：ぶっきらぼうな常体（一人称「俺」）
  - 王・公爵・大魔術師・高位の悪魔・タイタン：尊大・威厳のある口調（一人称「余」「我」「私」など）
  - アヴァドンの仲間（ハンド同士）：くだけた常体。同僚なので敬語は使わない（人物ごとの voices に従う）
  - 老人：「〜じゃ」口調は使いすぎない。丁寧な老人は です・ます
  - ゴブリン、オーガ、ラットリングなど：**原文の英語がたどたどしいときだけ**片言（ひらがな多め、簡単な語彙）。原文が流暢なら普通の口調で訳す
- 1ファイルの翻訳を終えたら、出力の `"_voices"` に人物ごとの口調メモを書くこと（後の翻訳で統一に使う）。

## 3. 記号と書式（**必ず守る**）
- 句読点は全角（、。！？）。英数字は半角。和文中に半角スペースを入れない。
- ！や？のあとに文が続くときは全角スペースを1つ入れる（例：「待て！　話を聞け。」）。
- 台詞の最後は句点などを付けてから閉じる（「〜だ。」「〜か？」）。「〜だ」」のように句点を省かない。
- 英語の `_` で囲まれた台詞は「」にする。台詞の中の引用は『』。訳文に `_` を残さない。
- "..." や "…" は「……」（2つ）にする。ダッシュ（" - " や "--"）は「――」にする。
- `|`（強制改行）は、原文と同じ数を同じ位置関係で残す。
- 先頭の `$`（見出しの印）は残す。
- `[N]` は主人公の名前に置き換えて表示される。訳文にも `[N]` をそのまま残す（例：「[N]、よく来た。」）。
- 原文の**先頭と末尾の空白はそのまま残す**（"  is wounded." のような部品は、つなげて表示されるため）。
- `print_named_str` の文は、ゲームが先頭に人物・怪物の名前を付けて表示する（「〈名前〉が応じない。」）。訳は「が」「は」などの助詞から始め、名前の後ろに直接つながる形にする。日本語で始まる場合は名前との間に空白は入らない。
- `code` 欄がある単位は、他の文字列や数値と連結して表示される**部品**です。`code` を見て、
  前後に何（名前・数値）がつながるかを考え、つなげたときに自然な日本語になるように訳すこと。
- `"` と `\` は訳文に使わない（スクリプトの文法を壊すため）。

## 4. 長さの制限（全角1文字＝2バイト、半角1文字＝1バイト）
| 種類 | 上限 |
|---|---|
| 1つの文字列すべて | 全角255文字（510バイト）。`max` 欄があればその文字数以内 |
| `cr_name`、`set_name`、`set_personality_name`、`ab_name`、`ob_name` | 全角9文字（19バイト） |
| `it_name` | 全角12文字（25バイト） |
| `give_char_text_bubble`、`create_text_bubble` | 全角19文字（39バイト） |
制限を超えそうなときは、意味を保ったまま言い換えて短くすること（略語・体言止めなど）。

## 5. 固有名詞と用語
- **対訳表（glossary.json）にある語は、必ず対訳表の訳を使う。**活用形（所有格の 's、複数形）も同じ訳にする。
- 対訳表にない人名・地名は英語読みのカタカナにする。V は「ヴ」で表す。
- 意味のある名前（Black Fortress、Beast's Woods、Honored Forge など）は意訳する。
- 称号の位置：原則として名前の後（Duke Gryfyn →「グリフィン公」、Captain Johnson →「ジョンソン隊長」、King Micah →「マイカ王」）。
- アヴァドンの役職は名前の前に「〜の」でつける：Hand Gavin →「ハンドのギャヴィン」、Heart Miranda →「ハートのミランダ」、Eye Shima →「アイのシマ」。
- 主な用語（対訳表より優先度が低いが、対訳表にないときはこれに従う）：
  - Avadon アヴァドン / the Black Fortress 黒の要塞 / the Pact 盟約 / Lynaeus リネウス
  - Hand ハンド（アヴァドンの工作員） / Eye アイ（密偵） / Heart ハート（幹部） / Keeper 番人（Keeper of Avadon アヴァドンの番人）
  - Farlands ファーランド / Farlander ファーランド人 / Titan タイタン / Wayfarer ウェイファーラー
  - クラス名: Blademaster 剣士 / Shadowwalker 影歩き / Shaman 呪術師 / Sorceress 妖術師（NPC の肩書きも同じ: Shaman Romy →「呪術師のロミー」）

## 6. 共通語彙（名前の部品。対訳表に個別の語がなければこれに従う）
- 職業・役割: Soldier 兵士 / Warrior 戦士 / Rebel 反逆者 / Sorcerer 妖術師 / Mage 魔術師 / Priest 司祭 / Shaman 呪術師 /
  Guard 衛兵 / Captain 隊長 / Mayor 町長 / Merchant 商人 / Smith 鍛冶屋 / Bandit 山賊 / Rogue ならず者 / Cultist 教団員 / Archmage 大魔術師
  （Shaman は Avadon ではクラス名と同じ「呪術師」、Sorceress は「妖術師」）
- 種族・怪物: Goblin ゴブリン / Ogre オーガ / Troll トロール / Giant 巨人 / Human 人間 / Drake ドレイク / Dragon ドラゴン / Imp 小鬼 /
  Demon デーモン / Golem ゴーレム / Skeleton 骸骨 / Zombie ゾンビ / Ghoul グール / Ghost ゴースト / Shade 亡霊 / Wraith レイス /
  Spirit 霊 / Elemental 精霊 / Bat コウモリ / Rat ネズミ / Ratling ラットリング / Lizard トカゲ / Spider 蜘蛛 / Beetle 甲虫 /
  Slime スライム / Fungus 菌 / Worm 蠕虫 / Serpent 大蛇 / Wolf 狼 / Bear 熊 / Lord 君主 / Queen 女王 / King 王
- 武器: Sword 剣 / Broadsword ブロードソード / Dagger 短剣 / Knife ナイフ / Spear 槍 / Halberd ハルバード / Mace メイス / Axe 斧 /
  Hammer ハンマー / Staff 杖 / Wand ワンド / Rod ロッド / Bow 弓 / Arrows 矢 / Javelins 投げ槍 / Darts ダーツ / Razordisks 円月刃
- 防具・装身具: Armor 鎧 / Chain Mail 鎖帷子 / Breastplate 胸当て / Plate 板金鎧 / Robes ローブ / Cloak 外套 / Shield 盾 /
  Buckler 小盾 / Helm 兜 / Cap 帽子 / Boots ブーツ / Gauntlets 籠手 / Gloves 手袋 / Belt ベルト / Ring 指輪 / Amulet 護符 /
  Necklace 首飾り / Bracelet 腕輪 / Band 腕輪 / Pendant ペンダント / Charm お守り
- 場所・設備: Fortress 要塞 / Fort 砦 / Cave 洞窟 / Tunnel トンネル / Gate 門 / Tower 塔 / Castle 城 / Keep 城塞 / Woods 森 / Stead 集落 / Pub 酒場 / Inn 宿屋
- 消耗品・素材: Potion 薬 / Elixir 霊薬 / Brew 薬 / Herbs 薬草 / Scroll 巻物 / Crystal 水晶 / Gem 宝石 / Pelt 毛皮 / Skin 皮 /
  Fang 牙 / Ichor 体液 / Key 鍵 / Book 本 / Spellbook 呪文書 / Note メモ / Letter 手紙
- 形容: Iron 鉄の / Steel 鋼の / Bronze 青銅の / Silver 銀の / Gold 金の / Magic 魔法の / Enchanted 魔力を帯びた /
  Blessed 祝福の / Cursed 呪われた / Fine 上質の / Rusty 錆びた / Giant 巨大 / Huge 巨大 / Minor 小 / Major 大

## 7. 個別の決定事項（作業中に決めたもの）
- 所持金の coins / gold は「ゴールド」（数字は半角）。
- 盟約などの軍の部隊・階級: Blade「十人隊」/ Watcher「十人長」/ Lance「百人隊」/ Monitor「百人長」（役職は名前の後ろ: Monitor Shigaz →「シガズ百人長」）。
  武器としての blade は「刃」、lance は「ランス」。
- 蜘蛛の Widow は「ゴケグモ」。難易度名は「カジュアル」「ノーマル」「ハード」「トーメント」。
- the Master of Avadon は「アヴァドンの主」（Keeper は「番人」）。
- 長さの単位は原文どおり（feet →「フィート」、miles →「マイル」）。メートルに換算しない。
- 台詞のあとに操作説明が続く選択肢（_I have the book._ (Give it to her.)）は「本を持っている。」（彼女に渡す。）の形にする。
- 「Open Door:」のようなメッセージ冒頭のラベルは「扉を開ける: 」のように半角コロン＋半角スペースで区切る（ラベルの区切りだけの例外）。
- クレジットの人名一覧は英字の原文のまま残す。
- 主人公が「Tell me more.」と言う選択肢は「詳しく教えてくれ。」で統一。
- UI 用語: Health 体力 / Vitality 活力 / Experience 経験値 / Scarab スカラベ / Codex コーデックス / Medals メダル /
  Pylon 転送柱 / Inventory 所持品 / Junk Bag 雑品袋 / Quick Use クイック使用 / Quickspell クイック呪文 /
  Specialization 特化 / Respec リスペック / Resistances 耐性 / Lockpick 解錠具。ゲーム名は『アヴァドン：黒の要塞』。
- 仲間の一人称: シマ「俺」、セヴィリン「俺」、ジェネル「私」、ナタリー「私」（voices.json に従う）。ウェイファーラーは主人公を「あなた」と呼ぶ。
