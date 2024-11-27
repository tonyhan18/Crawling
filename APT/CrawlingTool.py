# 출처: https://cocoabba.tistory.com/58 [새로운 시작~!:티스토리]
# 혹시나 서비스 제한이 뜰 경우 "Https 유니콘"을 활성화 시킬것
import requests
from bs4 import BeautifulSoup
import json, math

import tkinter as tk
import tkinter.ttk
import tkinter.messagebox as msgbox

import datetime
# pip install openpyxl
from openpyxl import Workbook

# 페이지 접근을 자주 막는 것에 대해 selenium을 이용해서 해결 시도
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# UIUX
import CrawlingToolUIUX as UIUX

'''
ENV Settings
'''

# request 방식으로 할 경우
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}

# selenium 방식 호출
#driver_path = "./APT/chromedriver"
#path = 'chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("--headless")  # 헤드리스 모드
chrome_options.add_argument("--disable-gpu")  # GPU 비활성화 (선택 사항)
chrome_options.add_argument("window-size=1920x1080")  # 창 크기 설정
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36") # 봇 감지 피하기
#service = Service(driver_path)

driver = webdriver.Chrome(options=chrome_options)

# 엑셀 저장을 위한 도구
wb = Workbook()

# 표현하고자 하는 칼럼
table_column_list = {"rletTpNm":"상가 구분", "tradTpNm":"거래 유형","prc":"가격","spc1":"계약면적(평)","spc2":"전용면적(m2)","hanPrc":"보증금","rentPrc":"월세", "rate":"수익률"}

# 서비스 제한이 걸렸을때의 해결책
class CustomException(Exception):
    pass

def btnsearchcmd():
    maximum_count = 1
    
    # TODO : 좀 더 나이스하게 이 부분을 바꾸는 방법 필요
    # DONE : 만약 사용자가 이상한 값을 넣었다면 어떻게 할 것인가의 해결책
    keyword = entry_search.get()
    if(keyword == ""):
        keyword = "구로구 구로동"
    
    # try :
            
    # finally:
    #          
    url = "https://m.land.naver.com/search/result/{}".format(keyword)
    
    try:    
        res = requests.get(url, headers=headers)
        res.raise_for_status()    
        soup = (str)(BeautifulSoup(res.text,"lxml"))
        
        if(res.status_code != 200):
            raise CustomException 
        
        value = soup.split("filter: {")[1].split("}")[0].replace(" ","").replace("'","")
        lat = value.split("lat:")[1].split(",")[0]
        lon = value.split("lon:")[1].split(",")[0]
        z = value.split("z:")[1].split(",")[0]
        cortarNo = value.split("cortarNo:")[1].split(",")[0]
        rletTpCds = value.split("rletTpCds:")[1].split(",")[0]
        tradTpCds = value.split("tradTpCds:")[1].split(",")[0]
        
    except CustomException as e :
        # TODO : 자주 서비스가 제한된다.
        driver.implicitly_wait(5)
        driver.get(url)
        print(driver.page_source)
        driver.quit()
        
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
        lat = '37.4937'
        lon = '126.8823'
        z = '14'
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
    # TODO : 동적 할당 기능 필요
    rletTpCds = "SG"

    # TODO : A1=매매/B1=전세/B2=월세/B3=단기임대/*=전체
    tradTpCds = "A1"
    
    ###### New ARTICLE DATA
    # 아파트는 COMPLEX로 묶어서 사용이 가능
    # 상가는 ARTICLE로 사용(묶일 이유가 없음)
    remaked_URL = "https://m.land.naver.com/cluster/clusterList?view=atcl&cortarNo={}&rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&addon=COMPLEX&bAddon=COMPLEX&isOnlyIsale=false"\
        .format(cortarNo, rletTpCds, tradTpCds, z, lat, lon)

    res_complx = requests.get(remaked_URL, headers=headers)
    #json_str = (str)(BeautifulSoup(res_complx.text,"lxml"))
    # TODO : 특정 article은 에러를 발생시킨다
    json_str = json.loads(json.dumps(res_complx.json()))
    soup = (str)(BeautifulSoup(res_complx.text,"lxml"))


    article_list = json_str['data']['ARTICLE']

    # 큰 원으로 구성되어 있는 전체 매물그룹(values)을 load 하여 한 그룹씩 세부 쿼리 진행
    '''
    https://m.land.naver.com/cluster/ajax/articleList?itemId=2120322202&mapKey=&lgeo=2120322202&showR0=&rletTpCd=SG&tradTpCd=A1&z=14&lat=37.4937&lon=126.8823&totCnt=25&cortarNo=1153010200&sort=rank&page=1
    '''

    j = 0
    for article in article_list:
        print(j)
        j += 1
        lgeo = article['lgeo']
        count = article['count']
        z2 = article['z']
        lat2 = article['lat']
        lon2 = article['lon']

        len_pages = count / 20 + 1

        for idx in range(1, math.ceil(len_pages)):
            remaked_detail = "https://m.land.naver.com/cluster/ajax/articleList?""itemId={}&mapKey=&lgeo={}&showR0=&" \
                "rletTpCd={}&tradTpCd={}&z={}&lat={}&lon={}&totCnt={}&cortarNo={}&page={}"\
                .format(lgeo, lgeo, rletTpCds, tradTpCds, z2, lat2, lon2, count, cortarNo, idx)
            
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
                atclNo = rs['atclNo']        # 물건번호
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
                tablelist = [str(rletTpNm), str(tradTpNm), str(format(prc, ','))+" 만원", str(spc1),
                str(spc2),str(hanPrc)+" 만원", str(format(rentPrc,',') +" 만원"),"7%"]
                
                tableview.insert("", 'end', values=tablelist)
    # ....
    # #엑셀시트에 데이터 append
    # ws.append([str(rletTpNm), str(tradTpNm), str(prc * 10000), str(spc1),
    #             str(spc2),
    #             str(hanPrc), str(rentPrc * 10000),
    #             str(flrInfo),str(tagList),
    #             str(rltrNm), detaild_information])
    # ....
    
    
    #검색 완료 후 엑셀 저장 버튼 활성화
    btn_exportexcel.config(state="active")


