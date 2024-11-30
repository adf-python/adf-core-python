# Windowsでの環境構築

## 1. Gitのインストール

1. [Git for Windows](https://gitforwindows.org/)の公式サイトにアクセスします。
2. トップページの"Download"をクリックします
3. ダウンロードが完了した後、インストーラーを実行します。
4. 全て"Next"をクリックします。
5. インストールが完了するまで待ちます。
6. インストールが完了したら"Finish"をクリックします。
7. 検索バーに"Git Bash"と入力し、Git Bashを実行します。
8. 画面が表示されていたらインストール成功です。

## 2. Pythonのインストール

1. [Python](https://www.python.org/)の公式サイトにアクセスします。
2. トップページの"Download Python ~"をクリックします
3. ダウンロードが完了した後、インストーラーを実行します。
4. "Add python.exe to PATH"にチェックが入っていることを確認した後、"Install Now"をクリックします。
5. インストールが完了するまで待ちます。
6. インストールが完了したら"Close"をクリックします。
7. Git Bashを開き、`python --version`と入力し、`Python [バージョン]`が表示されたら成功です。(もし表示されない場合はGit Bashを開き直してください)

## 3. OpenJDKのインストール

1. [OpenJDK](https://jdk.java.net/archive/)のダウンロードページにアクセスします。
2. 17.0.2のWindowsの横にある"zip"をクリックします。
3. ダウンロードしたzipを展開(解凍)します。
4. 展開(解凍)すると"jdk-17.0.2"のようなフォルダができるのを確認します。
5. このフォルダ"jdk-17.0.2"を`C:¥`の直下に移動させます。
6. Windowsでコマンドプロンプトを管理者として実行します。
7. 開いたら以下のコマンドを実行します。
    ```
    powershell -command "[System.Environment]::SetEnvironmentVariable(\"JAVA_HOME\", \"c:\jdk-17.0.2\", \"Machine\")"
    ```
8. 次に以下のコマンドを実行します。
    ```
    powershell -command "$oldpath = [System.Environment]::GetEnvironmentVariable(\"Path\", \"Machine\"); $oldpath += \";c:\jdk-17.0.2\bin\"; [System.Environment]::SetEnvironmentVariable(\"Path\", $oldpath, \"Machine\")"
    ```
9. Git Bashを開き、`java -version`と入力します。
    以下のような文字が表示されたらインストール成功です。
    ```
    openjdk version "17.0.2" 2022-01-18
    OpenJDK Runtime Environment (build 17.0.2+8-86)
    OpenJDK 64-Bit Server VM (build 17.0.2+8-86, mixed mode, sharing)
    ```