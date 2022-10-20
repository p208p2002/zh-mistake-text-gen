.. zh-mistake-text-gen documentation master file, created by
   sphinx-quickstart on Thu Oct 20 02:11:00 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

錯誤類型中文語料生成
===============================================

使用
=====

安裝
------------

.. code-block:: console

   $ pip install zh-mistake-text-gen

.. toctree::
   zh_mistake_text_gen.rst
   :maxdepth: 2
   :caption: Contents:


基礎用法
-------

.. code-block:: python

   from zh_mistake_text_gen import Pipeline
   pipeline = Pipeline()
   incorrect_sent = pipeline("中文語料生成")
   print(incorrect_sent)
   # type='PronounceSimilarVocabMaker' correct='中文語料生成' incorrect='鍾文語料生成' incorrect_start_at=0 incorrect_end_at=2 span='鍾文'

| 更多範例: https://github.com/p208p2002/zh-mistake-text-gen/tree/main/examples