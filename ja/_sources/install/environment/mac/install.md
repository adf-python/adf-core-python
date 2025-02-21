# Macでの環境構築
## 1. Homebrewのインストール
1. Terminalを起動し、以下のコマンドを実行します。
    ```bash
    brew -v
    ```

2. もし、`command not found`などのエラーが出た場合、以下のコマンドを実行します。
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

3. もう一度、以下のコマンドを実行してバージョンが表示されたら成功です。(表示されない方はTerminalを再起動してください)
    ```bash
    brew -v
    ```

## 2. Gitのインストール

1. Terminalを起動し、以下のコマンドを実行します。
    ```bash
    git --version
    ```
2. もし、`command not found`などのエラーが出た場合、以下のコマンドを実行します。
    ```bash
    brew install git
    ```
3. 以下のコマンドを入力し、バージョンが表示されたら成功です。(表示されない方はTerminalを再起動してください)
    ```bash
    git --version
    ```

## 3. Pythonのインストール

1. Terminalを起動し、以下のコマンドを実行します。また、バージョンが3.12以上になっていることを確認します。
    ```bash
    python --version
    ```
2. もし、`command not found`などのエラーが出た場合やバージョンが低い場合、以下のコマンドを実行します。
    ```bash
    brew install python
    ```
3. 以下のコマンドを入力し、バージョンが表示されたら成功です。(表示されない方はTerminalを再起動してください)
    ```bash
    python --version
    ```

## 3. OpenJDKのインストール

1. Terminalを起動し、以下のコマンドを実行します。また、バージョンが17になっていることを確認します。
    ```bash
    java --version
    ```
2. もし、`command not found`などのエラーが出た場合やバージョンが異なる場合、以下のコマンドを実行します。
    ```bash
    brew install openjdk@17
    ```
3. 以下のコマンドを入力し、バージョンが表示されたら成功です。(表示されない方はTerminalを再起動してください)
    ```bash
    java --version
    ```
