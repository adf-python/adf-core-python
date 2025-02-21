.. adf-core-python documentation master file, created by
   sphinx-quickstart on Mon Oct 14 00:15:07 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

adf-core-pythonのドキュメント
==============================

.. warning::

   現在このパッケージは開発中です。破壊的な変更が行われる可能性があります。

.. warning::

   パッケージとしてまだ公開していないため、pip でインストールすることはできません。

.. warning::

   以下の言語のドキュメントは機械翻訳を使用しています。翻訳の正確性については保証できません。
   英語


概要
----
adf-core-pythonは、RoboCup Rescue Simulation(RRS)におけるエージェント開発を支援するためのライブラリ及びフレームワークです。
adf-core-pythonを使用することで、エージェントの開発を効率化し、再利用性を向上させることができます。

特徴
----
adf-core-pythonには以下のような特徴があります。

- **モジュール単位での開発**: モジュール単位でエージェント開発を行い、モジュールの入れ替えが容易です。
- **モジュールの再利用**: 他のエージェントで使用されているモジュールを再利用することができます。
- **エージェントの開発に集中**: シミュレーションサーバーとの通信やログ出力などの共通処理をライブラリが提供します。

はじめに
--------
adf-core-pythonを始めるには、インストールに従い、このドキュメントに記載されているチュートリアルやハンズオンを参照してください。

.. toctree::
   :maxdepth: 1
   :caption: インストール

   install/environment/environment
   install/install/install

.. toctree::
   :maxdepth: 1
   :caption: クイックスタート

   quickstart/quickstart

.. toctree::
   :maxdepth: 1
   :caption: チュートリアル

   tutorial/environment/environment
   tutorial/agent/agent
   tutorial/agent/agent_control
   tutorial/config/config
   tutorial/module/module

.. toctree::
   :maxdepth: 1
   :caption: ハンズオン

   hands-on/clustering
   hands-on/search

.. toctree::
   :maxdepth: 1
   :caption: APIドキュメント

   modindex
   search

.. automodule:: adf_core_python
   :members:
   :undoc-members:
   :show-inheritance:
