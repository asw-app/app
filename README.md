# README

## Japanese
- app.py: アプリケーションを実行するメインのコード  
- home.html: HP用のHTMLファイル  
- report_form.html: 報告用のHTMLファイル
- result.html: 総和計算用のHTMLファイル

### 使い方
ターミナルで以下のコードを入力して，実行する．
```shell
$ pip install -r requirements.txt
$ flask run
```

### <注意点>  
- HTMLファイルは，App_run.pyファイルと同じ階層のtemplatesディレクトリに配置． - - - render_template('~.html')で表示.   
- JavaScript,CSSなどの静的ファイルを利用する場合staticディレクトリへ配置．

## English
- app.py: This is a Entry Point program file.
- home.html: This is a HTML file for top page.
- report_form.html: This is a HTML file for reporting.
- result.html: This is a a HTML file for calculating.

### How to use
Type bellow code in terminal.
```shell
$ pip install -r requirements.txt
$ flask run
```