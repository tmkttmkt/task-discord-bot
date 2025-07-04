import random
import sys
from pathlib import Path
from collections import deque

# 直接実行時と相対インポート時の対応
try:
    # パッケージとしてインポートされた場合（discord_bot.pyから呼ばれる場合）
    from .date import Fumu, listkun
except ImportError:
    # 直接実行された場合
    from date import Fumu, listkun

class Tetsu:
    def __init__(self, lists:dict[tuple[str],list[str]], max_length=100):
        self.list = lists.copy()
        if len(lists)==0:raise ValueError("え？？データないやん。どないしてくれるん？")
        self.num=len(list(lists.keys())[0])
        self.max_length = max_length  # 最大の文章の長さ

    def create_text(self):
        sentence = []
        count = 0
        queue = deque(list(self.list.keys())[0],maxlen=self.num)
        current_list = self.list[tuple(queue)]
        next_key = random.choice(current_list)
        queue.append(next_key)
        sentence.append(next_key)
        while not tuple(queue)==list(self.list.keys())[0] and count < self.max_length:
            current_list = self.list[tuple(queue)]
            if not current_list:
                break

            next_key = random.choice(current_list)
            if next_key==None:
                break
            sentence.append(next_key)
            queue.append(next_key)

            if not (tuple(queue) in self.list):
                break

            count += 1  # 文章の長さをカウント

        return "".join(sentence)


def main():
    f=Fumu(num=1)
    f.read_json(Path("output2.json"))
    print(f.dtnaver,f.dtnmedi)
    tetsus = Tetsu(f.date)
    text_list=[]
    for _ in range(10):
        generated_text = tetsus.create_text()
        text_list.append(generated_text)
    print(text_list)


if __name__ == "__main__":
    main()

"""

1-(40.14169779724333 2.0)
2-(4.150929047827825 1)

"""