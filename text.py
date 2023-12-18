def change_text (data_list):
    list = []
    error = []
    for data_index in (data_list):
        try :
            text = data_index[0] # data_index[0] : 標題
            #災情分類
            left = text.count("【")
            right = text.count("】")
            if (left == 2 and right == 2): # 【...】【...】
                text = text[text.find('【')+1:text.rfind('】')].split("】【")
            elif (left == 2): # 【...】【...
                text = text[text.find('【')+1:].split("】【")
            elif (right == 2 and text.find("】【") != -1): # ...】【...】
                text = text[:text.rfind('】')].split("】【")
            elif (right == 2 ): # 【...】...】
                text = text[text.find('【')+1:text.rfind('】')].split("】")
            elif ("-" in text): #【...-...】
                text = text[text.find('【')+1:text.rfind('】')].split("-")
                if (text[1].find('災') != -1 and (text[1].find('災') < text[1].find('日') or text[1].find('災') < text[1].find(':'))):
                    text_ = text[1].find('災') #【...-...災...】
                    text = [text[1][:text_+1],text[1][text_+1:]]
                elif(text[1].find("食物中毒")!=-1):
                    text = ["食物中毒",text[0]+text[1]]
            else: #【...】
                if (text.find('地震')!= -1):
                    text = ['地震',text[text.find('【')+1:text.rfind('】')]]
                elif(text.find('空勤直升機')!= -1):#山域事故
                    text = ['山域事故',text[text.find('【')+1:text.rfind('】')]]
                elif(text.find('空難')!= -1):#山域事故
                    text = ['空難',text[text.find('【')+1:text.rfind('】')]]
                elif(text.find('火災')!= -1):#山域事故
                    text = ['火災',text[text.find('【')+1:text.rfind('】')]]
                elif(text.find('電梯受困')!= -1):#山域事故
                    text = ['電梯受困',text[text.find('【')+1:text.rfind('】')]]
                else:
                    text = [' ',text[text.find('【')+1:text.rfind('】')]]
            l = [text[0]]
            text1 = text[1]
            #時間
            time = -1
            if (text1.find(':') != -1 and text1.find(':') < 13): # y/m/d h:m
                time = text1.find(':')+2
                if (text1[0].isdigit()):
                    l.append(text1[:time+1])
                else: #有其他符號
                    l.append(text1[1:time+1])
            elif (text1.find('日') != -1 and text1.find('日') < 11):#m月d日 d日
                time = text1.find('日')
                if (text1[0].isdigit()):
                    l.append(text1[:time+1])
                else: #有其他符號
                    l.append(text1[1:time+1])
            else:
                l.append(None)
            l.append(text1[time+1:])
            #print(time)
            if (text1.find('無傷亡') != -1):
                l.append('無傷亡')
            else:
                if (text1.find('焦屍') != -1 or text1.find('死') != -1 or text1.find('大體') != -1):
                    l.append('死亡')
                elif (text1.find('無生命徵象') != -1 or text1.find('OHCA') != -1):
                    l.append('無生命徵象')
                elif (text1.find('一氧化碳中毒') != -1):
                    l.append('一氧化碳中毒')
                elif (text1.find('高山症') != -1):
                    l.append('高山症')
                elif (text1.find('受困') != -1 or text1.find('失聯') != -1):
                    l.append('無傷亡')
                elif (text1.find('空勤直升機') != -1):
                    l.append('輕重傷')
                elif (text1.find('送醫') != -1 and text1.find('無需送醫') == -1):
                    l.append('輕重傷')
                elif (text1.find('傷') != -1 and text1.find('未受傷') == -1):
                    l.append('輕重傷')
                elif (text1.find('意識不清') != -1):
                    l.append('意識不清')
                else:
                    l.append('無傷亡')


            l.append(data_index[1]) # data_index[1] : 發布時間
            #print(l)
            list.append(l)
        except:
            error.append(text)
            print(text)
            continue
    
    return list