# 출처: https://cocoabba.tistory.com/58 [새로운 시작~!:티스토리]
import requests
from bs4 import BeautifulSoup
import json, math

import tkinter as tk
import tkinter.ttk
import tkinter.messagebox as msgbox




City="구로구 구로동"
url = "https://m.land.naver.com/search/result/{}".format(City) 

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'}
res = requests.get(url, headers=headers)

'''
BeautifulSoup이란 스크래핑을 하기위해 사용하는 패키지이고, 
BeautifulSoup은 response.text를 통해 가져온 HTML 문서를 탐색해서 원하는 부분을 뽑아내는 그런 역할을 하는 라이브러리이다.

lxml은 구문을 분석하기 위한 parser이다.
lxml을 통하여 의미있는 HTML문서로 변환하는 것이다.
'''
soup = (str)(BeautifulSoup(res.text,"lxml"))

#  filter: {
#             lat: '37.550985', : latitude 위도
#             lon: '126.849534', : longitude 경도
#             z: '12',
#             cortarNo: '1150000000',
#             cortarNm: '강서구',
#             rletTpCds: '*',
#             tradTpCds: 'A1:B1:B2'
#         },
value = soup.split("filter: {")[1].split("}")[0].replace(" ","").replace("'","")

lat = value.split("lat:")[1].split(",")[0]
lon = value.split("lon:")[1].split(",")[0]
z = value.split("z:")[1].split(",")[0]
cortarNo = value.split("cortarNo:")[1].split(",")[0]
rletTpCds = value.split("rletTpCds:")[1].split(",")[0]
tradTpCds = value.split("tradTpCds:")[1].split(",")[0]


'''
_rletTpCd = [{tagCd: 'APT', uiTagNm: '아파트'}, {tagCd: 'OPST', uiTagNm: '오피스텔'}, {tagCd: 'VL', uiTagNm: '빌라'},
            {tagCd: 'ABYG', uiTagNm: '아파트분양권'}, {tagCd: 'OBYG', uiTagNm: '오피스텔분양권'}, {tagCd: 'JGC', uiTagNm: '재건축'},
            {tagCd: 'JWJT', uiTagNm: '전원주택'}, {tagCd: 'DDDGG', uiTagNm: '단독/다가구'}, {tagCd: 'SGJT', uiTagNm: '상가주택'},
            {tagCd: 'HOJT', uiTagNm: '한옥주택'}, {tagCd: 'JGB', uiTagNm: '재개발'}, {tagCd: 'OR', uiTagNm: '원룸'},
            {tagCd: 'GSW', uiTagNm: '고시원'}, {tagCd: 'SG', uiTagNm: '상가'}, {tagCd: 'SMS', uiTagNm: '사무실'},
            {tagCd: 'GJCG', uiTagNm: '공장/창고'}, {tagCd: 'GM', uiTagNm: '건물'}, {tagCd: 'TJ', uiTagNm: '토지'},
            {tagCd: 'APTHGJ', uiTagNm: '지식산업센터'}];
'''
rletTpCds = "SG"

# A1=매매/B1=전세/B2=월세/B3=단기임대/*=전체
tradTpCds = "A1"

'''
https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo=1153010200&rletTpCd=SG&tradTpCd=A1&z=14&lat=37.4937&lon=126.8823&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false

https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo=1153010200&rletTpCd=APT&tradTpCd=A1:B1:B2&z=14&lat=37.4937&lon=126.8823&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false

https://m.land.naver.com/cluster/clusterList?view=actl&cortarNo=1153010200&rletTpCd=APT&tradTpCd=*&z=14&lat=37.4937&lon=126.8823&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false

https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo=1153010200&rletTpCd=SG&tradTpCd=A1:B1:B2&z=14&lat=37.4937&lon=126.8823&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false
'''

###### New ARTICLE DATA
# 아파트는 COMPLEX로 묶어서 사용이 가능
# 상가는 ARTICLE로 사용(묶일 이유가 없음)
remaked_URL = "https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={}&rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false"\
    .format(cortarNo, rletTpCds, tradTpCds, z, lat, lon)

res2 = requests.get(remaked_URL, headers=headers)
json_str = json.loads(json.dumps(res2.json()))

values = json_str['data']['ARTICLE']

# 큰 원으로 구성되어 있는 전체 매물그룹(values)을 load 하여 한 그룹씩 세부 쿼리 진행
'''
https://m.land.naver.com/cluster/ajax/articleList?itemId=2120322202&mapKey=&lgeo=2120322202&showR0=&rletTpCd=SG&tradTpCd=A1&z=14&lat=37.4937&lon=126.8823&totCnt=25&cortarNo=1153010200&sort=rank&page=1
'''

for v in values:
    lgeo = v['lgeo']
    count = v['count']
    z2 = v['z']
    lat2 = v['lat']
    lon2 = v['lon']

    len_pages = count / 20 + 1

    for idx in range(1, math.ceil(len_pages)):
        remaked_URL2 = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
            "rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&totCnt={}&cortarNo={}&page={}"\
            .format(lgeo, lgeo, rletTpCds, tradTpCds, z2, lat2, lon2, count,cortarNo, idx)
        res3 = requests.get(remaked_URL2, headers=headers)
        
        # json.dumps()는 Python 객체를 JSON 문자열로 변환합니다.
        #이 경우, res2.json()으로 얻은 딕셔너리를 JSON 문자열로 변환합니다.
        json_str = json.loads(json.dumps(res3.json()))

        realestates = json_str['body']
        
        for rs in realestates:
            atclNo = rs['atclNo']        # 물건번호
            rletTpNm = rs['rletTpNm']    # 상가구분
            tradTpNm = rs['tradTpNm']    # 매매/전세/월세 구분
            prc = rs['prc']              # 가격
            spc1 = rs['spc1']*0.3025    # 계약면적(m2) -> 평으로 계산 : * 0.3025
            spc2 = rs['spc2']*0.3025    # 전용면적(m2) -> 평으로 계산 : * 0.3025
            hanPrc = rs['hanPrc']        # 보증금                
            rentPrc = rs['rentPrc']      # 월세
            flrInfo = rs['flrInfo']      # 층수(물건층/전체층)
            tagList = rs['tagList']      # 기타 정보
            rltrNm = rs['rltrNm']        # 부동산
            detaild_information = "https://m.land.naver.com/article/info/{}".format(atclNo)
            
            tablelist = [str(rletTpNm), str(tradTpNm), str(format(prc, ','))+" 만원", str(spc1),
                str(spc2),str(hanPrc)+" 만원", str(format(rentPrc,',') +" 만원"),"7%"]
                
            tableview.insert("", 'end', values=tablelist)
        
print("hello")