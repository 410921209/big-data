import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

df = pd.read_csv("G:/我的雲端硬碟/big_data/Disaster.csv",encoding='utf-8-sig')
temp = True
pcount = 0
error = []

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
year = yesterday.year - 1911
YTD = str(year)+yesterday.isoformat()[4:]
TD = str(year)+today.isoformat()[4:]
print(YTD)

while(temp):
    pcount += 1
    print(pcount)
    req = requests.get(f"https://www.nfa.gov.tw/cht/index.php?code=list&ids=22&page={pcount}")
    req.encoding = 'utf-8'
    s = BeautifulSoup(req.text, "html.parser")  # 轉換成標籤樹
    data_index = s.find_all("tr")
    #print(data_index)
    for i in range(1,len(data_index)):
        data_index_nr = data_index[i]
        try :
            for b in data_index_nr.find_all("a"): #標題
                text=b.getText()
                print(text)
                l=[text]
            for b in data_index_nr.find_all("td",class_ = "center"): #發布時間
                date_text = b.getText()
            if (date_text == TD):
                temp = True
                continue
            if (date_text == YTD):
                l.append(date_text)
                print(l)
                df.loc[df.shape[0]] = l
            else:
                temp = False
                break    
        except:
            error.append(text)
            print(text)
            continue

print(df)
df = df.drop_duplicates()
df.to_csv("G:/我的雲端硬碟/big_data/Disaster.csv", index=False,encoding='utf-8-sig')