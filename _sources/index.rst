.. adf-core-python documentation master file, created by
   sphinx-quickstart on Mon Oct 14 00:15:07 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

adf-core-pythonのドキュメント
==============================

.. warning::

   現在このパッケージは開発中です。破壊的な変更が行われる可能性があります。

.. warning::

   パッケージとしてまだ公開していないので、pip でインストールすることはできません。


.. contents:: 目次
   :depth: 2
   :local:

特徴
----

- **モジュール単位での開発**: モジュール単位でエージェント開発を行い、モジュールの入れ替えが容易です。
- **モジュールの再利用**: 他のエージェントで使用されているモジュールを再利用することができます。
- **エージェントの開発に集中**: シミュレーションサーバーとの通信やログ出力などの共通処理をライブラリが提供します。

はじめに
--------

ADF Core Python を始めるには、インストール手順に従い、このドキュメントに記載されている例を参照してください。

.. toctree::
   :maxdepth: 1
   :caption: チュートリアル:

   tutorial/environment/environment
   tutorial/install/install
   tutorial/agent/agent
   tutorial/agent/agent_control
   tutorial/config/config
   tutorial/module/module

.. toctree::
   :maxdepth: 1
   :caption: ハンズオン:

   hands-on/clustering

.. toctree::
   :maxdepth: 1
   :caption: クイックスタート:

   quickstart/quickstart

.. automodule:: adf_core_python
   :members:
   :undoc-members:
   :show-inheritance:


パッケージの詳細
---------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
