#!/Users/rikutakada/.pyenv/shims python
# -*- coding: utf-8 -*-
from slackbot.bot import respond_to
import json
from datetime import datetime
from logger import create_file


#
# def parameter_check(string=''):
#     if not string.strip():
#         return 'ユーザー名を指定してください\n'
#
#
#
# def user_check(dic={[]}, string=''):
#     if dic.get(string) is None:
#         return string + 'というユーザー名は登録されていません\n'


@respond_to('paid (.*)')
@respond_to('unpay (.*)')
def paid(message, something):
    pay_or_unpay = message.body['text'].split(' ')[0]
    rpstring = '\n'
    something = something.split(' ')
    username = something[0]
    if len(something) > 1:
        year = something[1].lstrip().split('/')[0]
        month = something[1].lstrip().split('/')[1]
        if len(year) < 4:
            year = '20' + year
        if len(month) < 2:
            month = '0' + month
        y_and_m = year + '/' + month
    else:
        y_and_m = ''
    chosen_date = y_and_m or datetime.now().strftime('%Y/%m')

    with open('paylist.json', 'r') as f:
        json_dict = {k: set(v) for k, v in json.load(f).items()}
        if json_dict.get(username) is None:
            message.reply(username + 'というユーザー名は登録されていません\n')
            return

        if pay_or_unpay == 'paid':
            if chosen_date in json_dict[username]:
                json_dict[username].remove(chosen_date)
                rpstring += '{0} 様の {1} 分の支払いを確認しました\n'.format(username, chosen_date)
            else:
                rpstring += '{0} 様は {1} 分の支払いを既に済ませています\n'.format(username, chosen_date)
        else:
            if chosen_date not in json_dict[username]:
                json_dict[username].add(chosen_date)
                rpstring += '{0} 様の {1} 分を未払いに変更しました\n'.format(username, chosen_date)
            else:
                rpstring += '{0} 様は {1} 分の支払いをまだ済ませていません\n'.format(username, chosen_date)
            if json_dict[username] == [chosen_date]:
                message.reply(rpstring)
                return
        rejson(json_dict)
        if len(json_dict[username]) > 0:
            rpstring += '{0} 様は\n'.format(username)
            for date in sorted(json_dict[username]):
                rpstring += '\t{0}\n'.format(date)
            rpstring += '分の支払いを滞納しています。\n'
        else:
            rpstring += '{} 様の支払いの滞納はありません。\n'.format(username)
    message.reply(rpstring)


@respond_to('unpayall(.*)')
@respond_to('paidall(.*)')
def allunpay(message, something):
    pay_or_unpay = message.body['text'].split(' ')[0]
    rpstring = '\n'
    if len(something.lstrip()) > 0:
        year = something.lstrip().split('/')[0]
        month = something.lstrip().split('/')[1]
        if len(year) < 4:
            year = '20' + year
        if len(month) < 2:
            month = '0' + month
        y_and_m = year + '/' + month
    else:
        y_and_m = ''
    chosen_date = y_and_m or datetime.now().strftime('%Y/%m')

    with open('paylist.json', 'r') as f:
        json_dict = {k: set(v) for k, v in json.load(f).items()}
        if pay_or_unpay == 'paidall':
            for k, v in sorted(json_dict.items()):
                if chosen_date in v:
                    json_dict[k].remove(chosen_date)
                    rpstring += '{0} 様の {1} 分の支払いを確認しました\n'.format(k, chosen_date)
        else:
            for k, v in sorted(json_dict.items()):
                json_dict[k].add(chosen_date)
                rpstring += '{0} 様の {1} 分を未払いに変更しました\n'.format(k, chosen_date)
        rejson(json_dict)
        message.reply(rpstring)


@respond_to('list')
def unpaylist(message):
    with open('paylist.json', 'r') as f:
        json_dict = json.load(f)
        rpstring = '\n未払いリストを表示します\n'
        bill = 0
        for k, v in sorted(json_dict.items()):
            if v:
                rpstring += '{0}\t{1}\n'.format(k, ', '.join(v))
                bill += 1
        if bill == 0:
            message.reply('\n*未払いの人は誰も居ませんﾊﾟﾁﾊﾟﾁ*\n')
            return
        message.reply(rpstring)


def rejson(json_dict):
    with open('paylist.json', 'w') as f:
        json.dump({k: list(v) for k, v in json_dict.items()}, f)
