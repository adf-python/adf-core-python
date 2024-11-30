# Linuxでの環境構築

## 1. Gitのインストール

1. Terminalを起動し、以下のコマンドを実行します。
    ```bash
    git --version
    ```

2. もし、`command not found`などのエラーが出た場合、OS標準のパッケージマネージャーを使用してインストールします。
    - DebianベースのOSの場合(Ubuntuなど)
        ```bash
        sudo apt install git
        ```
    - Red HatベースのOSの場合(Fedoraなど)
        ```bash
        sudo yum install git
        ```

        ```bash
        sudo dnf install git
        ```

3. 以下のコマンドを入力し、バージョンが表示されたら成功です。(表示されない方はTerminalを再起動してください)
    ```bash
    git --version
    ```

## 2. Pythonのインストール

1. Terminalを起動し、以下のコマンドを実行します。また、バージョンが3.12以上になっていることを確認します。
    ```bash
    python --version
    # OR
    python3 --version
    ```

2. もし、`command not found`などのエラーが出た場合やバージョンが低い場合、OS標準のパッケージマネージャーを使用してインストールします
    - DebianベースのOSの場合(Ubuntuなど)
        ```bash
        sudo apt install python3.12 python3.12-pip
        ```
    - Red HatベースのOSの場合(Fedoraなど)
        ```bash
        sudo yum install python3.12 python3.12-pip
        ```

        ```bash
        sudo dnf install python3.12 python3.12-pip
        ```

3. 以下のコマンドを入力し、バージョンが表示されたら成功です。(表示されない方はTerminalを再起動してください)
    ```bash
    python --version
    # OR
    python3 --version
    ```

## 3. OpenJDKのインストール

1. Terminalを起動し、以下のコマンドを実行します。また、バージョンが17になっていることを確認します。
    ```bash
    java --version
    ```

2. もし、`command not found`などのエラーが出た場合やバージョンが異なる場合、OS標準のパッケージマネージャーを使用してインストールします
    - DebianベースのOSの場合(Ubuntuなど)
        ```bash
        sudo apt install openjdk-17-jdk
        ```
    - Red HatベースのOSの場合(Fedoraなど)
        ```bash
        sudo yum install java-17-openjdk-devel
        ```

        ```bash
        sudo dnf install java-17-openjdk-devel
        ```

3. 以下のコマンドを入力し、バージョンが表示されたら成功です。(表示されない方はTerminalを再起動してください)
    ```bash
    java --version
    ```
