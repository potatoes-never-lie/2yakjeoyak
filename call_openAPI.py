from urllib.parse import urlencode, quote_plus
from xml.etree import ElementTree
import requests
import json

serviceKey='2NB3WWEHcsTp8oyE6BiUgMcdn9RQ1B+O/ekuQkiE1qrUGTeSl4KFqp+6akjWbGbm7rmhZe1Mt4zkLVRoT4jSyQ=='

info_url =  'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
identify_url='http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList'
DUR_url='http://apis.data.go.kr/1470000/DURPrdlstInfoService/'

#전문의약품=0 일반의약품=1
isGeneral={'네렉손서방정': 0,'레보트라정': 0,'리보테인정': 1,'바로소펜정':1,'베포탄정':0,'벤즈날정':1, '비타포린정':1, '소론도정':0, '스틸녹스정':0, '쎄락틸정':1, '알레그라정':0, '위싹정':1, '티지피파모티딘정':1, '페니라민정':1, '후라시닐정':0}
names=('네렉손서방정','레보트라정','리보테인정','바로소펜','베포탄정','벤즈날정', '비타포린정', '소론도정', '스틸녹스정', '쎄락틸정', '알레그라정180', '위싹정', '티지피파모티딘정', '페니라민정', '후라시닐정')

#식별정보 조회
def identify_pill():
    for name in names:
        print(name+" 질의 중..")
        queryParams = '?' + urlencode({ quote_plus('ServiceKey') : '2NB3WWEHcsTp8oyE6BiUgMcdn9RQ1B+O/ekuQkiE1qrUGTeSl4KFqp+6akjWbGbm7rmhZe1Mt4zkLVRoT4jSyQ==', quote_plus('item_name') : name})
        response=requests.get(identify_url+queryParams)
        print(response.text)

#일반의약품 정보조회
def get_general_pillInfo(name):
    if name=='바로소펜정':
        name='바로소펜'
    data={}
    l={'entpName': '업체명','itemName':'제품명','itemSeq':'품목기준코드','efcyQesitm':'효능', 'efcyQesitm':'효능','useMethodQesitm': '사용법','atpnWarnQesitm': '주의사항 경고','atpnQesitm': '주의사항','intrcQesitm': '상호작용','seQesitm': '부작용','depositMethodQesitm':'보관법'}
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('itemName') : name, quote_plus('type') : 'json' })
    response=requests.get(info_url+queryParams)
    r=response.json()['body']['items'][0]
    for i in l:
        data[l[i]]=r[i]
    return data
    #return json.dumps(data, indent=4, ensure_ascii=False)

#전문의약품 정보조회
def get_pro_fillInfo(name):
    if name=='알레그라정':
        name='알레그라정180'
    path='/Users/chaeyeon/Documents/2yakjeoyak/venv/info/pro/'
    filename=path+name+'.json'
    with open(filename) as json_file:
        data=json.load(json_file)
    return data
    #return json.dumps(data, indent=4,ensure_ascii=False)

#기타 정보 조회
def get_pillotherInfo(name):
    data={}
    if name=='바로소펜정':
        name='바로소펜'
    if name=='알레그라정':
        name='알레그라정180'
    path='/Users/chaeyeon/Documents/2yakjeoyak/venv/info/other/'
    filename=path+name+'.json'
    with open(filename) as json_file:
        data=json.load(json_file)
    return data
    #return json.dumps(data, indent=4, ensure_ascii=False)

#병용금기 정보 조회
def get_tabooInfo(name):
    data={}
    data["병용금기여부"]="N"
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('itemName'): name})
    response=requests.get('http://apis.data.go.kr/1470000/DURPrdlstInfoService/getUsjntTabooInfoList'+queryParams)
    root_element=ElementTree.fromstring(response.text)
    iter_element=root_element.iter(tag="item")
    if any(iter_element)==True:
        for element in iter_element:
            data["병용금기여부"]="Y"
            l={}
            l['병용금기DUR성분']=element.find('MIXTURE_INGR_KOR_NAME').text
            l['병용금기품목명']=element.find('MIXTURE_ITEM_NAME').text
            l['금기내용']=element.find('PROHBT_CONTENT').text
            data["병용금기내용"]=l
    return data

#특정연령대금기 정보 조회
def get_ageTaboo(name):
    data={}
    data["특정연령대금기여부"]="N"
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('itemName'): name})
    response=requests.get('http://apis.data.go.kr/1470000/DURPrdlstInfoService/getSpcifyAgrdeTabooInfoList'+queryParams)
    root_element=ElementTree.fromstring(response.text)
    iter_element=root_element.iter(tag="item")
    if any(iter_element)==True:
        for element in iter_element:
            data["특정연령대금기여부"]="Y"
            l={}
            l['DUR성분']=element.find('INGR_NAME').text
            l['금기내용']=element.find('PROHBT_CONTENT').text
            data["특정연령대금기내용"]=l
    return data

