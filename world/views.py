from django.shortcuts import render
from django.http import JsonResponse

import requests
from selenium import webdriver
# import re
from bs4 import BeautifulSoup
# Create your views here.
from world.models import Composition, Tag, TensileStrength, YieldStrength, ThermodynamicProperty, Stainless
from .train import make_compound_dict,train_ts

root='http://www.matweb.com'

def crawl_lists(num_str):
    Stainless.objects.filter(name__icontains=num_str).delete()
    url=root+'/search/QuickText.aspx?SearchText='
    data=requests.get(url+num_str.replace(' ',''))
    html=BeautifulSoup(data.text,'lxml')
    # print(html)
    # try:
    table=html.find("table",{"id":"tblResults"}).find_all('tr')
    # except:
    #     status['blocked']=True
    #     return status
    lists=[]
    for tr in table:    
        tds=tr.find_all('td')
        if len(tds)>=3:
            flag=False
            a=tds[2].a
            name=''
            tags=[]
            num_str=num_str.replace(' ','').lower()
            compare_text = a.text.strip().replace(' ','').lower()
            if num_str+"stainlesssteel" == compare_text:
                flag=True
                name=a.text.strip()

            elif num_str+"stainlesssteel" in compare_text:
                flag=True
                name,tags = SemiOrColon(a.text)

            elif num_str in compare_text and "stainlesssteel" in compare_text:
                flag=True
                name,tags = SemiOrColon(a.text)

            if flag:
                lists.append({'url':root+a["href"],'name':name, 'tags': tags, 'num': num_str})
    # print(lists)
    print("Got lists of "+num_str)
    return lists

