##! メモ !## 
#! 以前のグルーピングとの重複を確認できるが、以前に話したことがある人の重複は考慮できない 
#!#!#! 

import math,random,sys,copy

# 名前を登録(敬称略)
Names=["Sakamoto","Eto","Iwaki","Ido","Ogina","Asai","Fumi Sato","Kamiyama","Tanno", \
      "Mio Sato","Seto","Yagi","Suzuki","Ono","Tate","Okamoto","Fukamaki","Toshiyuki Tanaka", \
      "Kaide","Nakajima","Saito","Kawakami","Yamashita","Tominaga","Tada","Kimura","Tanabe", \
      "Inazawa","Okawa","Fujioka","Hikita","Ishiyama","Kajitani","Hinako Tanaka","Wako","Jinnouchi"]

N=5         # 1グループ何人?
K=2         # 何人までの重複を許容? (K=2: 同時に同じグループに入ったことがある3人以上が同じグループに入る割り方を禁止)
T=10000     # 探索回数の上限

# 欠席者を登録
Absent=["Iwaki","Kaide","Tanabe","Fujioka","Hikita","Jinnouchi","Ishiyama","Kimura"]
# 欠席者がリストに含まれるかチェック&該当者を辞書から削除
for a in Absent:
    if not a in Names:
        print("欠席者の名前に間違いがあります:"+a)
        sys.exit()
    Names.remove(a)

# グループ数:余りグループの人数がN-1人以下の場合, 余りはランダムでどっかにappendする.
if len(Names)%N>N-2 or len(Names)%N==0:
    Ng=math.ceil(len(Names)/N)
    Amari=False
else:
    Ng=math.floor(len(Names)/N)
    Amari=True

# 部屋番を登録
#Owners=["Mio Sato","Saito","Eto","Toshiyuki Tanaka","Seto","Kajitani"]
Owners=["Mio Sato","Saito","Eto","Toshiyuki Tanaka","Seto"]
# 部屋番がリストに含まれるか, 多すぎ少なすぎはないか, 確認, 部屋番は辞書から削除
if len(Owners)!=Ng:
    print("部屋番の数がグループ数と一致しません. グループ数は {0} です.".format(Ng))
    sys.exit()
for o in Owners:
    if not o in Names:
        print("部屋番の名前に間違いがあります:"+o)
        sys.exit()
    Names.remove(o)

# 以前に組まれた組み合わせをリスト化(部屋ごと) 
BlackList = [\
# 第一回
["Mio Sato","Fumi Sato","Nakajima","Tanno","Yamashita","Ishiyama"],["Saito","Kimura","Kawakami","Inazawa","Hikita","Hinako Tanaka"],["Eto","Jinnouchi","Kaide","Wako","Yagi","Okawa","Sakamoto"],["Toshiyuki Tanaka","Kamiyama","Fukamaki","Tominaga","Ogina","Fujioka"],["Seto","Tate","Suzuki","Ido","Asai","Tada"],\
["Mio Sato","Yagi","Asai","Fujioka","Sakamoto","Ido"],["Saito","Ogina","Kaide","Hinako Tanaka","Kamiyama","Fukamaki"],["Eto","Tominaga","Hikita","Tanno","Suzuki","Yamashita"],["Toshiyuki Tanaka","Fumi Sato","Tada","Nakajima","Ishiyama","Tate","Jinnouchi"],["Seto","Wako","Okawa","Inazawa","Kawakami","Kimura"],\
["Mio Sato","Jinnouchi","Tada","Kawakami","Ogina","Hinako Tanaka"],["Saito","Yagi","Wako","Kimura","Suzuki","Asai"],["Eto","Tate","Fujioka","Fukamaki","Fumi Sato","Ishiyama"],["Toshiyuki Tanaka","Tanno","Sakamoto","Ido","Okawa","Hikita"],["Seto","Yamashita","Tominaga","Nakajima","Kamiyama","Kaide","Inazawa"], \
# 第二回
["Mio Sato","Wako","Ono","Yagi","Tate"],["Saito","Kamiyama","Sakamoto","Tominaga","Okamoto"],["Eto","Fukamaki","Tada","Suzuki","Ishiyama"],["Toshiyuki Tanaka","Yamashita","Kimura","Ido","Tanno"],["Seto","Inazawa","Kawakami","Asai","Fumi Sato"],["Kajitani","Nakajima","Okawa","Hinako Tanaka","Ogina"],\
["Mio Sato","Kawakami","Ogina","Tominaga","Asai"],["Saito","Fukamaki","Yamashita","Fumi Sato","Ido"],["Eto","Ono","Tate","Kimura","Wako"],["Toshiyuki Tanaka","Okawa","Nakajima","Okamoto","Inazawa"],["Seto","Yagi","Hinako Tanaka","Sakamoto","Ishiyama"],["Kajitani","Suzuki","Tanno","Kamiyama","Tada"], \
["Mio Sato","Hinako Tanaka","Okawa","Okamoto","Inazawa"],["Saito","Tada","Tanno","Suzuki","Tate"],["Eto","Fumi Sato","Ono","Asai","Ogina"],["Toshiyuki Tanaka","Kamiyama","Wako","Yagi","Sakamoto"],["Seto","Yamashita","Fukamaki","Nakajima","Tominaga"],["Kajitani","Ishiyama","Ido","Kawakami","Kimura"]]    

# 処理開始
Flag=False 
It=0
while not Flag:
    print("\r"+"探してます(試行回数:{0})".format(It),end="")
    groups = []
    if It>=T:
        print("適切な組み合わせが見つかりません, 制約を緩めてください")
        break
    random.shuffle(Names)
    for i in range(0,Ng):            
        groups.append([Owners[i]]+Names[(N-1)*i:(N-1)*i+(N-1)])

    Groups = copy.deepcopy(groups)
    if Amari:                       # 余った人をappendする処理
        while True:
            Groups = copy.deepcopy(groups)
            for p in Names[(N-1)*Ng:]:
                Groups[random.randint(0,Ng-1)].append(p)
            if max([len(g) for g in Groups])==(min([len(g) for g in Groups])+1):
                break

    for A in Groups:                 # ブラックリストの組み合わせにかぶってないかチェック
        for B in BlackList: 
            C=A+B
            r=len(C)-len(set(C))     # 重複した人数
            if r>K:                  # 重複人数が多い,やり直し
                Flag=False
                break
            else:
                Flag=True
        if not Flag:
            break
    It+=1
	
if len(Groups)>0:
    print("")
    print(Groups)
