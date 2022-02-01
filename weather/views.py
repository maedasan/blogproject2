from django.shortcuts import render, redirect
import requests
import json
from datetime import datetime,timedelta,timezone
from django.views.generic import FormView
from .forms import WeatherForm
from django.urls import reverse_lazy
import pandas as pd
import numpy as np
from django.http import HttpResponse
import pickle


#天気検索アプリ
class Weatherday(FormView):
    template_name = 'weather_input.html'
    form_class = WeatherForm

    def form_valid(self, form):
        #入力データの確保
        form_city_name= form.data.get("city_name")
        form_select_day= form.data.get("select_day")

        if form_select_day == "1day":#現在の予報
            url="http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&lang=ja&units=metric"
            url=url.format(city=form_city_name,key="ご自身でAPIkey取得してください。サイト名、OpenWeather")
            #天気データをジョンソンで取得
            jsondata=requests.get(url).json()

            if '404' != jsondata['cod'] :#入力データで天気情報を得ているか判定
                #世界時間を日本時間に調整
                tz= timezone(timedelta(hours=+9),"JST")
                japantime= str(datetime.fromtimestamp(jsondata["dt"],tz))[:-9]
                #データフレーム作成
                df=pd.DataFrame(
                    data=np.array([[japantime,jsondata["name"],jsondata["sys"]["country"],
                    str(jsondata["main"]["temp"]),str(jsondata["main"]["feels_like"]),jsondata["weather"][0]["main"],
                    jsondata["weather"][0]["description"],str(jsondata["wind"]["speed"])]]),
                    columns=["日時","地名","国名","気温","体感気温","天気","天気詳細","風速"])
                
                #検索データの一時保存
                with open('weather_df.csv', mode='wb') as f:
                    pickle.dump(df, f)
                #検索時のselect_dayを一時保存
                with open('select_day.txt', mode='wb') as f:
                    pickle.dump(form_select_day, f)


                #結果の表示
                return render(self.request, 'weather_output1day.html',{'df':df})

            else:
                #検索エラー時の表示
                return render(self.request, 'weather_error.html', {'error':'検索対象外の地名、又は入力文字に誤りがあります。'})


        else:#５日間の予報
            url="http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&lang=ja&units=metric"
            url=url.format(city=form_city_name,key="ご自身でAPIkey取得してください。サイト名、OpenWeather")
            #天気データをジョンソンで取得
            jsondata=requests.get(url).json()
            
            if '404' != jsondata['cod'] :#入力データで天気情報を得ているか判定
                df=pd.DataFrame(columns=["気温"])
                index= 0
                #世界時間を日本時間に調整
                tz=timezone(timedelta(hours=+9),"JST")
                for dat in jsondata["list"]:
                    jptime=str(datetime.fromtimestamp(dat["dt"],tz))[:-9]
                    #データフレームの作成
                    if index == 0:
                        df=pd.DataFrame(
                            data=np.array([[jptime,jsondata["city"]["name"],jsondata["city"]["country"],
                            str(dat["main"]["temp"]),str(dat["main"]["feels_like"]),dat["weather"][0]["main"],
                            dat["weather"][0]["description"],str(dat["wind"]["speed"])]]),
                            columns=["日時","地名","国名","気温","体感気温","天気","天気詳細","風速"])
                        index += 1
                    else:
                        df.loc[index]=np.array([jptime,jsondata["city"]["name"],jsondata["city"]["country"],
                        str(dat["main"]["temp"]),str(dat["main"]["feels_like"]),dat["weather"][0]["main"],
                        dat["weather"][0]["description"],str(dat["wind"]["speed"])])
                        index += 1
                        
                #検索データの一時保存
                with open('weather_df.csv', mode='wb') as f:
                    pickle.dump(df, f)
                #検索時のselect_dayを一時保存
                with open('select_day.txt', mode='wb') as f:
                    pickle.dump(form_select_day, f)
                
                
                #結果の表示
                return render(self.request, 'weather_output5day.html', {'df':df })

            else:
                #検索エラー時の表示
                return render(self.request, 'weather_error.html', {'error':'検索対象外の地名、又は入力文字に誤りがあります。'})



#天気検索結果のcsv形式ダウンロード出力
def csv_download(request):
    with open('weather_df.csv', mode='rb') as f:
        df_weather = pickle.load(f)
    with open('select_day.txt', mode='rb') as f:
        day_select= pickle.load(f)
    
    if day_select == '1day':
        f_name = df_weather.iloc[0,0]
    else:
        f_name = df_weather.iloc[0,0] + '//' + df_weather.iloc[39,0]
    response = HttpResponse(content_type='text/csv; charset=cp932')
    response['Content-Disposition'] = 'attachment; filename ="' + f_name + '.csv"'
    df_weather.to_csv(path_or_buf=response, sep=",", index=False)
    return response