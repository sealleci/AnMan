from typing import Dict

chara_dict: Dict[str, int] = {}

with open("./input/chara.txt", "r", encoding="utf-8") as file:
    while True:
        name_item = file.readline().strip()
        if name_item == '':
            break
        for i in range(len(name_item)):
            if not name_item[i] in chara_dict:
                chara_dict[name_item[i]] = 1
            else:
                chara_dict[name_item[i]] += 1
            i += 1

sorted_list = list(map(lambda x: (x, chara_dict[x]), chara_dict))
sorted_list.sort(key=lambda x: x[1], reverse=True)

with open("./output/chara.txt", "w", encoding="utf-8") as file:
    for item in sorted_list:
        file.write(f"{item[0]}: {item[1]}\n")

with open("./output/chara_raw.txt", "w", encoding="utf-8") as file:
    for item in sorted_list:
        file.write(f"{item[0]}\n")
