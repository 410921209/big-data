import pandas as pd
import func,text
from datetime import datetime
#from apyori import apriori
#from mlxtend.preprocessing import TransactionEncoder
#import random

Data = pd.read_csv("G:/我的雲端硬碟/big_data/Disaster.csv",encoding='utf-8-sig')
data_list = Data.values.tolist()
df = pd.DataFrame(text.change_text(data_list))
df.columns = ["災情","資料時間","詳細資料","傷亡情況","發布時間"]
df_drop_dup = df.drop_duplicates(subset=["災情","資料時間","詳細資料"],ignore_index=True)

index = max(df_drop_dup.index[(df_drop_dup["發布時間"] == "112-12-15")].tolist())

df_drop_dup_copy = df_drop_dup.copy()
df_drop_dup_copy = df_drop_dup_copy.iloc[:index+1]
df_drop_dup_copy["發生日期"] = df_drop_dup_copy.apply(lambda r: func.change_date(r['發布時間'], r['資料時間']), axis=1) #Occurrence Date
df_drop_dup_copy["發生時間"] = df_drop_dup_copy.apply(lambda r: func.change_time(r['資料時間']), axis=1) #Occurrence Time
df_drop_dup_copy["Year"] = df_drop_dup_copy.apply(lambda r: str(r['發生日期'].year), axis=1)
df_drop_dup_copy["Month"] = df_drop_dup_copy.apply(lambda r: r['發生日期'].month, axis=1)
df_drop_dup_copy["Weekday"] = df_drop_dup_copy.apply(lambda r: r['發生日期'].isoweekday(), axis=1)
df_drop_dup_copy["Hour"] = df_drop_dup_copy.apply(lambda r: str(func.change_hour(r['發生時間'])), axis=1)
df_drop_dup_copy = df_drop_dup_copy[df_drop_dup_copy["Year"] != "2021"]

dataframe_CH = df_drop_dup_copy[["災情","發生日期","發生時間","詳細資料","Year","Month","Weekday","Hour","傷亡情況"]].sort_values(by='發生日期',ignore_index=True)

dataframe_CH_copy = dataframe_CH.copy()
dataframe_CH_copy["災情"] = dataframe_CH_copy["災情"].replace(["消防快訊"],"住宅火災")
dataframe_CH_copy["發生地點"] = dataframe_CH_copy['詳細資料'].map(func.change_county_ch)
dataframe_CH_copy["災情分類"] = dataframe_CH_copy['災情'].map(func.change_class_ch)
dataframe_CH_copy["Disaster"] = dataframe_CH_copy["災情分類"].map(func.disaster_dict).astype(int)
dataframe_CH_copy["County"] = dataframe_CH_copy["發生地點"].map(func.county_dict).astype(int)
dataframe_CH_copy["Casualty"] = dataframe_CH_copy["傷亡情況"].map(func.casualty_level_dict).astype(str)

dataframe_CH_copy = dataframe_CH_copy.sort_values(by='Disaster',ignore_index=True)
detailed_disaster_dict = {dataframe_CH_copy["災情"].unique()[i] : i for i in range(len(dataframe_CH_copy["災情"].unique()))}
dataframe_CH_copy["Detailed disaster"] = dataframe_CH_copy["災情"].map(detailed_disaster_dict).astype(int)

dataframe_ch = dataframe_CH_copy[["災情分類","災情","發生地點","發生日期","Year","Month","Weekday","發生時間","Hour","傷亡情況","詳細資料","Disaster","Detailed disaster","County","Casualty"]]

print(dataframe_ch)
dataframe_ch.to_csv("G:/我的雲端硬碟/big_data/Disaster_process.csv", index=False,encoding='utf-8-sig')
"""
print(func.disaster_dict)
print(func.county_dict)
print(func.casualty_level_dict,end="\n\n")
print(detailed_disaster_dict)
"""