def crawl_detail(datas):
    status={'ok':0,'err':0,'blocked':False}
    PROXY = "socks5://127.0.0.1:9050"
    options=webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument('disable-gpu')
    options.add_argument('--proxy-server=%s' % PROXY)
    browser=webdriver.Chrome('chromedriver',chrome_options=options)

    for i,data in enumerate(datas):
        browser=webdriver.Chrome('chromedriver',chrome_options=options)
        browser.get(data['url'])
        browser.implicitly_wait(3)
        html=browser.page_source
        # print(html)
        soup=BeautifulSoup(html,'lxml')
        try:
            table=soup.find_all("table",{"class":"tabledataformat"})
            trs=table[2].find_all("tr",{"class":"datarowSeparator"})
        except:
            status['blocked']=True
            return status

        level=-1 # 0 : TS, 1 : YS, 2 : Thermal, 3 : composition
        stainless=Stainless.objects.create(name=data['name'], num=data['num'])
        for tag in data['tags']:
            stainless.tag_set.create(name=tag)

        for tr in trs:
            try:
                if level==-1 and ("Tensile Strength, Ultimate" == tr.td.text.strip() or "Tensile Strength" == tr.td.text.strip()):
                    level=0
                    row=tr.find_all("td")
                    strength,crit=getValue(row)
                    cond=''
                    # print('@@',strength,crit)
                    
                    idx=crit.find('Temperature')
                    if crit!='' and idx>-1:
                        crit=float(crit[idx+12:].split(' ')[0])    
                    else:
                        crit=20
                        cond=crit

                    TensileStrength.objects.create(
                        stainless=stainless,
                        strength=strength,
                        crit=crit,
                        cond=cond
                    )
                    # stainless.save()
                    continue
            except Exception as e:
                print("lev -1->0 ts",e)
                break
            try:
                if level==0 and tr.td.text.strip()=='':
                    row=tr.find_all("td")
                    strength,crit=getValue(row)
                    cond=''
                    temperature=20
                    # print('@@',strength,crit)

                    idx=crit.find('Temperature')
                    if crit!='' and idx>-1: # @Temperature
                        temperature=float(crit[idx+12:].split(' ')[0])
                        if idx>3: #other condition given
                            cond=crit.split(",")[0]
                    
                    TensileStrength.objects.create(
                        stainless=stainless,
                        strength=strength,
                        crit=temperature,
                        cond=cond
                    )
                    continue
                elif level==0:
                    level=1
            except Exception as e:
                print("lev 0 ts",e)
                break
            try:
                if level==1 and "Tensile Strength, Yield" == tr.td.text.strip():
                    level=2
                    row=tr.find_all("td")
                    strength,crit=getValue(row)
                    cond=''
                    temperature=20
                    # print('@@',strength,crit)

                    idx=crit.find('Temperature')
                    if crit!='' and idx>-1: # @Temperature
                        temperature=float(crit[idx+12:].split(' ')[0])
                        if idx>3: #other condition given
                            cond=crit.split(",")[0]
                    
                    YieldStrength.objects.create(
                        stainless=stainless,
                        strength=strength,
                        crit=temperature,
                        cond=cond
                    )
                    continue
                
            except Exception as e:
                print("lev 1->2 ys",e)
                break
            try:
                if level==2 and tr.td.text.strip()=='':
                    row=tr.find_all("td")
                    strength,crit=getValue(row)
                    cond=''
                    temperature=20
                    # print('@@',strength,crit)

                    idx=crit.find('Temperature')
                    if crit!='' and idx>-1: # @Temperature
                        temperature=float(crit[idx+12:].split(' ')[0])
                        if idx>3: #other condition given
                            cond=crit.split(",")[0]
                    
                    YieldStrength.objects.create(
                        stainless=stainless,
                        strength=strength,
                        crit=temperature,
                        cond=cond
                    )
                    continue
                elif level==2:
                    level=3
            except Exception as e:
                print('@@ 2 ys',strength,crit)
                print("lev 2 ys",e)
                break
            try:
                if level==3 and "Thermal Conductivity" == tr.td.text.strip():
                    level=4
                    row=tr.find_all("td")
                    k,crit=getValue(row)
                    if crit=='':
                        ThermodynamicProperty.objects.create(stainless=stainless,k=k)
                    else:
                        crit=float(crit.split(' ')[1])
                        ThermodynamicProperty.objects.create(stainless=stainless,k=k,crit=crit)
                    continue
            except Exception as e:
                print("lev 3->4 k",e)
                break
            try:
                if level==4 and tr.td.text.strip()=='':
                    row=tr.find_all("td")
                    k,crit=getValue(row)
                    if crit=='':
                        ThermodynamicProperty.objects.create(stainless=stainless,k=k)
                    else:
                        crit=float(crit.split(' ')[1])
                        ThermodynamicProperty.objects.create(stainless=stainless,k=k,crit=crit)
                    continue
                elif level==4:
                    level=5
            except Exception as e:
                print("lev 4 k",e)
                break
            try:
                if level==5 and ("Carbon" in tr.td.text or "Boron" in tr.td.text):
                    level=6
                    row=tr.find_all("td")
                    compound=row[0].text.split(',')[1].strip()

                    ratio_array=[float(e.strip())for e in row[1].text.split('=')[-1].split('%')[0].split('-')]
                    ratio=sum(ratio_array)/len(ratio_array)
                    Composition.objects.create(
                        stainless=stainless,
                        compound=compound,
                        ratio=ratio 
                    )
                    continue
            except Exception as e:
                print("lev 5->6 composition",e)
                break
            try:
                if level==6:
                    row=tr.find_all("td")
                    compound=row[0].text.split(',')[1].strip()

                    ratio_array=[float(e.strip())for e in row[1].text.split('=')[-1].split('%')[0].split('-')]
                    ratio=sum(ratio_array)/len(ratio_array)
                    Composition.objects.create(
                        stainless=stainless,
                        compound=compound,
                        ratio=ratio
                    )
                    continue
            except Exception as e:
                stainless.delete()
                print("lev 6 composition",e)
                break
        
        print(str(i+1)+" / "+str(len(datas)),end=' ')
        if level<6:
            status['err']=status['err']+1
            print(level,'less than 6 = not sufficient of data')
            try: stainless.delete()
            except: print('already deleted.')
        else:
            status['ok']=status['ok']+1
            print(stainless.name,stainless.tag_set.all())
        # stainless.save()
        # print(stainless, stainless.tag_set.all())
        browser.quit()
    return status
    # table=detail_html.find_all("table",{"class":"tabledataformat"})
    # print(len(table.find_all("tr")))   
    #detail page 데이터 존재 유무 확인, TS, YS, k

    #이미 존재하면 pass
    # print(name,tags)
    # print(root+a["href"])
    # return render(req,'world/index.html')

def main(request,name):
    datas=crawl_lists(name)
    status=crawl_detail(datas)
    return JsonResponse(status)
    # return render(request,'world/index.html')

def train(request):
    make_compound_dict()
    return JsonResponse({'url':'train'})

# def test(request):
#     test_db()
#     return JsonResponse({'url':'test'})

def SemiOrColon(text):
    sem=text.split(';')
    col=text.split(',')
    if len(sem) < len(col): 
        return col[0],[c.strip() for c in col[1:]]
    return sem[0], [s.strip() for s in sem[1:]]

def getValue(row):
    try:
        if row[1].a!=None:
            strength=float(row[1].a.text.split('=')[-1].strip())
            # print('@@getValue',strength)
        else:
            arr=[float(num.strip()) for num in row[1].text.split('=')[-1].split('%')[0].strip().split('-')]
            # &gt; x.xx %
            # &lt; x.xx
            # x.xx %
            # x.xx - y.yy
            strength=sum(arr)/len(arr)
    except Exception as e:
        print("=========error strength=========")
        strength=-1
        print(row,e)    

    try:
        crit=row[1].span.text.strip()
    except Exception as e:
        print("=========error crit=========")
        crit=''
        print(row,e)
    return strength, crit
    # return strength,''

def tensor_ts(request):
    train_ts()
    return JsonResponse({'hi':'world'})