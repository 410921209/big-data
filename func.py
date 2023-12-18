from datetime import datetime

ch_county = ["臺北市","新北市","基隆市","新竹市","桃園市","新竹縣","宜蘭縣",
      "臺中市","苗栗縣","彰化縣","南投縣","雲林縣",
      "高雄市","臺南市","嘉義市","嘉義縣","屏東縣","澎湖縣",
      "花蓮縣","臺東縣",
      "金門縣","連江縣","其他或無"]
ch_disaster = ["火災","化學災害","一氧化碳中毒","交通事故","地震","山域事故","災害救助","其他"]
county_dict = {ch_county[i] : i for i in range(len(ch_county))}
disaster_dict = {ch_disaster[i] : i for i in range(len(ch_disaster))}
casualty_level_dict = {"無傷亡" : 0 ,"死亡" : 2 ,"無生命徵象" : 2 ,"一氧化碳中毒" : 1 ,"高山症" : 1 ,"輕重傷" : 1 ,"意識不清" : 1 }


def change_date(Announce,Occurrence):
  #發布時間
  date_Announce = [int(i) for i in Announce.split("-")]
  date_Announce[0] += 1911
  day_Announce = date_Announce[2]

  #發生時間
  if (Occurrence == None):
    date = datetime(year=date_Announce[0], month=date_Announce[1], day=date_Announce[2]).date()
  elif ("年" in Occurrence):
    split_Occurrence = Occurrence.split("年")
    year_Occurrence = (int)(split_Occurrence[0])+1911
    split_Occurrence = split_Occurrence[1].split("月")
    month_Occurrence = (int)(split_Occurrence[0])
    day_Occurrence = (int)(split_Occurrence[1].split("日")[0])
    date = datetime(year=year_Occurrence, month=month_Occurrence, day=day_Occurrence).date()
  elif ("月" in Occurrence):
    split_Occurrence = Occurrence.split("月")
    month_Occurrence = (int)(split_Occurrence[0])
    day_Occurrence = (int)(split_Occurrence[1].split("日")[0])
    if (date_Announce[1] == 1 and month_Occurrence == 12):
      date = datetime(year=date_Announce[0]-1, month=12, day=day_Occurrence).date()
    else:
      date = datetime(year=date_Announce[0], month=month_Occurrence, day=day_Occurrence).date()
  elif("/" in Occurrence): # y/m/d h:m
    date_Occurrence = [int(i) for i in Occurrence.split(" ")[0].split("/")] # y/m/d h:m -> y/m/d
    date = datetime(year=date_Occurrence[0]+1911, month=date_Occurrence[1], day=date_Occurrence[2]).date()
  elif("日" in Occurrence):
    day_Occurrence = (int)(Occurrence.split("日")[0])
    if (day_Announce >= day_Occurrence or day_Announce > 10):
      date = datetime(year=date_Announce[0], month=date_Announce[1], day=day_Occurrence).date()
    elif (day_Announce < day_Occurrence):
      if (date_Announce[1] == 1):
        date = datetime(year=date_Announce[0]-1, month=12, day=day_Occurrence).date()
      else:
        date = datetime(year=date_Announce[0], month=date_Announce[1]-1, day=day_Occurrence).date()
  else:
    date = datetime(year=date_Announce[0], month=date_Announce[1], day=date_Announce[2]).date()
  return date

def change_time(Occurrence):
  #發生時間
  if (Occurrence == None):
    time = "No data"
  elif (":" in Occurrence):
    colon = Occurrence.find(':')
    if Occurrence[colon-1].isdigit():
      time = Occurrence[colon-(Occurrence[colon-2].isdigit())-1:colon+3]
    else:
      time = "No data"
  else:
    time = "No data"
  return time

def change_hour(Occurrence):
  #發生時間
  if (":" in Occurrence):
      colon = Occurrence.find(':')
      time = int(Occurrence[:colon])
  else:
    time = -1
  return time

def change_county_ch(data):
  for i in ch_county:
    if data.find(i) != -1:
      return i
  if data.find("台中") != -1 or data.find("臺中") != -1:
    return "臺中市"
  elif data.find("台北") != -1 or data.find("臺北") != -1:
    return "臺北市"
  elif data.find("台南") != -1:
    return "臺南市"
  elif data.find("高雄") != -1:
    return "高雄市"
  elif data.find("屏東") != -1:
    return "屏東縣"
  elif data.find("台東") != -1 or data.find("臺東") != -1:
    return "臺東縣"
  elif data.find("花蓮") != -1:
    return "花蓮縣"
  elif data.find("彰化") != -1:
    return "彰化縣"
  elif data.find("淡水") != -1:
    return "新北市"
  elif data.find("苗栗") != -1:
    return "苗栗縣"
  return "其他或無"

def change_class_ch(data):
  if data.find("火") != -1:
    return ch_disaster[0]
  elif data.find("化學災害") != -1 or data.find("瓦斯氣爆") != -1:
    return ch_disaster[1]
  elif data.find("一氧化碳中毒") != -1:
    return ch_disaster[2]
  elif data.find("交通事故") != -1 or data.find("車禍救護") != -1:
    return ch_disaster[3]
  elif data.find("地震") != -1:
    return ch_disaster[4]
  elif data.find("山域事故") != -1 or data.find("空中緊急救護") != -1:
    return ch_disaster[5]
  elif data.find("災害救助") != -1 or data.find("受困") != -1:
    return ch_disaster[6]
  return ch_disaster[7]
