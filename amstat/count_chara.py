from typing import Dict, List, Tuple

from circlify import Circle as CirclifyCircle, circlify
from matplotlib.patches import Circle as MatplotCircle
import matplotlib.pyplot as plt

SPECIAL_CHARA_LIST: List[str] = ["臂", "厷"]
REDUPLICATED_COUNT = 30
CLOUD_COLORS = [
    "#61DDAA",
    "#F6BD16",
    "#E8684A",
    "#6DC8EC",
]


def calc_chara_frequency() -> List[Tuple[str, int]]:
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

    for special_chara in SPECIAL_CHARA_LIST:
        if special_chara in chara_dict and chara_dict[special_chara] > REDUPLICATED_COUNT:
            chara_dict[special_chara] -= REDUPLICATED_COUNT

    sorted_chara_list = sorted(
        list(map(lambda x: (x, chara_dict[x]), chara_dict)),
        key=lambda x: x[1],
        reverse=True,
    )

    with open("./output/chara_frequency.txt", "w", encoding="utf-8") as file:
        for item in sorted_chara_list:
            file.write(f"{item[0]}: {item[1]}\n")

    with open("./output/chara.txt", "w", encoding="utf-8") as file:
        for item in sorted_chara_list:
            file.write(f"{item[0]}\n")

    return sorted_chara_list


def generate_chara_cloud(filtered_list: List[Tuple[str, int]]):
    circles: List[CirclifyCircle] = sorted(
        circlify(
            [count for _, count in filtered_list],
            show_enclosure=False,
            target_enclosure=CirclifyCircle(x=0, y=0, r=1),
        ),
        key=lambda _circle: _circle.r,
        reverse=True,
    )

    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    figure, axes = plt.subplots(figsize=(8, 8))
    axes.set_aspect("equal")
    axes.axis("off")

    for i, (circle, (chara, count)) in enumerate(zip(circles, filtered_list)):
        _font_size = max(6, circle.r * 160)

        axes.add_patch(
            MatplotCircle(
                (circle.x, circle.y),
                circle.r,
                facecolor=CLOUD_COLORS[i % len(CLOUD_COLORS)],
                linewidth=1,
            )
        )
        axes.text(
            circle.x,
            circle.y + circle.r * 0.15,
            chara,
            ha="center",
            va="center",
            fontsize=_font_size,
            fontweight="bold",
        )
        axes.text(
            circle.x,
            circle.y - circle.r * 0.5,
            str(count),
            ha="center",
            va="center",
            fontsize=_font_size * 0.6,
        )
    axes.set_xlim(-1.05, 1.05)
    axes.set_ylim(-1.05, 1.05)

    figure.savefig(
        "./output/chara_cloud.png",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.05
    )
    plt.close(figure)


sorted_chara_list = calc_chara_frequency()
filtered_chara_list = list(filter(lambda x: x[1] > 7, sorted_chara_list))
generate_chara_cloud(filtered_chara_list)
