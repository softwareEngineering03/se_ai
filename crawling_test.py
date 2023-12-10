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
    
    with open("validation.csv", mode="a", newline='') as f:
        wr = csv.writer(f)
        for i in range(len(problem_num)):
            problem_info = [problem_num[i], problem_sub[i], " ".join(problem_des[i].split())]
            # make_problem_dir = f"{file_name}"
            # pytext = open(f"{make_problem_dir}/{file_name}.py", "r").read()
            # readme = open(f"{make_problem_dir}/README.md", "r").read()
            problem_sublist.append(problem_sub[i])
            wr.writerow(problem_info)
        

    # 태그 입력을 위한 키워드
    print(*problem_sublist)


def urlrequest(url):
    """url header 변형으로 크롤링"""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return response


def mkdir(root_path, step_name):
    make_step_dir = f"{root_path}/{step_name}"
    if step_name in os.listdir(root_path):
        print("동일 이름을 가진 폴더가 존재합니다.", step_name)
    else:
        os.mkdir(make_step_dir)
    return make_step_dir


def mkproblemdir(make_step_dir, file_name):
    file_name = re.sub(r"[\/*?<>|]", "MoD", file_name)
    make_problem_dir = f"{make_step_dir}/{file_name}"
    if file_name in os.listdir(make_step_dir):
        print("동일 이름을 가진 폴더가 존재합니다.", file_name)
    else:
        os.mkdir(str(make_problem_dir))
    open(f"{make_problem_dir}/{file_name}.py", "w")
    open(f"{make_problem_dir}/README.md", "w")


root_path = "./data"
main_url = "https://www.acmicpc.net"
url = f"{main_url}/problemset?sort=ac_desc&algo=25&algo_if=and&page=3"


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
if whole_response.status_code == 200:
    step_html = whole_response.text
    step_soup = BeautifulSoup(step_html, "html.parser")
    step_main = step_soup.find("div", {"class": "table-responsive"})
    step_body = step_main.find("tbody")
    pbs = step_body.find_all("tr")
    cnt = 0

    file_namelist = []

    for pb in pbs:
        # nums = pb.find("td", {"class": "list_problem_id"}).text
        # subs = pb.find("a").text
        if not pb.find("a"):
            break
        # nums = pb.find("td").text
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
            pbcontent, headers={"User-Agent": "Mozilla/5.0"}
        )

        if pbcontent_response.status_code == 200:
            pbcontent_html = pbcontent_response.text
            pbcontent_soup = BeautifulSoup(pbcontent_html, "html.parser")
            pbcontent_main = pbcontent_soup.find("div", {"id": "problem-body"})
            pcs = pbcontent_main.find("div", {"class": "problem-text"}).text
            pb_input = pbcontent_main.find("div", {"id": "problem_input"}, {"class": "problem-text"}).text
            pb_output = pbcontent_main.find("div", {"id": "problem_output"}, {"class": "problem-text"}).text
            problem_des.append(pcs)
            # problem_input.append(pb_input)
            # problem_output.append(pb_output)

        else:
            print(f"There is no content in {nums}")
    # else:
    #     print(f"errorcode: {step_response.status_code} at {steps}step")
        cnt += 1
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
