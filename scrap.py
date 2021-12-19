import requests
from bs4 import BeautifulSoup
import xlsxwriter

url = "https://collegedunia.com/btech/mysore-colleges"

headers = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

res = requests.get(url=url, headers=headers)

soup = BeautifulSoup(res.content, 'html5lib')


clg = soup.find_all('a', attrs = {'class':'college_name'})
clg_urls = []
for i in range(0,6):
    clg_urls.append("https://collegedunia.com"+clg[i]['href'])
    
    
clg_summaries = []

for college in clg_urls:
    res = requests.get(url=str(college), headers=headers)
    soup = BeautifulSoup(res.content, 'html5lib')
    summary_el = soup.find('div',attrs={'class':'cdcms_college_highlights'})
    summary = ""
    for i in summary_el.find_all('p'):
        summary = summary + i.text
    clg_summaries.append(summary)

# print(len(clg_summaries))
# jsx-2675951502 table table-striped text-center
# th_data = []
td_data = []
clg_names=[]
for college in clg_urls:
    res = requests.get(url=str(college), headers=headers)
    soup = BeautifulSoup(res.content, 'html5lib')
    table_el = soup.find('table',attrs={'class':["jsx-2675951502"]})
    # th_data.append(table_el.find_all('th',attrs={'class':"jsx-2675951502"}))
    # clg_name_el = soup.find('h3',attrs={'class':["jsx-2675951502","card-heading"]})
    clg_name_el = soup.find('h1',attrs={'id':["collegePageTitle"]})
    clg_names.append(clg_name_el.text)
    tds = table_el.find_all('td',attrs={'class':"jsx-2675951502"})
    tds_data = []
    for i in tds:
        tds_data.append(i.text)
    tds_final = []
    x=0
    for j in range(x,len(tds_data),3):
        x=j
        tds_final.append(tds_data[x:x+4])
    td_data.append(tds_final)



for i,j,k in zip(clg_names,td_data,clg_summaries):
    print(i)
    print(j)
    print(k)
    print("-----------------------")
    
    

# for college in clg_names:
#     worksheet = workbook.add_worksheet(college)



    
workbook = xlsxwriter.Workbook("test_final.xlsx")
for college,table_data,clg_sum in zip(clg_names,td_data,clg_summaries):
    worksheet = workbook.add_worksheet(college[:31])
    heads = ["Summary","COURSE","FEES","ELIGIBILITY"]
    row=0
    col=0
    for head in heads:
        worksheet.write(row,col,head)
        col+=1
    worksheet.write(1,0,clg_sum)
    row = 1
    for i in table_data:
        col=1
        for j in i:
            worksheet.write(row,col,j)
            col+=1
        row+=1
workbook.close()



        
        
        

    



    


