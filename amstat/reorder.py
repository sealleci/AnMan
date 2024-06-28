output_order = ""

with open("./input/order.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    prev_index = "-1"
    cur_sub_order = 0

    for index, line in enumerate(lines):
        line = line.strip()

        if line != "":
            if line != prev_index:
                cur_sub_order = 0
                prev_index = line
                is_has_sub = False

                if index != len(lines) - 1:
                    next_line = lines[index+1].strip()
                    if next_line == line:
                        is_has_sub = True

                if is_has_sub:
                    output_order += f"\'{line}-{chr(ord('a')+cur_sub_order)}\n"
                    cur_sub_order += 1
                else:
                    output_order += f"\'{line}\n"
            else:
                output_order += f"\'{line}-{chr(ord('a')+cur_sub_order)}\n"
                cur_sub_order += 1


with open("./output/order.txt", "w", encoding="utf-8") as f:
    f.write(output_order)
