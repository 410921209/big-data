import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
list = []
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
                if (date_text[:3] == '111' or date_text == TD or date_text == YTD): #停止抓取資料
                    temp = False
                    break                    
                l.append(date_text)
                print(l)
            if (pcount == 1 and temp == False):
                temp = True
                continue
            if (temp == False):
                break
            list.insert(0,l)
        except:
            error.append(text)
            print(text)
            continue

data = data_index[0].find_all("th",class_="center")#表頭
df = pd.DataFrame(list)
df.columns = [data[0].getText(),data[2].getText()]


df.to_csv("G:/我的雲端硬碟/big_data/Disaster.csv", index=False,encoding='utf-8-sig')