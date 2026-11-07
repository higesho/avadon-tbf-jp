# Avadon: The Black Fortress 日本語化MOD（開発メモ）

Avernum: Escape From the Pit の日本語化MOD（`..\..\Avernum Escape From the Pit\_jp_mod`）を移植したものです。
エンジンは同じですが exe のコードは別物なので、フック位置はすべて調べ直しました。

## 仕組み
- `dsound.dll`（ゲームフォルダに置く）が起動時に読み込まれ、`Avadon.exe` の
  「枠内にテキストを描く関数」(VA 0x46e080) と「文字列の幅を測る関数」(0x46df00) を自前の実装に差し替えます。
- テキストは EUC-JP（既定）として解釈します。英数字はゲーム内フォント（`G290.png`）で、日本語は Windows のフォント
  （既定: メイリオ）で文字画像を作り、ゲーム本来の描画関数（0x4079d0）で描きます。
- `[N]`（主人公の名前）の置き換えは、ゲームの関数 0x46ede0 を DLL から呼んで行います。
- `Avadon.exe` は DSOUND.dll を序数 1（DirectSoundCreate）で読み込むので、`dsound.def` で序数 1 を出します。

## ビルドと起動
1. `build.bat` で `dsound.dll` をビルドする（VS2022 Build Tools, x86）
2. `dsound.dll` をゲームフォルダ（Avadon.exe と同じ場所）にコピーする
3. Steam から起動する（`steam://rungameid/112100`）
ログは `avadon_jp/avadon_jp.log`。設定は `avadon_jp.ini`（Avernum 版と同じ項目）。

## 調べてわかったこと（Steam 版、ASLR の影響を除いた VA）
| VA | 内容 |
|---|---|
| 0x46e080 | 枠内テキスト描画（ecx=モード 0:折返し/1:中央/2:1行、cdecl: 文字列, フォントコード, r, g, b, rect{top,left}, rect{bottom,right}）。Avernum と違い、矩形の補正処理はない。512バイト以上の文字列は描かない（DLL では制限なし） |
| 0x46df00 | フォント0での文字列の幅（edx=文字列、戻り値 ax）。現在のフォントをフォント0に変える |
| 0x46ede0 | `[N]` を主人公の名前に置き換える（ecx=バッファ、内部で0x404バイトの作業領域を境界チェックなしで使う） |
| 0x470290 | ASCII 1行描画（cdecl: str, r, g, b。描画位置は 0x6bf32c(x)/0x6bf330(y)） |
| 0x4704a0 | 文字位置の計算（edx=文字列、push 位置配列） |
| 0x4079d0 | テクスチャ矩形の描画（cdecl: テクスチャオブジェクト, 1, 0, 0, src1, src2, dst1, dst2） |
| 0x5c30b0 + n*0x310 | フォント5種の字形テーブル（コード12/15/14/16/24） |
| 0x5c4008 | 文字→字形番号の変換表（short[256]） |
| 0x6bf324 | フォントのテクスチャオブジェクトへのポインタ（構造は Avernum と同じ: 0x170バイト、+0x2c=GL ID） |
| 0x5c308c | 現在バインド中の GL テクスチャのキャッシュ |
| 0x5d078c/90/94 | 描画色 r/g/b（float、値/31） |
| 0x458b9a | スクリプト読み込み時の字句数見積もりの文字分類（DLL が 0x80 以上を英字扱いにする） |
| 0x464b35 | print_named_str の sprintf("%s %s")（DLL が日本語のとき空白を入れない） |
| 0x4a8955 | sprintf |
| 0x459ca4 | スクリプトの文字列リテラルの上限 0x1ff（510バイト）。Avernum と同じ |

## AvScenData.dat
- 先頭 0x1168 バイトがヘッダ（ゾーン名: +4 から 0x2c バイトおき、名前欄 0x28）。
- 続いてゾーン 24 個（各 0x3d42c バイト）。地図のラベルが +0x16054 から 10 個（0x28 バイトおき）、
  エリア名が +0x2c24c から 10 個（0x28 バイトおき）。いずれも 39 バイトまで。
- `tools/scen_extract.py`、`tools/scen_tool.py`

