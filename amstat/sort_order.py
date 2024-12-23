from re import match, search

sorted_order = ""
sub_index_pattern = r"'?\d+-(\w)"
special_sub_index = ["00", "e", "-1"]

with open("./input/sort.txt", "r", encoding="utf-8") as f:
    """
    1.

    192
    193

    2.

    192-a
    192-b

    3.

    192-c
    193-a

    4.

    192-c
    193
    """

    cur_line_index: int = 1
    cur_line_sub_index: int = 0
    lines = f.readlines()

    for index, line in enumerate(lines):
        line = line.strip()
        is_cur_line_has_sub_index: bool = False
        is_next_line_has_sub_index: bool = False
        is_next_line_sub_index_continuous: bool = False

        if line in special_sub_index:
            sorted_order += f"{line}\n"
            continue

        cur_line_match = search(sub_index_pattern, line)

        if cur_line_match:
            is_cur_line_has_sub_index = True
            cur_line_sub_index = ord(cur_line_match.group(1)) - ord("a")

        if index < len(lines) - 1:
            next_line = lines[index+1].strip()
            next_line_match = search(sub_index_pattern, next_line)

            if next_line_match:
                is_next_line_has_sub_index = True
                next_line_sub_index = ord(next_line_match.group(1)) - ord("a")

                if is_cur_line_has_sub_index and cur_line_sub_index + 1 == next_line_sub_index:
                    is_next_line_sub_index_continuous = True

        sorted_order += f"{'0' if cur_line_index <= 9 else ''}{cur_line_index}{f'-{chr(ord('a') + cur_line_sub_index)}' if is_cur_line_has_sub_index else ''}\n"

        if not is_next_line_has_sub_index or not is_next_line_sub_index_continuous:
            cur_line_index += 1

with open("./output/sort.txt", "w", encoding="utf-8") as f:
    f.write(sorted_order)
