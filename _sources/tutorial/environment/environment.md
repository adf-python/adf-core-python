# 環境構築

## 必要なもの

- Git
- Python 3.12 以上
- OpenJDK 17

[Windowsでの必要なもののインストール方法](./windows/install.md)

## シミュレーションサーバーのインストール

```{note}
WORKING_DIR は任意のディレクトリを指定してください。
```

```bash
cd WORKING_DIR
git clone https://github.com/roborescue/rcrs-server.git
cd rcrs-server
./gradlew completeBuild
```

ビルドした際に以下のようなメッセージが表示されたら成功です。

```bash
BUILD SUCCESSFUL in ...
```

## チュートリアルで使用するマップのダウンロード

{download}`マップのダウンロード <./../../download/tutorial_map.zip>`
をクリックしてダウンロードしてください。

ダウンロードしたファイルを解凍し、中のファイルを `WORKING_DIR/rcrs-server/maps/` の中に移動させてください。

## シュミレーションサーバーの動作確認

```bash
cd WORKING_DIR/rcrs-server/scripts
./start-comprun.sh -m ../maps/tutorial_fire_brigade_only/map -c ../maps/tutorial_fire_brigade_only/config
```

何個かのウィンドウが表示されたら成功です。
コマンドラインで `Ctrl + C` を押すとシミュレーションサーバーが終了します。