def focus_in(entry_search):
    if entry_search.cget("state") == "disabled":
        entry_search.config(state="normal")
        entry_search.delete(0, tk.END)
        
def focus_out(entry_search, search_keyword):
    if(entry_search.get().strip() == ""):
        entry_search.insert(0, "구로구 구로동")
        entry_search.config(state="disabled")
        
def btnexportexcel():
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y%m%d_%H%M%S')
    keyword = entry_search.get()
    sheet = wb.active

    column_title = list(table_column_list.values())
    sheet.append(column_title)
    
    for row_id in tableview.get_children():
        row = tableview.item(row_id)["values"]
        sheet.append(row)
        
    file_name = keyword+"_"+nowDatetime+".xlsx"
    wb.save("./"+file_name)
    
    msgbox.showinfo("파일 저장", "'"+file_name+"' 파일로 정상적으로 추출되었습니다.")

def btnexit():
    exit()



# This probably means that Tcl wasn't installed properly
# https://blog.naver.com/tjdus25/221652293934
root = tk.Tk()
root.title("부동산 상가 매물 검색 프로그램")

#검색 프레임 (entry, 검색버튼, 엑셀 버튼)
search_frame = tk.Frame(root)
search_frame.pack(expand=True, pady=10,fill="both")

#검색 입력 창
entry_search = tk.Entry(search_frame)
entry_search.pack(side="left",fill="both", expand=True)
entry_search.insert(0, "구로구 구로동")
entry_search.configure(state='disabled')

#entry에 클릭했을 때 on_forcus_in 함수 실행 
x_focus_in = entry_search.bind('<Button-1>', lambda x: focus_in(entry_search)) #<Button-1> 왼쪽버튼 클릭
x_focus_out = entry_search.bind('<FocusOut>', lambda x: focus_out(entry_search, '검색할 지역명 검색 (예: 구로구 구로동)')) #<FocusOut> 위젯선택 풀릴 시 (다른 곳 클릭 or tab)

#검색버튼
btn_search = tk.Button(search_frame, text="검색", padx=5, pady=5, command = btnsearchcmd)
btn_search.pack(side="left", padx=5, fill="both")

#엑셀 저장 버튼
btn_exportexcel = tk.Button(search_frame, text="엑셀 저장",  padx=5, pady=5, command = btnexportexcel, state=tk.DISABLED)
btn_exportexcel.pack(side="left", padx=5,fill="both")

#프로그램 종료 버튼
btn_exit = tk.Button(search_frame,  text="프로그램 종료", padx=5, pady=5, command = btnexit)
btn_exit.pack(side="left", padx=5,fill="both")


