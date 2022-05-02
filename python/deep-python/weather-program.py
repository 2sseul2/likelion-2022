# API를 이용하여 날씨 정보를 출력하는 프로그램

# https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}

import requests
import json

city = "Seoul"
apiKeys = "a2928e1327806ad26bd3fa3cb3e5019a"
lang = "kr"


# API 요청을 보낼 API 서버의 주소
# ? 뒤에 language 추가
# 화씨 -> 섭씨 : units 추가

api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKeys}&lang={lang}&units=metric"

result = requests.get(api)

# response [200] : 요청에 대한 응답 성공적.
print(result.text)

# str
type(result.text)

# json 타입으로 변경해줌.
data = json.loads(result.text)
type(data) # dict 

print(data["name"],"의 날씨입니다.")
print("날씨는 ",data["weather"][0]["description"],"입니다.")
print("현재 온도는 ",data["main"]["temp"],"입니다.")
print("하지만 체감 온도는 ",data["main"]["feels_like"],"입니다.")
print("최저 기온은 ",data["main"]["temp_min"],"입니다.")
print("최고 기온은 ",data["main"]["temp_max"],"입니다.")
print("습도는 ",data["main"]["humidity"],"입니다.")
print("기압은 ",data["main"]["pressure"],"입니다.")
print("풍향은 ",data["wind"]["deg"],"입니다.")
print("풍속은 ",data["wind"]["speed"],"입니다.")
