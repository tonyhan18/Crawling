Sub NaverBlogCrawl()

Dim s As String
Dim v As Variant: Dim va As Variant: Dim i As Long: Dim a As Variant
Dim obj As Object

Dim href As Variant

Dim keyword As String: keyword = ENCODEURL(Sheet1.Range("C4").Value)

Set obj = GetHttp("https://search.naver.com/search.naver?where=view&sm=tab_jum&query=" & keyword, includeMeta:=True)

Set v = obj.getElementsByClassName("total_tit")

ReDim va(1 To v.Length)
ReDim href(1 To v.Length)

i = 1
For Each a In v
    va(i) = Replace(Replace(a.innerhtml, "<mark>", ""), "</mark>", "")
    i = i + 1
Next

i = 1
For Each a In v
    href(i) = a.href
    i = i + 1
Next

ArrayToRng Sheet1.Range("F6"), va
ArrayToRng Sheet1.Range("G6"), href

ExportText obj.body.innerhtml

End Sub

Function ENCODEURL(varText As Variant, Optional blnEncode = True)
 
'############################################################
'한글/영문 텍스트를 URL 주소로 변경합니다.
'https://www.oppadu.com/vba-encodeurl-함수/
'############################################################
 
Static objHtmlfile As Object
 
If objHtmlfile Is Nothing Then
    Set objHtmlfile = CreateObject("htmlfile")
    With objHtmlfile.parentWindow
    .execScript "function encode(s) {return encodeURIComponent(s)}", "jscript"
    End With
End If
 
If blnEncode Then
    ENCODEURL = objHtmlfile.parentWindow.encode(varText)
End If
 
End Function

Sub ArrayToRng(startRng As Range, Arr As Variant, Optional ColumnNo As String = "")
 
'###############################################################
'오빠두엑셀 VBA 사용자지정함수 (https://www.oppadu.com)
'▶ ArrayToRng 함수
'▶ 배열을 범위 위로 반환합니다.
'▶ 인수 설명
'_____________startRng      : 배열을 반환할 기준 범위(셀) 입니다.
'_____________Arr               : 반환할 배열입니다.
'_____________ColumnNo   : [선택인수] 배열의 특정 열을 선택하여 범위로 반환합니다. 여러개 열을 반환할 경우 열 번호를 쉼표로 구분하여 입력합니다.
'                                               값으로 공란을 입력하면 열을 건너뜁니다.
'▶ 사용 예제
'Dim v As Variant
'ReDim v(0 to 1)
''v(0) = "a" : v(1) = "b"
'ArrayToRng Sheet1.Range("A1"), v
'▶ 사용된 보조 명령문
'Extract_Column 함수
'##############################################################
 
On Error GoTo SingleDimension:
 
Dim Cols As Variant: Dim Col As Variant
Dim X As Long: X = 1
If ColumnNo = "" Then
    startRng.Cells(1, 1).Resize(UBound(Arr, 1) - LBound(Arr, 1) + 1, UBound(Arr, 2) - LBound(Arr, 2) + 1) = Arr
Else
    Cols = Split(ColumnNo, ",")
    For Each Col In Cols
        If Trim(Col) <> "" Then
            startRng.Cells(1, X).Resize(UBound(Arr, 1) - LBound(Arr, 1) + 1) = Extract_Column(Arr, CLng(Trim(Col)))
        End If
        X = X + 1
    Next
End If
Exit Sub
 
SingleDimension:
Dim tempArr As Variant: Dim i As Long
ReDim tempArr(LBound(Arr, 1) To UBound(Arr, 1), 1 To 1)
For i = LBound(Arr, 1) To UBound(Arr, 1)
    tempArr(i, 1) = Arr(i)
Next
startRng.Cells(1, 1).Resize(UBound(Arr, 1) - LBound(Arr, 1) + 1, 1) = tempArr
 
End Sub
 
'########################
' 배열에서 특정 열 데이터만 추출합니다.
' Array = Extract_Column(Array, 1)
'########################
 
Function Extract_Column(DB As Variant, Col As Long) As Variant
 
Dim i As Long
Dim vArr As Variant
 
ReDim vArr(LBound(DB) To UBound(DB), 1 To 1)
For i = LBound(DB) To UBound(DB)
        vArr(i, 1) = DB(i, Col)
Next
 
Extract_Column = vArr
 
End Function

Sub ExportText(InnerStrings As String, Optional fileName As String = "텍스트추출", Optional Path As String)
 
'###############################################################
'오빠두엑셀 VBA 사용자지정함수 (https://www.oppadu.com)
'▶ Export_Text 함수
'▶ 문자열을 텍스트파일로 추출합니다.
'▶ 인수 설명
'_____________InnerStrings      : 텍스트파일로 추출할 문자열입니다.
'_____________fileName           : 텍스트 파일 이름입니다. 기본값은 "텍스트추출" 입니다. (선택인수)
'_____________path                   : 텍스트 파일을 생성할 경로입니다. 기본값은 바탕화면입니다. (선택인수)
'▶ 사용 예제
'ExportText "추출할 텍스트"
'###############################################################
 
