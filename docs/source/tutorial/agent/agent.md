# エージェントの作成

このセクションでは、`adf-core-python` ライブラリの使用方法の概要を提供します。

## 新規エージェントの作成

新規エージェントを作成するには、次のコマンドを実行します：

```bash
adf-core-python
```

実行すると、下記のような対話形式のプロンプトが表示されます：

```bash
Your agent team name: my-agent
Creating a new agent team with name: my-agent
```

入力後、下記のようなエージェントのテンプレートがカレントディレクトリに作成されます。

```bash
.
└── my-agent
    ├── config
    │   ├── development.json
    │   ├── launcher.yaml
    │   └── module.yaml
    ├── main.py
    └── src
        └── my-agent
            ├── __init__.py
            └── module
                ├── __init__.py
                └── complex
                    ├── __init__.py
                    ├── sample_human_detector.py
                    ├── sample_road_detector.py
                    └── sample_search.py
```

## シミュレーションを実行する

ターミナルを2つ起動します。

片方のターミナルを開き、シミュレーションサーバーを以下のコマンドで起動します：

```bash
# Terminal A
cd WORKING_DIR/rcrs-server/scripts
./start-comprun.sh -m ../maps/tutorial_fire_brigade_only/map -c ../maps/tutorial_fire_brigade_only/config
```

その後、別のターミナルを開き、エージェントを起動します：

```bash
# Terminal B
cd WORKING_DIR/my-agent
python main.py
```

エージェントが正常に起動すると、シミュレーションサーバーに接続され、エージェントがシミュレーションに参加し、エージェントが動き出します。
途中で止めたい場合は、それぞれのコマンドラインで `Ctrl + C` (MacOSの場合は `Command + C` ) を押してください。

```{warning}
シミュレーションサーバーを停止させたあとは、プロセスが残ってしまう場合があるので`./kill.sh` を実行してください。
```
