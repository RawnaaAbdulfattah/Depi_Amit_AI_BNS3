from bs4 import BeautifulSoup
with open("C:/Users/Computer Market/Desktop/Depi/Depi_Amit_AI_BNS3/sources/session/code/wuzzuf_webscrabbing_task/25 data scientist jobs.html",encoding='UTF-8') as file:
    content=file.read()
    soupy=BeautifulSoup(content,'lxml')
    info=soupy.find_all('div',class_='css-d7j1kk')
    for company_info in info:
        company_name=company_info.a.text
        print(company_name)