Dim TextFile As Integer
Dim FilePath As String
 
If Path = "" Then Path = Environ("USERPROFILE") & "\Desktop\"
FilePath = Path & fileName & ".txt"
 
TextFile = FreeFile
 
Open FilePath For Output As TextFile
Print #TextFile, InnerStrings
Close TextFile
 
End Sub


Function GetGoogleKeyword(keyword, lang)

Dim s As String
Dim v As Variant
Dim i As Long

s = GetHttp("https://www.google.com/complete/search?q=" & keyword & "&client=gws-wiz&hl=" & lang & "&authuser=0", includeMeta:=True).body.innerhtml

s = Replace(s, "\u003cb\u003e", "")
s = Replace(s, "\u003c\/b\u003e", "")

s = Split(s, "[[[")(1)
v = Split(s, "[""")

For i = LBound(v) To UBound(v)
   v(i) = Replace(Left(v(i), InStr(1, v(i), """,")), """", "")
Next

GetGoogleKeyword = v
'GetGoogleKeyword = Application.WorksheetFunction.Transpose(v)

End Function

Function GetHttp(URL As String, Optional formText As String, _
                                Optional isWinHttp As Boolean = False, _
                                Optional RequestHeader As Variant, _
                                Optional includeMeta As Boolean = False, _
                                Optional RequestType As String = "GET") As Object
 
'###############################################################
'오빠두엑셀 VBA 사용자지정함수 (https://www.oppadu.com)
'▶ GetHttp 함수
'▶ 웹에서 데이터를 받아옵니다.
'▶ 인수 설명
'_____________URL                         : 데이터를 스크랩할 웹 페이지 주소입니다.
'_____________formText                 : Encoding 된 FormText 형식으로 보내야 할 경우, Send String에 쿼리문을 추가합니다.
'_____________isWinHttp               : WinHTTP 로 요청할지 여부입니다. Redirect가 필요할 경우 True로 입력하여 WinHttp 요청을 전송합니다.
'_____________RequestHeader       : RequestHeader를 배열로 입력합니다. 반드시 짝수(한 쌍씩 이루어진) 개수로 입력되어야 합니다.
'_____________includeMeta           : TRUE 일 경우 HTML 문서위로 ResponseText를 강제 입력합니다. Meta값이 포함되어 HTML이 작성되며 innerText를 사용할 수 없습니다. 기본값은 False 입니다.
'_____________RequestType           : 요청방식입니다. 기본값은 "GET"입니다.
'▶ 사용 예제
'Dim HtmlResult As Object
'Set htmlResult = GetHttp("https://www.naver.com")
'msgbox htmlResult.body.innerHTML
'###############################################################
 
Dim oHTMLDoc As Object: Dim objHTTP As Object
Dim HTMLDoc As Object
Dim i As Long: Dim blnAgent As Boolean: blnAgent = False
Dim sUserAgent As String: sUserAgent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
 
Application.DisplayAlerts = False
 
If Left(URL, 4) <> "http" Then URL = "http://" & URL
 
Set oHTMLDoc = CreateObject("HtmlFile")
Set HTMLDoc = CreateObject("HtmlFile")
 
If isWinHttp = False Then
    Set objHTTP = CreateObject("MSXML2.ServerXMLHTTP")
Else
    Set objHTTP = CreateObject("WinHttp.WinHttpRequest.5.1")
End If
 
objHTTP.setTimeouts 3000, 3000, 3000, 3000
objHTTP.Open RequestType, URL, False
If Not IsMissing(RequestHeader) Then
    Dim vRequestHeader As Variant
    For Each vRequestHeader In RequestHeader
        Dim uHeader As Long: Dim Lheader As Long: Dim steps As Long
        uHeader = UBound(vRequestHeader): Lheader = LBound(vRequestHeader)
        If (uHeader - Lheader) Mod 2 = 0 Then GetHttp = CVErr(xlValue): Exit Function
        For i = Lheader To uHeader Step 2
            If vRequestHeader(i) = "User-Agent" Then blnAgent = True
            objHTTP.setRequestHeader vRequestHeader(i), vRequestHeader(i + 1)
        Next
    Next
End If
If blnAgent = False Then objHTTP.setRequestHeader "User-Agent", sUserAgent
 
objHTTP.send formText
 
If includeMeta = False Then
    With oHTMLDoc
        .Open
        .Write objHTTP.responseText
        .Close
    End With
Else
    oHTMLDoc.body.innerhtml = objHTTP.responseText
End If
 
Set GetHttp = oHTMLDoc
Set oHTMLDoc = Nothing
Set objHTTP = Nothing
 
Application.DisplayAlerts = True
 
End Function

