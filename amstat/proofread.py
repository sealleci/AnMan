import requests
from bs4 import BeautifulSoup, Tag
from concurrent.futures import ThreadPoolExecutor
from typing import cast

chara_list: list[str] = []  # 确保这里有200个汉字
result_dict: dict[str, str] = {}

with open("./output/chara_raw.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

    for line in lines:
        cur_line = line.strip()

        if cur_line != '':
            chara_list.append(cur_line)


def write_result(chara: str, status: str, file_name: str = "proofread.txt"):
    with open(f"./output/{file_name}", "a", encoding="utf-8") as file:
        if status != "[correct]":
            file.write(f"{chara}: {status}\n")


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

                is_has_zhu = False
                note_elm_list = body_elm.find_all(
                    "div", {"class": "col-md-12 notes"})

                for note_elm in note_elm_list:
                    note_elm = cast(Tag, note_elm)
                    h3_elm = note_elm.find("h3")

                    if h3_elm is None:
                        continue

                    h3_elm = cast(Tag, h3_elm)
                    note_title = h3_elm.get_text().strip()

                    if note_title.find("說文解字注") >= 0:
                        is_has_zhu = True
                        break

                if not is_has_zhu:
                    chara_status = "[unorthodox]"
                elif real_chara == chara:
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

        write_result(chara, chara_status)
        return (chara, chara_status)
    else:
        print(f"request failed: {chara}")
        return (chara, "[fail]")


# chara_list = ["蝰", "賣", "欠", "透"]

results = []
start_index = 1582

# for chara in chara_list[start_index:]:
#     res = query_chara(chara)
#     if res[1] != "[correct]":
#         with open("./output/proofread.txt", "a", encoding="utf-8") as file:
#             file.write(f"{res[0]}: {res[1]}\n")

with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(query_chara, chara_list))