#임부금기 정보조회
def get_pwTaboo(name):
    data={}
    data["임부금기여부"]="N"
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('itemName'): name})
    response=requests.get('http://apis.data.go.kr/1470000/DURPrdlstInfoService/getPwnmTabooInfoList'+queryParams)
    root_element=ElementTree.fromstring(response.text)
    iter_element=root_element.iter(tag="item")
    if any(iter_element)==True:
        for element in iter_element:
            data["임부금기여부"]="Y"
            l={}
            l['DUR성분']=element.find('INGR_NAME').text
            l['금기내용']=element.find('PROHBT_CONTENT').text
            data["임부금기내용"]=l
    return data

#용량주의 정보조회 
def get_capaTaboo(name):
    data={}
    data["용량주의여부"]="N"
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('itemName'): name})
    response=requests.get('http://apis.data.go.kr/1470000/DURPrdlstInfoService/getCpctyAtentInfoList'+queryParams)
    root_element=ElementTree.fromstring(response.text)
    iter_element=root_element.iter(tag="item")
    if any(iter_element)==True:
        data["용량주의여부"]="Y"
        l={}
        l['용량주의']="용량에 주의하여 복용합니다."
        data["용량주의내용"]=l
    return data

#투여기간주의 정보조회 
def get_dateTaboo(name):
    data={}
    data["투여기간주의여부"]="N"
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('itemName'): name})
    response=requests.get('http://apis.data.go.kr/1470000/DURPrdlstInfoService/getMdctnPdAtentInfoList'+queryParams)
    root_element=ElementTree.fromstring(response.text)
    iter_element=root_element.iter(tag="item")
    if any(iter_element)==True:
        data["투여기간주의여부"]="Y"
        l={}
        l['투여기간주의']="투여기간에 주의하여 복용합니다."
        data["투여기간주의내용"]=l
    return data

#노인주의 정보조회
def get_elderTaboo(name):
    data={}
    data["노인주의여부"]="N"
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('itemName'): name})
    response=requests.get('http://apis.data.go.kr/1470000/DURPrdlstInfoService/getOdsnAtentInfoList'+queryParams)
    root_element=ElementTree.fromstring(response.text)
    iter_element=root_element.iter(tag="item")
    if any(iter_element)==True:
        for element in iter_element:
            data["노인주의여부"]="Y"
            l={}
            l['DUR성분']=element.find('INGR_NAME').text
            l['금기내용']=element.find('PROHBT_CONTENT').text
            data["노인주의내용"]=l
    return data

#서방정 분할주의 정보조회
def get_sbjTaboo(name):
    data={}
    data["서방정분할주의여부"]="N"
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : serviceKey, quote_plus('itemName'): name})
    response=requests.get('http://apis.data.go.kr/1470000/DURPrdlstInfoService/getSeobangjeongPartitnAtentInfoList'+queryParams)
    root_element=ElementTree.fromstring(response.text)
    iter_element=root_element.iter(tag="item")
    if any(iter_element)==True:
        for element in iter_element:
            data["서방정분할주의여부"]="Y"
            l={}
            l['금기내용']=element.find('PROHBT_CONTENT').text
            data["서방정분할주의내용"]=l
    return data

def get_JSON(name):
    if name=='알레그라정180':
        name='알레그라정'
    if name=='바로소펜':
        name='바로소펜정'
    if isGeneral[name]==1:     #일반의약품이면
        res1=get_general_pillInfo(name)
    else:   #전문의약품이면
        res1=get_pro_fillInfo(name)
    res2=get_pillotherInfo(name)
    tabooInfo=get_tabooInfo(name)
    ageTaboo=get_ageTaboo(name)
    pwTaboo=get_pwTaboo(name)
    cpTaboo=get_capaTaboo(name)
    dateTaboo=get_dateTaboo(name)
    elderTaboo=get_elderTaboo(name)
    sbjTaboo=get_sbjTaboo(name)
    res={**res1, **res2, **tabooInfo, **ageTaboo, **pwTaboo, **cpTaboo, **dateTaboo, **elderTaboo, **sbjTaboo}
    return json.dumps(res, indent=4, ensure_ascii=False)

'''
for i in names:
    print(i)
    print(get_JSON(i))
'''
