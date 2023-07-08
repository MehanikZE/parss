import lxml
# import record as record
import requests
import aiohttp
import psycopg2
import asyncio
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

user_agent = {'User-agent': 'Mozilla/5.0'}
#url ='https://api.hh.ru/vacancies?text=python%20middle&per_page=100'
## url ='https://api.hh.ru/?text=python%20middle%20developer&per_page=50'
DB_USER = "postgres"
DB_NAME = "hw1"
DB_PASSWORD = "Vrt342zf"
DB_HOST = "127.0.0.1"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

# def spisok_vac(record=None):
url = 'https://hh.ru/search/vacancy?text=middle+python+developer&area=1&items_on_page=20&page=5&st=vacancy_simple'

class Base(DeclarativeBase):
    pass

class Vacan(Base):
    __tablename__ = 'vacancies'

    index: Mapped[str] = mapped_column(primary_key=True)
    company_name: Mapped[str]
    position: Mapped[str]
    job_description: Mapped[str]
    key_skills: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.index!r}, name={self.company_name!r}, fullname={self.position!r}, fullname={self.key_skills!r})"


class Vacan_bs4(Base):
    __tablename__ = 'vacancies_bs4'

    index: Mapped[str] = mapped_column(primary_key=True)
    company_name: Mapped[str]
    position: Mapped[str]
    job_description: Mapped[str]
    key_skills: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.index!r}, name={self.company_name!r}, fullname={self.position!r}, fullname={self.key_skills!r})"


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
print("Таблица создана")


result1 = requests.get(url, headers=user_agent)
print(result1.status_code)
b = result1.content.decode()
# print(b)
soup = BeautifulSoup(b, 'lxml')
soup_en = soup.encode()
# print(soup)
list = []
for link in soup.find_all('a'):
    s = link.get('href')
    list.append(s)
    print(link.get('href'))
print(list)
list_h = []
for i in list:
    # i = i+1
    # list_h = []
    if i[:30] == 'https://voronezh.hh.ru/vacancy':
        list_h.append(i)
        print(f'fff',i)
# print(list_h)
# print (len(list_h))

for sdf, z in enumerate(list_h):
    url_s = z
    # print(url_s)
    resultat = requests.get(url_s, headers=user_agent)
    # print(resultat.status_code)
    k = resultat.content.decode()
    # print (k)
    sop = BeautifulSoup(k, 'lxml')
    nazvan = sop.find_all('h1', {'data-qa': 'vacancy-title'})
    value1 = nazvan[0].getText()

    description = sop.find_all('div', {'data-qa': 'vacancy-description'})


    value2 = description[0].getText()
    # company_name = sop.find_all('span', {'data-qa': 'bloko-header-2'})
    company_name = sop.find_all('span', {'data-qa': 'bloko-header-2'})
    value3 = company_name[0].getText()

    key_skils = sop.find_all('span', {'data-qa': 'bloko-tag__text'})
    try:
        value4 = key_skils[0].getText()
    except:
        print ('IndexError: list index out of range:')

    # gh = BeautifulSoup.text(company_name, 'lxml')
    # rg = gh.get_text()

    with Session(engine) as session:
        names_bs4 = Vacan_bs4(index = sdf + 1 ,company_name = value3, position = value1, job_description = value2, key_skills = value4 )
        session.add_all([names_bs4])
        session.commit()
    # print(nazvan)
    # print(description)
    # ds = company_name.get_text()
    # print(company_name)
    print(key_skils)
    # print(value1)
    # print(value2)
    # print(value3)
    print(value4)
# for i, nov in enumerate(soup_en):
#     m = soup.find('a', attrs={result1 = requests.get(url, headers=user_agent))
#     # z = nov.find('a', attrs={'data-qa': 'serp-item__title'})

    # print(m)
###################################################################################################

