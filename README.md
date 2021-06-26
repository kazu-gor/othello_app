![supported platforms](https://img.shields.io/badge/platform-Mac-929292)
![supported python versions](https://img.shields.io/badge/python-%3E%3D%203.6-306998)


# Othello API

## API概要

盤面の情報を送ると，次の1手を返してくれる人工知能API

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
* [x] POSTでAPIを叩くことができる
* [ ] GETでAPIを叩くことができる
* [ ] 対人間において人間を圧倒できる強さをもつ


## 実行

1. 以下のURLにAPIのリクエストを送る

   https://othelloapi.df.r.appspot.com/

2. 受け取る形式はPOSTのみ

   例に示すような ```{'body': {'board': value }}``` のJSON形式で送る必要がある．

   GETでアクセスしてしまうと，```0``` が Return される．


   <u>例 (JSON)</u>


   ```json
  "board": {
      "0": "[0,0,0,0,0,0,0,0]",
      "1": "[0,0,0,0,0,0,0,0]",
      "2": "[0,0,0,0,0,0,0,0]",
      "3": "[0,0,0,-1,1,0,0,0]",
      "4": "[0,0,0,1,-1,0,0,0]",
      "5": "[0,0,0,0,0,0,0,0]",
      "6": "[0,0,0,0,0,0,0,0]",
      "7": "[0,0,0,0,0,0,0,0]"
   }
   ```

3. ```{"result": str(row) + "," + str(col)}``` のようにJSON形式でコンマ区切りの行列が返される．

   <u>例</u>  ```{"result": "4,3"}```


## 補足
* APIのプレイヤー番号は現在原則 ```1``` としている．
* Userの番号は ```-1``` である．
* 配置していないマスは ```0``` である．



## 参考文献

+ [DeepMind Official Blog](https://deepmind.com/blog/article/muzero-mastering-go-chess-shogi-and-atari-without-rules)
+ [Muzero paper](https://www.nature.com/articles/s41586-020-03051-4.epdf?sharing_token=kTk-xTZpQOF8Ym8nTQK6EdRgN0jAjWel9jnR3ZoTv0PMSWGj38iNIyNOw_ooNp2BvzZ4nIcedo7GEXD7UmLqb0M_V_fop31mMY9VBBLNmGbm0K9jETKkZnJ9SgJ8Rwhp3ySvLuTcUr888puIYbngQ0fiMf45ZGDAQ7fUI66-u7Y%3D)
+ [Flask Official Tutorial](https://flask.palletsprojects.com/en/2.0.x/)