# 環境構築
今回はチュートリアル用のシナリオを使用してチュートリアルを行います。

## チュートリアルで使用するマップのダウンロード

{download}`マップのダウンロード <./../../download/tutorial_map.zip>`
をクリックしてダウンロードしてください。

ダウンロードしたファイルを解凍し、中のファイルを `rcrs-server/maps/` の中に移動させてください。

## シュミレーションサーバーの動作確認

```bash
cd WORKING_DIR/rcrs-server/scripts
./start-comprun.sh -m ../maps/tutorial_fire_brigade_only/map -c ../maps/tutorial_fire_brigade_only/config
```

何個かのウィンドウが表示されたら成功です。
コマンドラインで `Ctrl + C` (MacOSの場合は `Command + C` ) を押すとシミュレーションサーバーが終了します。