# result = requests.get(url, headers=user_agent)
#
# print(result.status_code)
# print(result.text)
# j = result.json()
# print('dddd',j)
# print(type(j))
# vacans = result.json().get('items')
# print('eeeee',vacans)
# ttt = []
# for i, vac in enumerate(vacans):
#     print(i+1) #vac['name'], vac['url'], vac['alternate_url'])
#     s = vac['url']
#     print(s)
#     res = requests.get(s, headers=user_agent)
#     vacs = res.json()
#     m = vacs['name']
#     g = vacs['employer']['name']
#     z = vacs['description']
#     key_skills = vacs['key_skills']
#     if key_skills:
#         list = []
#         for sk in key_skills:
#             # list = []
#             l = sk['name']
#             list.append(l)
#
#     with Session(engine) as session:
#         names = Vacan(index = i+1 ,company_name = g, position = m, job_description = z, key_skills = list )
#         session.add_all([names])
#         session.commit()
#             # print(l)
#     # print(f'Вакансия:',m)
#     print(f'Комания:',g)
#     # ins_prod_query = .insert().values(company_name='31', position='31',job_descriptio='31',key_skills='31')
#     # print(f'Требования', z)
#     # print(list)
##################################################################################################################







#     with Session(engine) as session:
#         # for record in filesList:
#         new_name = Vacanss(
#                      g=record['company_name'],
#                      position=record['position'],
#                      job_descriptio=record['job_descriptio'],
#                      fkey_skills=record['key_skills'])
# # def create_table():




# spisok_vac()

#     result = requests.get(url, headers=user_agent)
#
#     # return res
#     # print(res)
#
#     # a = spisok()
#     vac = result.json().get('items')
#     spisok_id=[]
#     for i, vacans in enumerate(vac):
#     # print('sss',a.text)
#     # print(vac)
#         id_vac = vacans['id']
#         spisok_id.append(id_vac)
#     # print(c)
#     print('xxx',spisok_id)
#     print(len(spisok_id))
#     return spisok_id
#     # v =c['id']
#     # print(v)
# spisok_vac()
#
# def analizy_vac():
#     for g, vacansy in enumerate(spisok_vac()):





#     asyncio.run(main(sp))
# async def get_vacansy(id,session):
#     url = f'/vacancies/{id}'
#
#     async with session.get(url=url) as response:
#         vacansy_json = await response.json()
#         return vacansy_json
#
#
# async def main(ids):
#
#     async with aiohttp.ClientSession('https://api.hh.ru') as session:
#         task = []
#         for id in ids:
#             task.append(asyncio.create_task(get_vacansy(id, session)))
#         results = await asyncio.gather(*task)
#     for l, result in enumerate (results):
#         k = result['name']
#         # if k is not True:
#         #     print('xx')
#         print(l+1, result['name'],  result['employer']['name'], result['description']) #, result['key_skills'])





        # async with session.get('https://www.voronezh.hh.ru') as response:
        #     print(f"Ответ", response.status)
        #     # print(f'респонс',response)
        #     html = await response.text()
        #     return html
            # print(html[:150])
# vacansies_ids =  ['82525826', '82402579']
# print()
# asyncio.run(spisok())

# spisok()


# result = requests.get(url, headers=user_agent)

# print(result.status_code)
# print(result.text)
# j = result.json()
# print(j)
# print(type(j))
# vacans = result.json().get('items')
# print(vacans)
# for i, vac in enumerate(vacans):
#     print(i+1) #vac['name'], vac['url'], vac['alternate_url'])
#     s = vac['url']
#     # print(s)
#     res = requests.get(s, headers=user_agent)
#     vacs = res.json()
#     m = vacs['name']
#     g = vacs['employer']['name']
#     z = vacs['description']
#     key_skills = vacs['key_skills']
#     if key_skills:
#         list = []
#         for sk in key_skills:
#             # list = []
#             l = sk['name']
#             list.append(l)
#
#             # print(l)
#     print(f'Вакансия:',m)
#     print(f'Комания:',g)
#     print(f'Требования', z)
#     print(list)
#
#
#


# user_agent = {'User-agent': 'Mozilla/5.0'}
# result = requests.get('https://voronezh.hh.ru/vacancy/82402579', headers=user_agent)
# print (result)
# a = result.status_code
# print(a)
# b = result.content.decode()
# # print(b)
# soup = BeautifulSoup(result.content.decode(), 'lxml')
# # print(soup.prettify())
#
# v=soup.find('h1')
# # print(v)
# print(v.text)
#
# g = soup.find('a', attrs={'data-qa': 'vacancy-company-name'})
# # print(g)
# print(g.text)
#
# z = soup.find('div', attrs={'data-qa': 'vacancy-description'})
# # print(z)
# print(z.text)