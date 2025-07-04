import MeCab
import json
import os
from pathlib import Path
import statistics


class Fumu:
    def __init__(self,prcosse:list[tuple[str,tuple]]=[],num=1) -> None:
        # MeCabの初期化（環境変数MECABRCを使用）
        try:
            print("MeCab初期化中...")
            self.mecab = MeCab.Tagger()
            print("MeCab初期化成功！")
            # テスト
            test_result = self.mecab.parse("テスト")
            print(f"MeCabテスト結果: {test_result}")
        except Exception as e:
            print(f"MeCab初期化エラー: {e}")
            print("環境変数を確認します...")
            print(f"MECABRC: {os.environ.get('MECABRC', 'Not set')}")
            print(f"MECAB_DICDIR: {os.environ.get('MECAB_DICDIR', 'Not set')}")
            raise e
        
        self.date:dict[tuple[str],list[str]]={}
        self.__words:dict[str,int]={}
        self.wordnum=0
        self.dictonum:float=0
        self.minenum:float=0
        self.__prcosses:list=prcosse
        self.num=num
    def procosses(self,input:list):
        self.__prcosses=input
    def parseToNode(self,text):
        node=self.mecab.parseToNode(text)
        words=[]
        while node:
            if node.surface:  # ノードが空でない場合
                # 表層形を追加
                words.append(node.surface)
            node = node.next  # 次のノードに進む
        self.listtodic(words)

    def train(self,text,prcosse_flg=False):
        if isinstance(text,Path):
            if text.is_file():#ファイルです
                with open(text,encoding="UTF-8") as f:
                    self.train(f.read())
            elif text.is_dir():#ディレクトリです
                for item in text.iterdir():
                    self.train(item)
            else:
                raise ValueError(f"{text} は存在しないか、ファイルでもディレクトリでもありません")
        elif isinstance(text,list):
            for obj in text:
                self.train(obj)
        elif isinstance(text,str):#必ずここにたどり着く
            if not prcosse_flg:
                for prcosse in self.__prcosses:
                    text=getattr(text,prcosse[0])(*prcosse[1])
                if not isinstance(text,str):
                    if isinstance(text,list):
                        for obj in text:
                            self.train(obj,prcosse_flg=True)
                    else:
                        raise Exception("はい、なんででしょうね？")
                else:
                    self.parseToNode(text)
            else:
                self.parseToNode(text)
        else:
            raise ValueError(f"え!!それどんな型？？、頭大丈夫？？\n\tPath型とlist型とstr型の派生クラス以外受け付けません\n\t{type(text)}")

    def listtodic(self,words:list):
        for word in words:
            self.wordnum+=1
            if word in self.__words:
                self.__words[word]+=1
            else:self.__words[word]=1
        n=0
        key=()
        while n<len(words):
            if n<self.num:
                key=words[:n]
                while len(key)<self.num:
                    key.insert(0,None)
            else:
                key=words[n-self.num:n]
            key=tuple(key)
            if key in self.date:
                self.date[key].append(words[n])
            else:self.date[key]=[words[n]]
            n+=1
        if key in self.date:
            self.date[key].append(None)
        else:self.date[key]=[None]

        self.words=sorted(self.__words.items(), key=lambda x:x[1],reverse=True)

    def reset(self):
        self.date=None
        self.__words={}
        self.wordnum=0
    def read_json(self,filetxt="output.json",append=False):
        with open(filetxt, 'r',encoding='utf-8') as file:
            data = json.load(file)
        todate={}
        for key  in data:
            tt=key[1:]
            todate[tuple(tt.split("-"))]=data[key]
        if append:
            for key  in todate:
                if key in self.date:
                    self.date[key]+=todate[key]
                else:self.date[key]=todate[key]
        else:
            self.date=todate
        self.lendic()
    def lendic(self):
        lis=[]
        for key in self.date:
            lis.append(len(self.date[key]))
        self.dtnaver:float=sum(lis) / len(lis)
        self.dtnmedi:float=statistics.median(lis)
    def write_json(self,filetxt="output.json"):
        data={}
        for key in self.date:
            ex_txt=""
            for txt in key:
                if txt==None:
                    ex_txt+="-"+"none"
                elif type(txt)==str:
                    ex_txt+="-"+txt
                else:
                    ValueError(f"{type(txt)}ってなんだ？")
            data[ex_txt]=self.date[key]
        with open(filetxt, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

listkun = {
    None: ["私は", "俺は", "うちは", "拙者は"],
    "私は": ["プログラミングが", "本が", "映画が", "音楽が"],
    "俺は": ["プログラミングが", "本が", "映画が", "音楽が"],
    "うちは": ["プログラミングが", "本が", "映画が", "音楽が"],
    "拙者は": ["プログラミングが", "本が", "映画が", "音楽が"],
    "プログラミングが": ["好きです。", "面白いです。", "挑戦しています。", "学んでいます。"],
    "本が": ["好きです。", "面白いです。", "勉強になります。", "リラックスできます。"],
    "映画が": ["好きです。", "興味深いです。", "感動しました。", "娯楽の一部です。"],
    "音楽が": ["好きです。", "リラックスできます。", "エネルギーをもらえます。", "日常の一部です。"],
    "好きです。": ["毎日", "時々", "よく", "たまに"],
    "面白いです。": ["とても", "かなり", "すごく", "特に"],
    "挑戦しています。": ["毎日", "時々", "週末には", "時間があるときに"],
    "学んでいます。": ["新しい技術を", "新しい知識を", "新しいスキルを", "新しい言語を"],
    "勉強になります。": ["いろいろなことを", "多くの知識を", "深い理解を", "専門的な知識を"],
    "リラックスできます。": ["静かな環境で", "お風呂に入って", "好きな音楽を聴いて", "読書しながら"],
    "興味深いです。": ["歴史的な", "文化的な", "技術的な", "独特な"],
    "感動しました。": ["涙が出るほど", "心に残る", "思い出に残る", "深く感銘を受けました"],
    "娯楽の一部です。": ["週末の", "休日の", "リラックスタイムの", "気分転換の"],
    "毎日": ["新しいことを", "少しずつ", "努力して", "挑戦して"],
    "時々": ["趣味に", "新しいことに", "リラックスに", "自分磨きに"],
    "よく": ["友達と", "家族と", "一人で", "時間があるときに"],
    "たまに": ["特別な日に", "イベントの時に", "何もない日に", "暇なときに"],
    "とても": ["面白い", "楽しい", "感動的", "興味深い"],
    "かなり": ["魅力的", "刺激的", "新鮮", "意外な"],
    "すごく": ["面白い", "印象的", "心に残る", "衝撃的"],
    "特に": ["心に残る", "感動的", "新しい", "意義深い"],
    "新しい技術を": ["学んでいます。", "試しています。", "研究しています。", "実践しています。"],
    "新しい知識を": ["身につけています。", "得ています。", "吸収しています。", "活用しています。"],
    "新しいスキルを": ["習得しています。", "磨いています。", "挑戦しています。", "練習しています。"],
    "新しい言語を": ["勉強しています。", "練習しています。", "使っています。", "習得しています。"],
    "いろいろなことを": ["学んでいます。", "経験しています。", "考えています。", "試しています。"],
    "多くの知識を": ["吸収しています。", "得ています。", "実践しています。", "活用しています。"],
    "深い理解を": ["得ています。", "実感しています。", "体験しています。", "学んでいます。"],
    "専門的な知識を": ["習得しています。", "学んでいます。", "研究しています。", "活用しています。"],
    "静かな環境で": ["リラックスしています。", "読書しています。", "瞑想しています。", "深呼吸しています。"],
    "お風呂に入って": ["リラックスしています。", "体を温めています。", "心を落ち着けています。", "疲れを取っています。"],
    "好きな音楽を聴いて": ["リラックスしています。", "元気をもらっています。", "集中しています。", "気分転換しています。"],
    "読書しながら": ["リラックスしています。", "知識を深めています。", "感情を整理しています。", "心を落ち着けています。"],
    "歴史的な": ["出来事に関する", "背景を知る", "人物を学ぶ", "文化を理解する"],
    "文化的な": ["背景を学ぶ", "意味を理解する", "影響を考える", "伝統を知る"],
    "技術的な": ["進歩を追う", "トレンドを知る", "専門的な知識を得る", "イノベーションを学ぶ"],
    "独特な": ["スタイルを学ぶ", "アプローチを理解する", "特性を知る", "ユニークな点を見つける"],
    "涙が出るほど": ["感動しました。", "心が揺さぶられました。", "強い感情を覚えました。", "深く感銘を受けました。"],
    "心に残る": ["体験をしました。", "思い出に残りました。", "感情が揺さぶられました。", "深く印象に残りました。"],
    "思い出に残る": ["体験をしました。", "特別な瞬間がありました。", "感情が動かされました。", "強く記憶に残りました。"],
    "深く感銘を受けました": ["心が動かされました。", "印象に残りました。", "感情が高まりました。", "忘れられない体験をしました。"],
    "週末の": ["活動をしています。", "リラックス時間を持っています。", "プランを立てています。", "楽しい時間を過ごしています。"],
    "休日の": ["アクティビティをしています。", "家族と過ごしています。", "旅行に行っています。", "リフレッシュしています。"],
    "リラックスタイムの": ["過ごし方を楽しんでいます。", "アクティビティをしています。", "ルーチンを変えています。", "心を落ち着けています。"],
    "気分転換の": ["方法を試しています。", "活動をしています。", "時間を持っています。", "アプローチを変えています。"],
    "新しいことを": ["学んでいます。", "試しています。", "挑戦しています。", "体験しています。"],
    "少しずつ": ["成長しています。", "改善しています。", "進んでいます。", "上達しています。"],
    "努力して": ["成果を出しています。", "目標に向かっています。", "取り組んでいます。", "進歩しています。"],
    "挑戦して": ["新しいことを試しています。", "困難に立ち向かっています。", "自己成長を目指しています。", "新しい経験をしています。"],
    "友達と": ["過ごしています。", "アクティビティをしています。", "食事に行っています。", "イベントに参加しています。"],
    "家族と": ["時間を過ごしています。", "旅行に行っています。", "食事を楽しんでいます。", "休日を過ごしています。"],
    "一人で": ["リラックスしています。", "趣味を楽しんでいます。", "集中しています。", "自己改善をしています。"],
    "時間があるときに": ["新しいことに挑戦しています。", "リラックスしています。", "趣味を楽しんでいます。", "自分の時間を楽しんでいます。"],
    "プロジェクトを": ["進めています。", "計画しています。", "管理しています。", "完成させています。"],
    "活動を": ["進めています。", "楽しんでいます。", "計画しています。", "管理しています。"],
    "時間を": ["有効に使っています。", "楽しんでいます。", "計画しています。", "休息を取っています。"],
    "作成しています。": ["新しいアイデアを", "プロジェクトを", "作品を", "プランを"],
    "進めています。": ["プロジェクトを", "計画を", "アクティビティを", "目標を"],
    "計画しています。": ["プロジェクトを", "活動を", "未来のことを", "次のステップを"],
    "考えています。": ["次のアイデアを", "解決策を", "目標を", "新しいアプローチを"],
    "楽しんでいます。": ["趣味を", "活動を", "リラックスしています。", "友達と過ごしています。"]
}
