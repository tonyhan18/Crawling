for idx in range(1, math.ceil(len_pages)):
            remaked_detail = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
                "rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&totCnt={}&cortarNo={}&page={}"\
                .format(lgeo, lgeo, rletTpCds, tradTpCds, z2, lat2, lon2, count, cortarNo, idx)
            print(remaked_detail)
            
            details_res = requests.get(remaked_detail, headers=headers)
        
            # json.dumps()는 Python 객체를 JSON 문자열로 변환합니다.
            #이 경우, res2.json()으로 얻은 딕셔너리를 JSON 문자열로 변환합니다.
            try:
                json_str = json.loads(json.dumps(details_res.json()))
                soup = (str)(BeautifulSoup(details_res.text,"lxml"))
            except Exception as e:
                soup = (str)(BeautifulSoup(details_res.text,"lxml"))
                print(article)
                print(e)
            realestates = json_str['body']
            i =0
            
            for i in range(maximum_count):
                rs = realestates[i]
                atclNo = rs['atclNo']        # 물건번호 - 테스트용도
                rletTpNm = rs['rletTpNm']    # 상가구분
                tradTpNm = rs['tradTpNm']    # 매매/전세/월세 구분
                prc = rs['prc']              # 가격
                spc1 = round(float(rs['spc1'])*0.3025,2)    # 계약면적(m2) -> 평으로 계산 : * 0.3025
                spc2 = round(float(rs['spc2'])*0.3025,2)    # 전용면적(m2) -> 평으로 계산 : * 0.3025
                hanPrc = rs['hanPrc']        # 보증금                
                rentPrc = rs['rentPrc']      # 월세
                flrInfo = rs['flrInfo']      # 층수(물건층/전체층)
                tagList = rs['tagList']      # 기타 정보
                rltrNm = rs['rltrNm']        # 부동산
                detaild_information = "https://m.land.naver.com/article/info/{}".format(atclNo)
                
                # 표에 삽입될 데이터
                tablelist = [str(atclNo), str(rletTpNm), str(tradTpNm), str(format(prc, ','))+" 만원", str(spc1),
                str(spc2),str(hanPrc)+" 만원", str(format(rentPrc,',') +" 만원"),"7%"]
                
                tableview.insert("", 'end', values=tablelist)