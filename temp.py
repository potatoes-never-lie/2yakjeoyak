#DUR 정보 조회(=정보조회 모듈 JSON 파일과 합치기)
def get_DUR():
    urls=['getUsjntTabooInfoList','getSpcifyAgrdeTabooInfoList','getPwnmTabooInfoList','getCpctyAtentInfoList', 'getMdctnPdAtentInfoList', 'getOdsnAtentInfoList', 'getEfcyDplctInfoList', 'getSeobangjeongPartitnAtentInfoList','getDurPrdlstInfoList']
    names=['레보트라정']
    i=0
    for url in urls:
        for name in names:
            queryParams = '?' + urlencode({ quote_plus('ServiceKey') :'2NB3WWEHcsTp8oyE6BiUgMcdn9RQ1B+O/ekuQkiE1qrUGTeSl4KFqp+6akjWbGbm7rmhZe1Mt4zkLVRoT4jSyQ==', quote_plus('itemName') :name})
            response=requests.get(DUR_url+url+queryParams)
            print(response.text)

def get_DUR1():         #각 DUR 별 case로 JSON element 추가하는 코드 만들기 
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') :'2NB3WWEHcsTp8oyE6BiUgMcdn9RQ1B+O/ekuQkiE1qrUGTeSl4KFqp+6akjWbGbm7rmhZe1Mt4zkLVRoT4jSyQ==', quote_plus('itemName'): '아테노린정'})
    response=requests.get('http://apis.data.go.kr/1470000/DURPrdlstInfoService/getPwnmTabooInfoList'+queryParams)
    root_element=ElementTree.fromstring(response.text)
    datas=[]
    iter_element=root_element.iter(tag="item")
    for element in iter_element:
        data={}
        data['ITEM_NAME']=element.find('ITEM_NAME').text
        data['INGR_CODE']=element.find('INGR_CODE').text
        data['PROHBT_CONTENT']=element.find('PROHBT_CONTENT').text
        datas.append(data)
    print(json.dumps(datas, indent=4, ensure_ascii=False))


def get_pillotherInfo(name, company=None):
    data={}
    if name=='바로소펜정':
        name='바로소펜'
    if name=='네렉손서방정':
        name='에페리손염산염'
    queryParams = '?' + urlencode({ quote_plus('ServiceKey') :serviceKey, quote_plus('itemName'): name, quote_plus("entpName"): company})
    response=requests.get('http://apis.data.go.kr/1470000/DURPrdlstInfoService/getDurPrdlstInfoList'+queryParams)
    root_element=ElementTree.fromstring(response.text)
    #datas=[]
    iter_element=root_element.iter(tag="item")
    if any(iter_element)==True:
        for element in iter_element:
            data['전문일반구분']=element.find('ETC_OTC_CODE').text
            data['제품종류']=element.find('CLASS_NO').text
            data['성상']=element.find('CHART').text
            data['원료성분']=element.find('MATERIAL_NAME').text
            data['유효기간']=element.find('VALID_TERM').text
            #datas.append(data)
    return data
    #return json.dumps(data, indent=4, ensure_ascii=False)