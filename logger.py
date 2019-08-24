import json
from datetime import datetime
from os import system
from glob import glob


def getLog(filename='fundLog.json'):
    log = {}
    create_file(filename)  # fundLog.jsonがなかった時の処理
    with open(filename, 'r') as f:
        if not f.readlines():
            return log
        else:
            f.seek(0)  # ファイルポインタの位置を戻す
            log = json.load(f)
    return log  # 返り値はdict(list)ですのであしからず


def subLog(filename='fundLog.json', sub=0, memo=''):
    log = getLog(filename)
    log[datetime.now().strftime('%Y/%m/%d %H:%M:%S')] = (sub, memo)
    with open(filename, 'w') as f:
        json.dump(log, f)


# 空ファイル作成
def create_file(filename='None.txt', rem=False):
    if rem:
        system('rm -f ' + filename)
    if filename not in glob('*'):
        system('touch ' + filename)


if __name__ == '__main__':
    subLog('fundLog.json', 1000, 'テスト')
