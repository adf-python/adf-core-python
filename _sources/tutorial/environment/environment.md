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

## シュミレーションサーバーの動作確認

```bash
cd WORKING_DIR/rcrs-server/scripts
./start-comprun.sh -m ../maps/test/map -c ../maps/test/config
```

何個かのウィンドウが表示されたら成功です。
コマンドラインで `Ctrl + C` を押すとシミュレーションサーバーが終了します。
