from django import forms

day=(("1day","現在の気象情報"),("5day","５日間の気象情報"))

#コメント投稿フォーム
class WeatherForm(forms.Form):
    city_name= forms.CharField(label="地名")
    select_day = forms.ChoiceField(choices=day, label="現在 or 5日間")