Sub 네이버부동산크롤링()
 
Application.ScreenUpdating = False
Application.EnableEvents = False
 
    NaverLandCrawl Sheet1.Range("D5").Value, Sheet1.Range("E5").Value
 
Application.ScreenUpdating = True
Application.EnableEvents = True
 
End Sub
 
Sub 초기화()
 
Dim shp As Shape
 
For Each shp In Sheet1.Shapes
    If Left(shp.Name, 3) <> "btn" Then shp.Delete
Next
 
With Sheet1
    .Range(.Cells(9, 4), .Cells(GetLastRow(Sheet1), 29)).ClearContents
    .Range(.Cells(9, 4), .Cells(GetLastRow(Sheet1), 29)).RowHeight = 18
End With
 
End Sub


Sub NaverLandCrawl(city As String, isImage As Boolean)
 
'##########################################################
' 변수 설정
Dim htmlResult As Object
Dim strResult As String
Dim URL As String
 
'##########################################################
'1. 네이버 부동산 메인 페이지 -> 지역 검색
'                             -> 가용 매물 목록을 받아오기 위한 위/경도, 그 외 변수 추출
'[            https://meyerweb.com/eric/tools/dencoder/                ]  '-> URL 디코딩/인코딩
'[            http://json.parser.online.fr/                                             ]  '-> JSON 파서
 
URL = "https://m.land.naver.com/search/result/" & city
 
'--------------------------------------------
' 2021.01.29 수정
' 네이버 부동산 접속경로가 302 redirect 되면서 html 파싱 방법이 변경되었습니다.
' 따라서 redirect 된 URL에서 값을 받아 오도록 명령문을 수정하였는데요.
' 지난번 네이버 로그인 강의 이후에도 동일한 상황이 있었는데요. 이번에도 강의 업로드 이후 네이버에서 관련 정책을 바꾸는 관계로 2차 수정을 하였습니다.
' 크롤링이라는 것은 어느 인터넷 정보제공자라도 원치 않는 작업일 것입니다.
' 이번 2차 수정을 마지막으로 네이버 부동산 웹크롤링 코드는 수정을 종료하려고 합니다.
' 감사합니다.
 
'---------------------------------------
'Set htmlResult = GetHttp(URL)
'strResult = htmlResult.body.innerHTML
'strResult = Splitter(strResult, "filter: {", "},")
 
Dim vResult As Variant
Dim idx As Long
strResult = GetRedirectURL(URL)
strResult = Splitter(strResult, "/map/", "?")
strResult = Replace(strResult, "/*/", ":")
 
vResult = Split(strResult, ":")
 
'----------------------------------------
' 매물유형 예) 아파트: APT, 빌라 : VL, 오피스텔: OPST, ...적절히 수정
' 건물유형 A1, B1, ... 적절히 수정가능
'----------------------------------------
 
'---------------- 해당 지역(메인) 위/경도 + 그 외 변수 생성
Dim lat As String: lat = vResult(0)
Dim lon As String: lon = vResult(1)
Dim z As String: z = vResult(2)
Dim cortarNo As String: cortarNo = vResult(3)
Dim searchType As String: searchType = "APT"
Dim buildingType As String
For idx = 4 To UBound(vResult)
    buildingType = buildingType & vResult(idx) & ":"
Next
buildingType = Left(buildingType, Len(buildingType) - 1)
 
'------------------------------------------------------------------------------------------------
 
'#########################################################
' 2. 네이버 부동산 지도 페이지 -> 받아온 위/경도, 그 외 변수로 검색
'                                                -> 해당 지역 가용매물 목록의 상세 위/경도 추출
 
Debug.Print "2"
URL = "https://m.land.naver.com/cluster/clusterList?view=actl&cortarNo=" & cortarNo & "&rletTpCd=" & searchType & "&tradTpCd=" & buildingType & _
            "&z=" & z & "&lat=" & lat & "&lon=" & lon & "&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false"
 
Set htmlResult = Nothing
Set htmlResult = GetHttp(URL)
strResult = htmlResult.body.innerHTML

 
Dim forceCOMPLEX As Boolean
If InStr(1, strResult, "COMPLEX") > 0 Then strResult = Splitter(strResult, "COMPLEX"): forceCOMPLEX = True
Dim v As Variant
v = ParseJSON(strResult, "lgeo,lat,lon,count")
 
