#!/Users/rikutakada/.pyenv/shims python
# -*- coding: utf-8 -*-
import json
from datetime import datetime
from slackbot.bot import respond_to
from logger import create_file

fund = 'こちらはfundのヘルプです\nfund\nadd num [memo]\ngetlog [line]\nのいずれかを入力してください'
pay = 'こちらはpayのヘルプです\nunpayall [ "year/month" ]\npaidall [ "year/month" ]\nunpay id [ "year/month" ]\npaid id [ "year/month" ]\nlist\nのいずれかを入力してください'
wish = '現在鋭意作成中'
helps = 'こちらはヘルプです\nhelp -f(fund)\nhelp -p(pay)\nhelp -w(wish)\nのいずれかを入力してください'


@respond_to('help(.*)')
def help(message, something):
    if something == ' -f':
        message.reply(fund)
    elif something == ' -p':
        message.reply(pay)
    elif something == ' -w':
        message.reply(wish)
    else:
        message.reply(helps)


@respond_to('makedb')
def makedb(message):
    now_date = datetime.now().strftime('%Y/%m')
    with open('user.txt') as f:
        dic = {line.strip(): [now_date] for line in f.readlines()}
        if '' in [k for k, v in dic.items()]:
            dic.pop('')
        create_file('paylist.json', rem=True)
        with open('paylist.json', 'w') as f2:
            json.dump(dic, f2)
