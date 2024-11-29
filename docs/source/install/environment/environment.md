# 環境構築
adf-core-pythonをインストールするには以下の必要条件が必要です。
既にお使いのPCにインストールされている場合は再度インストールする必要はありません。

## 必要条件

- Git
- Python 3.12 以上
- OpenJDK 17

各OSでのインストール方法は以下のページをそれぞれ参照してください

[Windowsでの必要条件のインストール方法](./windows/install.md)

[MacOSでの必要条件のインストール方法](./mac/install.md)

[Linuxでの必要条件のインストール方法](./linux/install.md)

## シミュレーションサーバーのインストール
次にRoboCup Rescue Simulationのシミュレーションサーバーをインストールします。

```{note}
WORKING_DIR は任意のディレクトリを作成、指定してください。
```

```bash
mkdir WORKING_DIR
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

![シミュレーションサーバーの起動](../../images/launch_server.png)

上記のように何個かのウィンドウが表示されたら成功です。
コマンドラインで `Ctrl + C`  (MacOSの場合は `Command + C` )  を押すとシミュレーションサーバーが終了します。
