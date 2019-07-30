# 3目並べ
オープンキャンパスのためにちゃちゃっと作りました．  
参考: [囲碁ディープラーニングプログラミング](https://www.amazon.co.jp/dp/B07RW5NN1D/ref=dp-kindle-redirect?_encoding=UTF8&btkr=1)  
完成品: https://tic-tac-toe-456e8.firebaseapp.com/

## 導入
``` bash
$ git clone https://github.com/fuurin/tic-tac-toe
$ cd tic-tac-toe
```

まずはサーバを起動する必要がある
``` bash
$ cd server
$ python -m venv .venv
$ source .venv/bin/activate もしくは .venv\\Scripts\\activate
$ pip install -r requirements.txt
$ python app.py
```
  
続いてフロントエンド  
``` bash
$ cd ../front
$ yarn
$ yarn s
```
  
自動でブラウザが立ち上がり3目並べゲームができる．  


herokuサーバのデプロイ  
``` bash
$ cd server
$ heroku login
$ pip freeze > requirements.txt
$ git init
$ git remote add heroku https://git.heroku.com/tic-tac-toe-minimax-bot.git
$ git add .
$ git commit -m "comment"
$ git push heroku master
```

AWSサーバへのデプロイはgit経由
80番ポートをHTTPで開けておく
``` bash
$ export FLASK_APP=~/tic-tac-toe/server/app.py
$ flask run --host='0.0.0.0' --port='80' --with-threads --no-debugger >> log.txt &
```

firebaseへのフロントのデプロイ
``` bash
$ cd front
$ yarn build
$ firebase login
$ firebase init
$ firebase deploy
```

# 主な使用技術
サーバサイド  
- Python 3.7.3
- Flask 1.1.1
  
フロントエンド  
- TypeScript 3.5.3
- Phaser 3.18.1
- Vue-cli 3
- Webpack 4
- axios
  
ホスティング  
- Heroku
- Firebase