# Linuxでの環境構築

## 1. Gitのインストール

1. Terminalを起動し、以下のコマンドを実行します。
    ```bash
    git --version
    ```

2. もし、`command not found`などのエラーが出た場合、OS標準のパッケージマネージャーを使用してインストールします。
    - DebianベースのOSの場合(Ubuntuなど)
        ```bash
        sudo apt update
        sudo apt upgrade -y
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
    ```

2. もし、`command not found`などのエラーが出た場合やバージョンが低い場合、Pythonのバージョン管理ツールであるpyenvを使用してインストールします
    
    ```{warning}
    インストール方法の内容が最新ではない場合があるため、[https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv)を参照してください。
    ```

    1. 以下のコマンドを実行します。
        ```bash
        curl https://pyenv.run | bash
        ```

    2. 次に以下のコマンドを実行して、使用しているShellを確認します。
        ```bash
        echo $SHELL
        ```

    3. 表示されたShellに従ってコマンドを実行してください。

        `bash`が表示された方は以下のコマンドを実行してください
        ```bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc

        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile

        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
        echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
        echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
        ```

        `zsh`が表示された方は以下のコマンドを実行してください
        ```bash
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
        echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
        ```

        `fish`が表示された方は以下のコマンドを実行してください
        ```bash
        set -Ux PYENV_ROOT $HOME/.pyenv
        fish_add_path $PYENV_ROOT/bin
        pyenv init - | source
        ```

    4. 必要パッケージのインストール
        - DebianベースのOSの場合(Ubuntuなど)
            ```bash
            sudo apt update
            sudo apt upgrade -y
            sudo apt install make libssl-dev build-essential zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
            ```
        - Red HatベースのOSの場合(Fedoraなど)
            ```bash
            sudo yum install gcc bzip2 bzip2-devel openssl openssl-devel readline readline-devel sqlite-devel tk-devel
            ```

            ```bash
            sudo dnf install gcc bzip2 bzip2-devel openssl openssl-devel readline readline-devel sqlite-devel tk-devel
            ```

    5. python3.12のインストール
        ```bash
        exec "$SHELL"
        pyenv install 3.12
        pyenv global 3.12
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

2. もし、`command not found`などのエラーが出た場合やバージョンが異なる場合、OS標準のパッケージマネージャーを使用してインストールします
    - DebianベースのOSの場合(Ubuntuなど)
        ```bash
        sudo apt update
        sudo apt upgrade -y
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
