from bs4 import BeautifulSoup
with open("C:/Users/Computer Market/Desktop/Depi/Depi_Amit_AI_BNS3/sources/session/code/wuzzuf_webscrabbing_task/25 data scientist jobs.html",encoding='UTF-8') as file:
    content=file.read()
    soupy=BeautifulSoup(content,'lxml')
    info=soupy.find_all('div',class_='css-d7j1kk')
    time=soupy.find_all('div',class_='css-do6t5g')
    for company_info,announce_time in zip(info,time) :
        company_name=company_info.a.text
        company_location=company_info.span.text
        print(f"The company name is:{company_name}and it's location is: {company_location} and the job is posted {announce_time.text}")