## exe 内の UI 文字列
- `tools/exe_extract.py Avadon.exe exe_strings.tsv` で、ゲーム本体の文字列（.rdata 0x5a5d80〜0x5b06f8）を抽出する。
  `sink` 列は文字列を受け取る関数から付けた使われ方（float = 頭上の文字 39 バイトまで、internal = 訳さない）。
- `tools/exe_fragctx.py` で、部品をつなぐメッセージ（0x46ddb0 / 0x46de30: [ebp+8]+ecx+edx+esi+数値+[ebp+0xc]）の組み立て順を出す。

## 本文の翻訳
手順は Avernum 版の TRANSLATION.md と同じ。違い:
- `tools/make_jobs.py` で、チャンクを約3万字の担当にまとめ、陣（並列に走らせる単位）に割り振る。大きなファイルは
  複数の担当に分け、続きは必ず後の陣に回す（口調メモを引き継ぐため）。
- `tools/prep_job.py` の口調メモの照合を修正（Avernum 版は日本語名で英文を探していたため、口調メモが渡っていなかった）。
- `trans/GLOSS_BRIEF.md` が用語集の翻訳手順。

## 配布
- `tools/build_release.py <元のファイルのフォルダ> <日本語化したフォルダ> dist v0.9.0 https://higesho.github.io/avadon-tbf-jp/`
  で `dist/AvadonTBF_JP_<版>.zip` を作る（どちらも「Avadon Files/...」の形のフォルダ）。中身は dsound.dll、avadon_jp.ini、
  avadon_jp/jp_patch.bin（`tools/make_patch.py` の差分）、avadon_jp/avadon_jp_exe.tsv、avadon_jp/README.txt。
- 日本語化したファイルは、`build_scripts.py` などの出力先をゲームフォルダの代わりにした作業フォルダに作ってもよい。
  ゲームフォルダの元ファイルは英語版のままにしておく（DLL が起動時に差分を当てて avadon_jp/cache に作る）。

## 試験
- `_backup_original/` に元の Scripts、AvScenData.dat、Graphics Core の画像8枚がある。
- computer-use では「Avadon The Black Fortress」と「avadon.exe」の両方の許可が要る。クリックは
  マウスを押して 0.2 秒待って離す（普通のクリックは無視される）。起動ダイアログで「Play Game in Window」、1280x800。

## 状況（2026-11-08）
- スクリプト本文は全訳済み（465チャンク・15,017件、名前欄1,965件、検査エラー0）。Haiku の担当61本で翻訳し、Opus が点検。
- exe の UI 文字列 728件（うち職業名4件は .data の固定長配列に直接書き込む: `exe_strings.tsv` の sink `inplace20`）、
  AvScenData.dat の地名・ラベル134件、画像8枚（G158 タイトル、G203 メニュー、G220、G189、G167、G169、G128、G133）。
- 仕上げの順番: `tools/polish.py trans` → `tools/unify_dupes.py trans`（英文と種類（選択肢・吹き出し・その他）ごとに統一）→
  `tools/check_trans.py trans` → `tools/build_scripts.py ../_backup_original/Scripts trans "../Avadon Files/Scripts"`。
- exe: `tools/exe_merge.py exe_strings.tsv trans_exe` → `tools/check_exe_strings.py exe_strings.tsv ../avadon_jp`
  （`trans_exe/ja/zz_manual.json` は手で足した訳）。地名: `tools/scen_tool.py build trans_scen ../_backup_original/AvScenData.dat "../Avadon Files/AvScenData.dat"`。
  画像: `tools/make_images.py "../_backup_original/Graphics Core" img_out img_preview` → `img_out/*` を `Avadon Files/Graphics Core` へ。
- ゲーム内で確認済み: タイトル、キャラクター作成、難易度選択、導入スライド、チュートリアル、最初の会話。
- 配布用パッチ v0.9.0 を作成（262ファイルの差分、ZIP 約2.5MB）。ゲームフォルダを英語版に戻し、ZIP の中身だけを入れた状態で
  タイトル、キャラクター作成、難易度選択、導入、ゲーム画面の日本語表示を確認（ログ: data files: 262 translated）。
- 未確認: メダル画面・読み込み画面の挿絵など、通しプレイでの確認。