'##########################################################
' 3. 네이버 부동산 매물페이지  -> 상세 위 경도로 매물 정보 검색
'                                                -> 각 매물별 상세정보 추출
' 매물페이지는 페이지당 20개씩만 출력.. 그래서 추가 작업 필요!
' Set htmlResult = Nothing
' Set htmlResult = GetHttp(URL)
'                strResult = htmlResult.body.innerHTML
'                vReturn = ParseJSON(strResult, "hscpNm,hscpNo,scpTypeCd,hscpTypeNm,totDongCnt,totHsehCnt,genHsehCnt,useAprvYmd,repImgUrl,dealCnt,leaseCnt,rentCnt," & _
                                             "strmRentCnt,totalAtclCnt,minSpc,maxSpc,dealPrcMin,dealPrcMax,leasePrcMin,leasePrcMax,isalePrcMin,isalePrcMax,isaleNotifSeq,isaleScheLabel,isaleScheLabelPre", city, "<em class="txt_unit">,</em>")
 
Dim i As Long: Dim iPage As Long: Dim j As Long
Dim vReturn As Variant
Dim x As Long: x = GetLastRow(Sheet1) + 1
Dim initR As Long
initR = x
 
For i = LBound(v, 1) To UBound(v, 1)
    If v(i, 1) <> "" Then
        iPage = Application.WorksheetFunction.RoundUp(v(i, 4) / 20, 0)
        For j = 1 To iPage
        If forceCOMPLEX = False Then
            URL = "https://m.land.naver.com/cluster/ajax/articleList?itemId=" & v(i, 1) & "&lgeo=" & v(i, 1) & _
                            "&rletTpCd=" & searchType & "&tradTpCd=" & buildingType & "&z=" & z & "&lat=" & v(i, 2) & "&lon=" & v(i, 3) & "&cortarNo=" & cortarNo & _
                            "&isOnlyIsale=false&sort=readRank&page=" & j
            Debug.Print URL
            Set htmlResult = Nothing
            Set htmlResult = GetHttp(URL)
            strResult = htmlResult.body.innerHTML
            If InStr(1, strResult, "atclNo") > 0 Then
                vReturn = ParseJSON(strResult, "atclNm,atclNo,tradTpCd,rletTpNm,totDongCnt_tmp,totHsehCnt_tmp,genHsehCnt_tmp,atclCfmYmd,repImgUrl,tradTpNm,flrInfo,atclTetrDesc," & _
                                "strmRentCnt_tmp,totalAtclCnt_tmp,spc1,spc2,sameAddrMinPrc,sameAddrMaxPrc,minMviFee,maxMviFee,cpid,cpNm,rltrNm,isaleScheLabel_tmp,isaleScheLabelPre_tmp", city, "<em class="">,</em>")
                ArrayToRng Sheet1.Cells(x, 4), vReturn
                x = x + UBound(vReturn, 1)
            End If
        Else
            URL = "https://m.land.naver.com/cluster/ajax/complexList?itemId=" & v(i, 1) & "&lgeo=" & v(i, 1) & _
                    "&rletTpCd=" & searchType & "&tradTpCd=" & buildingType & "&z=" & z & "&lat=" & v(i, 2) & "&lon=" & v(i, 3) & "&cortarNo=" & cortarNo & "&isOnlyIsale=false&sort=readRank&page=" & j
            Set htmlResult = Nothing
            Set htmlResult = GetHttp(URL)
            strResult = htmlResult.body.innerHTML
            If InStr(1, strResult, "hscpNo") > 0 Then
                vReturn = ParseJSON(strResult, "hscpNm,hscpNo,scpTypeCd,hscpTypeNm,totDongCnt,totHsehCnt,genHsehCnt,useAprvYmd,repImgUrl,dealCnt,leaseCnt,rentCnt," & _
                                "strmRentCnt,totalAtclCnt,minSpc,maxSpc,dealPrcMin,dealPrcMax,leasePrcMin,leasePrcMax,isalePrcMin,isalePrcMax,isaleNotifSeq,isaleScheLabel,isaleScheLabelPre", city, "<em class="">,</em>")
                ArrayToRng Sheet1.Cells(x, 4), vReturn
                x = x + UBound(vReturn, 1)
            End If
        End If
        Next
    End If
Next
 
 
'#########################################################
' 4. 대표 이미지 삽입
If isImage = True Then
    Dim shpImg As Shape: Dim shpRng As Range
    For j = initR To Sheet1.Cells(Sheet1.Rows.Count, 4).End(xlUp).Row + 1
        Set shpRng = Sheet1.Cells(j, 13)
        If shpRng.Value <> "" Then
            shpRng.EntireRow.RowHeight = 80
            InsertWebImage shpRng, "https://landthumb-phinf.pstatic.net" & shpRng.Value
        Else
            shpRng.EntireRow.RowHeight = 18
        End If
    Next
End If
 
End Sub


