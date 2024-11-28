# クイックスタート

## 前提条件

インストールする前に、以下の前提条件を確認してください：

- Python 3.12 以上
- pip

## パッケージのインストール

パッケージをインストールするには、次のコマンドを実行します：

```bash
pip install adf_core_python
```

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

## エージェントを実行する

エージェントを実行するには、シミュレーションサーバーを起動し、次のコマンドを実行します：

```bash
python main.py
```

エージェントの実行が開始され、シミュレーションサーバーとの通信が開始されます。
