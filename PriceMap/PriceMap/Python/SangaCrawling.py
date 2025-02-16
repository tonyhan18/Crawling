import requests
from bs4 import BeautifulSoup
import json, math

# request 방식으로 할 경우
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}

# 서비스 제한이 걸렸을때의 해결책
class CustomException(Exception):
    pass

'''가격범위 프레임 ENV'''
price_ranges = {
    "1억 - 3억미만":"10000-30000",
    "3억 - 6억미만":"30000-60000",
    "6억 - 10억미만":"60000-100000",
    "10억 - 25억미만":"100000-250000",
    "25억 초과":"250000-10000000",
}

def SangGaCrawling():
    #btn_search.invoke()
    # TODO : 좀 더 나이스하게 이 부분을 바꾸는 방법 필요
    # DONE : 만약 사용자가 이상한 값을 넣었다면 어떻게 할 것인가의 해결책
    keyword = "구로구 구로동"
     
    # try :
            
    # finally:
    baseUrl = "https://m.land.naver.com/search/result/{}".format(keyword)
    print("baseUrl : "+baseUrl)
    res = requests.get(baseUrl, headers=headers)
    res.raise_for_status()    
    soup = (str)(BeautifulSoup(res.text,"lxml"))
        
    if(res.status_code != 200):
        raise CustomException 
        
    value = soup.split("filter: {")[1].split("}")[0].replace(" ","").replace("'","")
    lat = value.split("lat:")[1].split(",")[0]
    lon = value.split("lon:")[1].split(",")[0]
    z = value.split("z:")[1].split(",")[0]
    cortarNo = value.split("cortarNo:")[1].split(",")[0]
    #rletTpCds = value.split("rletTpCds:")[1].split(",")[0]
    #tradTpCds = value.split("tradTpCds:")[1].split(",")[0]
    sel_prc_rng = list(price_ranges["3억 - 6억미만"].split('-'))
    dprcMin = sel_prc_rng[0]
    dprcMax = sel_prc_rng[1]

    '''
    _rletTpCd = [{tagCd: 'APT', uiTagNm: '아파트'}, {tagCd: 'OPST', uiTagNm: '오피스텔'}, {tagCd: 'VL', uiTagNm: '빌라'},
                {tagCd: 'ABYG', uiTagNm: '아파트분양권'}, {tagCd: 'OBYG', uiTagNm: '오피스텔분양권'}, {tagCd: 'JGC', uiTagNm: '재건축'},
                {tagCd: 'JWJT', uiTagNm: '전원주택'}, {tagCd: 'DDDGG', uiTagNm: '단독/다가구'}, {tagCd: 'SGJT', uiTagNm: '상가주택'},
                {tagCd: 'HOJT', uiTagNm: '한옥주택'}, {tagCd: 'JGB', uiTagNm: '재개발'}, {tagCd: 'OR', uiTagNm: '원룸'},
                {tagCd: 'GSW', uiTagNm: '고시원'}, {tagCd: 'SG', uiTagNm: '상가'}, {tagCd: 'SMS', uiTagNm: '사무실'},
                {tagCd: 'GJCG', uiTagNm: '공장/창고'}, {tagCd: 'GM', uiTagNm: '건물'}, {tagCd: 'TJ', uiTagNm: '토지'},
                {tagCd: 'APTHGJ', uiTagNm: '지식산업센터'}];
    '''
    # DONE : 동적 할당 기능 필요
    rletTpCds = "SG"

    # DONE : A1=매매/B1=전세/B2=월세/B3=단기임대/*=전체 := 어짜피 매매밖에 안 쓴다
    tradTpCds = "A1"
    
    ###### New ARTICLE DATA
    # 아파트는 COMPLEX로 묶어서 사용이 가능
    # 상가는 ARTICLE로 사용(묶일 이유가 없음)
    # DONE: 상가는 COMPLEX를 사용할 수 없기 때문에 반드시 레인지 조건이 들어가야함
    remakedURL = "https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={}&rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&dprcMin={}&dprcMax={}&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false"\
        .format(cortarNo, rletTpCds, tradTpCds, z, lat, lon,dprcMin,dprcMax)
    print("remakedURL : " + remakedURL)

    res_complx = requests.get(remakedURL, headers=headers)
    #json_str = (str)(BeautifulSoup(res_complx.text,"lxml"))
    # TODO : 특정 article은 에러를 발생시킨다
    json_str = json.loads(json.dumps(res_complx.json()))
    article_list = json_str['data']['ARTICLE']
    #sel_prc_rng = list(price_ranges[selected.get()].split('-'))
    # 데이터 중에 prc가 없는 데이터도 있기 때문에 필터링 잘 거치어야 함
    article_list_fit = [article for article in article_list if ("prc" not in article)]
    regionName = json_str['cortar']['detail']['regionName']

    # 큰 원으로 구성되어 있는 전체 매물그룹(values)을 load 하여 한 그룹씩 세부 쿼리 진행
    '''
    https://m.land.naver.com/cluster/ajax/articleList?itemId=2120322202&mapKey=&lgeo=2120322202&showR0=&rletTpCd=SG&tradTpCd=A1&z=14&lat=37.4937&lon=126.8823&totCnt=25&cortarNo=1153010200&sort=rank&page=1
    '''

    j = 0
    for article in article_list_fit:
        print(j)
        j += 1
        lgeo = article['lgeo']
        count = article['count']
        z2 = article['z']
        lat2 = article['lat']
        lon2 = article['lon']

        len_pages = count / 20 + 1

        # 페이지별로 데이터 가지고 오기
        for idx in range(1, math.ceil(len_pages)):
            remaked_detail = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
                "rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&totCnt={}&cortarNo={}&page={}"\
                .format(lgeo, lgeo, rletTpCds, tradTpCds, z2, lat2, lon2, count, cortarNo, idx)
            print("remaked_detail : " + remaked_detail)
            
            details_res = requests.get(remaked_detail, headers=headers)
        
            # json.dumps()는 Python 객체를 JSON 문자열로 변환합니다.
            #이 경우, res2.json()으로 얻은 딕셔너리를 JSON 문자열로 변환합니다.
            try:
                json_str = json.loads(json.dumps(details_res.json()))
                realestates = json_str['body']
            except Exception as e:
                soup = (str)(BeautifulSoup(details_res.text,"lxml"))
                print(article)
                print(e)
            
            # DONE : 필요한 데이터 칼럼만 따서 만들기
            # https://m.land.naver.com/cluster/ajax/articleList?itemId=2103001011&mapKey=&lgeo=2103001011&showR0=&rletTpCd=SG&tradTpCd=A1&z=14&lat=36.5032849&lon=127.25004883&totCnt=17&cortarNo=3611011100&page=1
            # https://fin.land.naver.com/front-api/v1/article/basicInfo?articleId=2455894856&realEstateType=D02&tradeType=A1
            # 매매 : https://fin.land.naver.com/front-api/v1/article/basicInfo?articleId=2456304140&realEstateType=D02&tradeType=A1
            # 월세 : https://fin.land.naver.com/front-api/v1/article/basicInfo?articleId=2456931438&realEstateType=D02&tradeType=B2
                
            for rs in realestates:
                atclNo = rs['atclNo']          # 물건번호 - 테스트용도
                atclCfmYmd = str(rs['atclCfmYmd']).replace(".","")   # 물건등록일자
                rletTpNm = rs['rletTpNm']      # 상가구분
                rletTpCd = rs['rletTpCd']       # 디테일한 검색용
                prc = rs['prc']                # 가격
                tradTpNm = rs['tradTpNm']      # 매매/전세/월세 구분
                flrInfo = rs['flrInfo']        # 층수(물건층/전체층)
                spc1 = rs['spc1']    # 계약면적(m2)
                spc1P = round(float(rs['spc1'])*0.3025,2)   # 계약면적(m2) -> 평으로 계산 : * 0.3025
                spc2 = rs['spc2']    # 전용면적(m2)
                spc2P = round(float(rs['spc2'])*0.3025,2)    # 전용면적(m2) -> 평으로 계산 : * 0.3025
                atclFetrDesc = rs['atclFetrDesc'] if "atclFetrDesc" in rs else "" 
                detaild_information = "https://m.land.naver.com/article/info/{}".format(atclNo)
                direction=rs['direction']
                
                #hanPrc = rs['hanPrc']        # 보증금                
                #rentPrc = rs['rentPrc']      # 월세
                tagList = rs['tagList']      # 기타 정보
                rltrNm = rs['rltrNm']        # 부동산
                
                
                res_detail_info_url = "https://fin.land.naver.com/front-api/v1/article/basicInfo?articleId={}&realEstateType={}&tradeType={}".format(atclNo,rletTpCd,tradTpCds)
                print("res_detail_info_url : " + res_detail_info_url)
                res_deatil_info = requests.get(res_detail_info_url, headers=headers)
        
                # json.dumps()는 Python 객체를 JSON 문자열로 변환합니다.
                #이 경우, res2.json()으로 얻은 딕셔너리를 JSON 문자열로 변환합니다.
                try:
                    res_detail_info_json = json.loads(json.dumps(res_deatil_info.json()))
                    desc = str(res_detail_info_json['result']['detailInfo']['articleDetailInfo']['articleDescription']).replace(" ","")
                    price = res_detail_info_json['result']['priceInfo']['price']
                    previousDeposit = res_detail_info_json['result']['priceInfo']['previousDeposit']
                    previousMonthlyRent = res_detail_info_json['result']['priceInfo']['previousMonthlyRent']
                    buildingUse = res_detail_info_json['result']['detailInfo']['articleDetailInfo']['buildingUse']
                    curBisType = res_detail_info_json['result']['detailInfo']['spaceInfo']['currentBusinessType']
                    rltrPh = re.search(r"010.{10}", desc).group() if "010" in desc else "" #공인중개사 번호 뽑아내기
                    # 실재로 6% 넘는지 빠르게 계산하기 위해서는 (월세 * 20)이 (매매가 - 보증금) 보다 크면 됨
                    rateOfReturn = round((float(previousMonthlyRent) / (float(price) - float(previousDeposit))) * 1200, 2)
                    #print("월세 수익률 : " + previousMonthlyRent + " " + previousDeposit + " " + rateOfReturn)
                except Exception as e:
                    soup = (str)(BeautifulSoup(res_deatil_info.text,"lxml"))
                    print(article)
                    print(e)
                    
                # 평단가
                equilibriumPrice = round(prc / spc2P,2)            
                
                
                if (atclNo == "2454818411"):
                    break
                # 표에 삽입될 데이터
                # TODO : 지역명 넣는 방법 필요한
                # TODO : 층별로 데이터를 나누어서 받아오게 수정
                if (curBisType is None and previousMonthlyRent == 0):
                    continue
                tablelist = [
                    str(atclNo), # 매물번호
                    str(atclCfmYmd), # 물건등록일자
                    str(rletTpNm), # 물건 구분
                    str(rateOfReturn), #월세 수익률
                    str(price), #매매가
                    str(previousDeposit), #기보증금
                    str(previousMonthlyRent), #월세
                    str(curBisType), #현재업종
                    str(flrInfo).split('/')[0], #현재층
                    str(spc1P), #계약평형
                    str(spc2P), #전용평형
                    str(equilibriumPrice), #평단가(가격/전용평형)
                    str(atclFetrDesc), #매물특징
                    str(spc1), #계약면적
                    str(spc2), #전용면적
                    str(detaild_information), #링크
                    str(regionName), #소재지
                    str(direction), #방향
                    str(buildingUse), #추천업종
                    str(("Y" if any("주차" in tag for tag in tagList) else "N")), # 주차가능
                    str(flrInfo).split('/')[1], #전체층
                    str(rltrNm), #중개사
                    str(rltrPh), #중개사전화
                ]
                
                # tableview.insert("", 'end', values=tablelist)
    # ....
    # #엑셀시트에 데이터 append
    # ws.append([str(rletTpNm), str(tradTpNm), str(prc * 10000), str(spc1),
    #             str(spc2),
    #             str(hanPrc), str(rentPrc * 10000),
    #             str(flrInfo),str(tagList),
    #             str(rltrNm), detaild_information])
    # ....
    
    
    #검색 완료 후 엑셀 저장 버튼 활성화
    #btn_exportexcel.config(state="active")
    return tablelist

if __name__ == "__main__":
    tablelist = SangGaCrawling()
    print(tablelist)