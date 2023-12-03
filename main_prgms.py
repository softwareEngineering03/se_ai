import requests
import sys
from bs4 import BeautifulSoup
import os
import re
import csv

def savewithtext(
    problem_num,
    problem_sub,
    problem_des,
    file_namelist
):
    problem_sublist = []
    
    with open("kakao_prgms.tsv", mode="a", newline='') as f:
        wr = csv.writer(f, delimiter='\t')
        for i in range(len(problem_num)):
            problem_info = [problem_num[i], problem_sub[i], problem_des[i].strip()]
            # make_problem_dir = f"{file_name}"
            # pytext = open(f"{make_problem_dir}/{file_name}.py", "r").read()
            # readme = open(f"{make_problem_dir}/README.md", "r").read()
            problem_sublist.append(problem_sub[i])
            wr.writerow(problem_info)
    
        

    # 태그 입력을 위한 키워드
    print(*problem_sublist)


def urlrequest(url):
    """url header 변형으로 크롤링"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response


main_url = "https://school.programmers.co.kr"
# url = f"{main_url}/workbook/view/1152"
url = "https://school.programmers.co.kr/learn/challenges?order=recent&page=1&partIds=37527"

# Step 가져오기
step_list = []
# 문제 번호
problem_num = []
# 문제 소제목
problem_sub = []
# 문제 설명
problem_des = []

# problem_input = []
# problem_output = []

whole_response = urlrequest(url)
# print(whole_response)
# 응답 코드가 200일시 *정상적으로 가져왔을시에
# if whole_response.status_code == 200:
#     html = whole_response.text
#     soup = BeautifulSoup(html, "html.parser")
#     main = soup.find("div", {"class": "table-responsive"})
#     body = main.find("tbody")
#     links = body.find_all("tr")
#     for link in links:
#         lnk = link.find("a").attrs["href"]
#         steps = main_url + lnk
#         step_list.append(steps)

#     # 필요한 링크를 모두 가져왔다.
#     need_step = int(input("필요한 단계를 입력하시오."))
#     steps = step_list[int(need_step) - 1]

#     # request를 해오고 이를 BS로 html을 파싱해온다.
#     step_response = urlrequest(steps)
    
# else:
#     print("파싱 에러", whole_response.status_code)
#     raise ConnectionError("크롤링 HTML 가져오지 못하였음")
with open('kakao.text', 'rt') as f:
    step_html = f.read()
    
if whole_response.status_code == 200:
    # step_html = whole_response.text
    step_soup = BeautifulSoup(step_html, "html.parser")
    step_main = step_soup.find("div", {"class": "inner-wrap"})
    step_body = step_main.find("tbody")
    pbs = step_body.find_all("tr")
    cnt = 1

    file_namelist = []

    for pb in pbs:
        # nums = pb.find("td", {"class": "list_problem_id"}).text
        # subs = pb.find("a").text
        nums = cnt
        subs = pb.find("a").text
        file_name = f"{str(cnt).zfill(2)}#{nums}_{subs}"
        # 문제별 폴더, 파일(.py, README) 생성하기
        file_namelist.append(file_name)
        
        
        problem_num.append(nums)
        problem_sub.append(subs)
        pblink = pb.find('a').attrs["href"]
        pbcontent = main_url + pblink
        pbcontent_response = requests.get(
            pbcontent, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        )

        if pbcontent_response.status_code == 200:
            pbcontent_html = pbcontent_response.text
            pbcontent_soup = BeautifulSoup(pbcontent_html, "html.parser")
            pbcontent_main = pbcontent_soup.find("div", {"class": "markdown solarized-dark"})
            hr_tag = pbcontent_main.find('hr')
            p_tag = pbcontent_main.find('p')
            li_tag = pbcontent_main.find('li')
            pb_str_list = list(pbcontent_main.stripped_strings)
            
            # pcs = ''.join(pb_str_list[:pbcontent_main.index(hr_tag)])
            pcs=''
            for e in pbcontent_main.find_all():
                if e is hr_tag:
                    break
                elif e is p_tag or e is li_tag:
                    pcs+=str(e.text.strip())
            # pcs = ''.join(str(e) for e in pbcontent_main.find_all() if e is not hr_tag)
            # pcs = ''.join(pb_str_list)
            # pb_input = pbcontent_main.find("div", {"id": "problem_input"}, {"class": "problem-text"}).text
            # pb_output = pbcontent_main.find("div", {"id": "problem_output"}, {"class": "problem-text"}).text
            problem_des.append(pcs)
            # problem_input.append(pb_input)
            # problem_output.append(pb_output)

        else:
            print(f"There is no content in {nums}")
        cnt += 1
    # else:
    #     print(f"errorcode: {step_response.status_code} at {steps}step")
else:
    print("파싱 에러", whole_response.status_code)
    raise ConnectionError("크롤링 HTML 가져오지 못하였음")

if len(problem_num) == len(problem_sub):
    print("work correctly!")
else:
    print("something is wrong..")


savewithtext(
    problem_num,
    problem_sub,
    problem_des,
    file_namelist
)
# problem_input
# problem_output   
