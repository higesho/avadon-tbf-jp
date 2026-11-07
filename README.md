# Avadon: The Black Fortress 日本語化パッチ

Spiderweb Software の RPG「Avadon: The Black Fortress」（Steam 版）を日本語で遊べるようにする非公式パッチです。会話・本・アイテム・画面の文字・地名まで、ゲーム内のほぼすべての文章を日本語にします。

- **紹介ページ**: https://higesho.github.io/avadon-tbf-jp/
- **ダウンロード**: [Releases](https://github.com/higesho/avadon-tbf-jp/releases/latest) の `AvadonTBF_JP_<版>.zip`

![会話画面](docs/img/dialogue.jpg)

## 使い方
1. ZIP の中身（`dsound.dll`、`avadon_jp.ini`、`avadon_jp` フォルダ）をゲームのフォルダ（`Avadon.exe` のある場所）にコピーする
2. Steam からゲームを起動する

元に戻すときは、コピーしたファイルとフォルダを削除します。詳しくは ZIP 内の `avadon_jp/README.txt` か紹介ページを見てください。

動作確認は Steam 版（Windows）で行っています。GOG 版など他のストアの版でも動くように作ってありますが未確認です（対応できない版では日本語化を自動で止め、英語のまま起動します）。ゲームの元のファイルは書き換えません。初回の起動時に DLL が手元のファイルと差分（`avadon_jp/jp_patch.bin`）から日本語版を `avadon_jp/cache/` に作り、ゲームが読むファイルをそちらに差し替えます。

## 翻訳の規模
| 対象 | 件数 |
|---|---|
| 会話・本・イベントの文（スクリプト） | 15,017 |
| 人物・アイテム・能力などの名前 | 1,965 |
| 画面・戦闘メッセージ（実行ファイル内の文字列） | 728 |
| 地名・地図のラベル（シナリオデータ） | 134 |
| 文字入りの画像 | 8 枚 |

## リポジトリの中身
| パス | 内容 |
|---|---|
| `avadon_jp.c`, `dsound.def`, `build.bat` | 日本語表示 DLL（DirectSound の代理 DLL）。VS2022 Build Tools（x86）でビルド |
| `exe_strings.tsv` | 実行ファイル内の文字列の訳（ゲームには `avadon_jp_exe.tsv` として置く） |
| `trans/` | スクリプト本文の訳（`ja/`）、用語集、口調メモ、文体の決まり（`STYLE.md`） |
| `trans_exe/`, `trans_scen/` | 実行ファイルの文字列とシナリオデータの訳 |
| `tools/` | 抽出・検査・組み込み・画像生成・パッチ作成のツール（Python）。`gen_patterns.py` は DLL が書き換える位置を探すためのパターンを作る |
| `dist_src/` | 配布 ZIP の説明書と設定ファイル |
| `docs/` | 紹介ページ（GitHub Pages） |

開発の詳細（DLL のしくみ、調べたアドレス、翻訳の手順）は [DEVELOPMENT.md](DEVELOPMENT.md) にあります。Avernum: Escape From the Pit の日本語化パッチ（[avernum-efp-jp](https://github.com/higesho/avernum-efp-jp)）と同じしくみです。

ゲームから抽出した英語の原文や元の画像は、このリポジトリに含めていません。翻訳を組み込み直すには、お手元のゲームのファイルから `tools/` のスクリプトで抽出してください。

## 配布 ZIP の作り方
```
python -I tools/build_release.py <元のファイルのフォルダ> <日本語化したファイルのフォルダ> <出力先> v0.9.0 https://higesho.github.io/avadon-tbf-jp/
```
`tools/make_patch.py` が元のファイルとの差分（`avadon_jp/jp_patch.bin`）を作ります。文章は差分として翻訳部分だけを、画像は元の画像との差として持つため、ZIP 単体ではゲームの内容を取り出せません。

## 免責
本パッチは非公式のファン翻訳であり、Spiderweb Software とは関係ありません。使用は自己責任でお願いします。Avadon は Spiderweb Software の商標です。
