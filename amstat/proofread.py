import requests
from bs4 import BeautifulSoup, Tag
from concurrent.futures import ThreadPoolExecutor
from typing import cast

chara_list = []  # 确保这里有200个汉字
result_dict: dict[str, str] = {}

with open("./output/chara_raw.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

    for line in lines:
        cur_line = line.strip()

        if cur_line != '':
            chara_list.append(cur_line)


def query_chara(chara: str) -> tuple[str, str]:
    print(f"handling: {chara}")
    url = f"https://www.shuowen.org/?kaishu={chara}"

    response = requests.get(url)

    if response.status_code == 200:
        chara_status = "[fail]"
        soup = BeautifulSoup(response.text, 'html.parser')

        while True:
            body_elm = soup.find("body", {"class": "shuowen-detail"})

            if body_elm is not None:
                body_elm = cast(Tag, body_elm)
                ol_elm = body_elm.find("ol", {"class": "breadcrumb"})

                if ol_elm is None:
                    break

                ol_elm = cast(Tag, ol_elm)
                li_elm = ol_elm.find("li", {"class": "active"})

                if li_elm is None:
                    break

                li_elm = cast(Tag, li_elm)
                real_chara = li_elm.get_text().strip()

                if real_chara == chara:
                    chara_status = "[correct]"
                else:
                    chara_status = real_chara
            else:
                body_elm_2 = soup.find("body", {"class": "home"})

                if body_elm_2 is None:
                    break

                body_elm_2 = cast(Tag, body_elm_2)
                table_elm = body_elm_2.find("table")

                if table_elm is None:
                    break

                table_elm = cast(Tag, table_elm)
                tbody_elm = table_elm.find("tbody")

                if tbody_elm is None:
                    break

                tbody_elm = cast(Tag, tbody_elm)
                tr_list = tbody_elm.find_all("tr")

                if len(tr_list) < 1:
                    break
                elif len(tr_list) == 1:
                    tr_elm = tr_list[0]

                    if tr_elm is None:
                        break

                    tr_elm = cast(Tag, tr_elm)
                    td_elm = tr_elm.find("td", {"colspan": "5"})

                    if td_elm is not None:
                        td_elm = cast(Tag, td_elm)
                        inner_text = td_elm.get_text().strip()

                        if inner_text == "沒有記錄":
                            chara_status = "[none]"
                            break
                else:
                    multi_chara = ''

                    for tr_elm in tr_list:
                        tr_elm = cast(Tag, tr_elm)
                        td_list = tr_elm.find_all("td")

                        if len(td_list) > 0:
                            td_elm = cast(Tag, td_list[0])
                            a_elm = td_elm.find("a")

                            if a_elm is not None:
                                a_elm = cast(Tag, a_elm)
                                real_chara = a_elm.get_text().strip()

                                if multi_chara != '':
                                    multi_chara += ' '

                                multi_chara += real_chara

                    chara_status = multi_chara

            break

        return (chara, chara_status)
    else:
        print(f"request failed: {chara}")
        return (chara, "[fail]")


# chara_list = ["蝰", "賣", "欠"]

results = []
start_index = 1582

# with ThreadPoolExecutor(max_workers=50) as executor:
#     results = list(executor.map(query_chara, chara_list))

for chara in chara_list[start_index:]:
    res = query_chara(chara)

    if res[1] != "[correct]":
        with open("./output/proofread.txt", "a", encoding="utf-8") as file:
            file.write(f"{res[0]}: {res[1]}\n")

# for key, value in results:
#     if value != "[correct]":
#         result_dict[key] = value

# with open("./output/proofread.txt", "w", encoding="utf-8") as file:
#     for key, value in result_dict.items():
#         file.write(f"{key}: {value}\n")
