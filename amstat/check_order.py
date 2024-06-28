missed = ""

with open("./input/check.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    prev_index = "00"

    for line in lines:
        line = line.strip().split("-")[0]

        if line == "":
            continue

        prev_int = int(prev_index)
        cur_int = int(line)

        if prev_int != cur_int and abs(cur_int - prev_int) != 1:
            for i in range(prev_int + 1, cur_int):
                missed += f"{i}\n"

        prev_index = line

with open("./output/check.txt", "w", encoding="utf-8") as f:
    f.write(missed)
