![supported platforms](https://img.shields.io/badge/platform-Mac-929292)
![supported python versions](https://img.shields.io/badge/python-%3E%3D%203.6-306998)


# Othello API

## 一行で概要を説明すると？

盤面の情報を送れると，次の1手を返してくれる人工知能APIです．

## 開発環境
+ MacOS BigSur 11.2.3
+ Python 3.8.5
+ GCP App Engine
+ Pytorch 1.8.1
+ REST API

## 特徴

* [x] 強化学習としてMuzeroを使用
* [x] オセロに特化したAI型API
* [x] 学習レベルによって難易度を変更可能
* [ ] 対人間において人間を圧倒できる強さをもつ


## 実行

1. 以下のURLをAPIのURLとして指定する．

   ~~https://othelloapi.df.r.appspot.com/~~

   （一応アクセスできますが現在調整中）

2. 受け取る形式はPOSTのみ

   以下のような配列の形式で送ることで認証できる．

   <u>一例</u>
   ```python
   [[ 0,  0,  0,  0,  0,  0,  0,  0],
   [ 0,  0,  0,  0,  0,  0,  0,  0],
   [ 0,  0,  0,  0,  0,  0,  0,  0],
   [ 0,  0,  0,  1, -1,  0,  0,  0],
   [ 0,  0,  0, -1,  1,  0,  0,  0],
   [ 0,  0,  0,  0,  0,  0,  0,  0],
   [ 0,  0,  0,  0,  0,  0,  0,  0],
   [ 0,  0,  0,  0,  0,  0,  0,  0]]
   ```

3. ```4,3```のように```行,列```の形式でコンマ区切りのstringが返される．


## 参考文献

+ [DeepMind Official Blog](https://deepmind.com/blog/article/muzero-mastering-go-chess-shogi-and-atari-without-rules)
+ [Muzero paper](https://www.nature.com/articles/s41586-020-03051-4.epdf?sharing_token=kTk-xTZpQOF8Ym8nTQK6EdRgN0jAjWel9jnR3ZoTv0PMSWGj38iNIyNOw_ooNp2BvzZ4nIcedo7GEXD7UmLqb0M_V_fop31mMY9VBBLNmGbm0K9jETKkZnJ9SgJ8Rwhp3ySvLuTcUr888puIYbngQ0fiMf45ZGDAQ7fUI66-u7Y%3D)
+ [Flask Official Tutorial](https://flask.palletsprojects.com/en/2.0.x/)