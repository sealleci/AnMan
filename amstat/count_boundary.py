if __name__ == '__main__':
    jie_dict = {}
    with open('./input/boundary.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            cur_line = line.strip()
            if cur_line != '':
                if cur_line in jie_dict:
                    jie_dict[cur_line] += 1
                else:
                    jie_dict[cur_line] = 1

    with open('./output/boundary.txt', 'w', encoding='utf-8') as f:
        jie_dict = dict(
            sorted(jie_dict.items(), key=lambda x: x[1], reverse=True))
        for k, v in jie_dict.items():
            f.write(f'{k}: {v}\n')