# 상가 구분 프레임
sg_condition_frame = tk.Frame(root)
sg_condition_frame.pack(side="top", pady=20,fill="both")

# 큰 프레인 안에 좌:"상가 구분", 우:"거래 유형" 으로 레이아웃 쪼개기
# LableFrame 을 활용하여, checkbutton 을 묶어서 제목:"상가 구분" 붙이기
frame_middle_left = tk.LabelFrame(sg_condition_frame, text="상가 구분")
frame_middle_left.pack(side="left", fill="both", expand=True)

sg_chk1 = tk.IntVar()
sg_chk1_box = tk.Checkbutton(frame_middle_left, text="상가", variable = sg_chk1)# 상가
sg_chk1_box.pack(side="left")
sg_chk1_box.select()

sg_chk2 = tk.IntVar()
sg_chk2_box = tk.Checkbutton(frame_middle_left, text="상가주택", variable = sg_chk2)# 상가주택
sg_chk2_box.pack(side="left")

sg_chk3 = tk.IntVar()
sg_chk3_box = tk.Checkbutton(frame_middle_left, text="사무실", variable = sg_chk3)# 사무실
sg_chk3_box.pack(side="left")

sg_chk4 = tk.IntVar()
sg_chk4_box = tk.Checkbutton(frame_middle_left, text="공장/창고", variable = sg_chk4)# 공장/창고
sg_chk4_box.pack(side="left")

sg_chk5 = tk.IntVar()
sg_chk5_box = tk.Checkbutton(frame_middle_left, text="건물", variable = sg_chk5)# 건물
sg_chk5_box.pack(side="left")

sg_chk6 = tk.IntVar()
sg_chk6_box = tk.Checkbutton(frame_middle_left, text="토지", variable = sg_chk6)# 토지
sg_chk6_box.pack(side="left")

sg_chk7 = tk.IntVar()
sg_chk7_box = tk.Checkbutton(frame_middle_left, text="지식산업센터", variable = sg_chk7)# 사무실
sg_chk7_box.pack(side="left")


# 거래 유형 프레임
frame_middle_right = tk.LabelFrame(sg_condition_frame, text="거래유형")
frame_middle_right.pack(side="right", fill="both", expand=True)

tr_type1 = tk.IntVar()
tr_type1_box = tk.Checkbutton(frame_middle_right, text="매매", variable = tr_type1)# 매매 
tr_type1_box.pack(side="left")
tr_type1_box.select()

tr_type2 = tk.IntVar()
tr_type2_box = tk.Checkbutton(frame_middle_right, text="전세", variable = tr_type2)# 전세
tr_type2_box.pack(side="left")

tr_type3 = tk.IntVar()
tr_type3_box = tk.Checkbutton(frame_middle_right, text="월세", variable = tr_type3)# 월세
tr_type3_box.pack(side="left")

tr_type4 = tk.IntVar()
tr_type4_box = tk.Checkbutton(frame_middle_right, text="단기임대", variable = tr_type4)# 단기임대
tr_type4_box.pack(side="left")


# 결과 출력 프레임
result_print_frame = tk.LabelFrame(root, text = "검색 결과")
result_print_frame.pack(side="top", fill="both")

list_frame  = tk.Frame(result_print_frame)
list_frame.pack(side="top", fill="both")

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill = "y")

# TODO : 칼럼항목을 조절할 수 있음
keys_view = list(table_column_list.keys())

tableview = tkinter.ttk.Treeview(list_frame, columns=keys_view,\
                    displaycolumns=keys_view, height=20, yscrollcommand=scrollbar.set)

# 이렇게 안 하면 #0 컬럼이 생겨버림;;
tableview.column("#0",width=0,stretch=tk.NO)
tableview.pack(fill="both")

# 각 컬럼 설정. 컬럼 이름, 컬럼 넓이, 정렬 등
for key, value in table_column_list.items():
    tableview.column(key, width=80,anchor="center")
    tableview.heading(key, text=value, anchor="center")

#스크롤바를 움직일 때 표도 같이 이동할 수 있도록 적용
scrollbar.config(command=tableview.yview)

root.mainloop()

    
# 이런식으로 명명하면 다른 파일에서 임포트되었을 때 실행되지 않도록한다.
# def main():
    
# if __name__ == "__main__":
#     main()