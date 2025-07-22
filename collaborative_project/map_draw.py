import pandas as pd
import os
import matplotlib.pyplot as plt

# 1단계에서 생성된 결과 파일 경로를 지정합니다.
csv_path = os.path.join("result", "caffee_map.csv")
print(os.path.exists(csv_path))  # True가 나오면 존재함
# csv 파일 읽기
df = pd.read_csv(csv_path)

# 여기에 추가: NaN 값을 "Empty"로 채워줍니다.
df["struct_name"] = df["struct_name"].fillna("Empty").str.strip()

# print(df.head())

# df의 x, y 좌표 범위 확인
x_min, x_max = df["x"].min(), df["x"].max()
y_min, y_max = df["y"].min(), df["y"].max()


# plt 객체를 불러와서 그래프 임의로 크기 생성
plt.figure(figsize=(10, 6))
# 격자선 표시
plt.grid(True)
# matplotlib의 기본 y축 방향이 화면 위가 증가 방향이므로
# 시각적으로 아래쪽이 0이 되도록 반전
plt.gca().invert_yaxis()

# 축 눈금을 정수로 고정
plt.xticks(range(x_min, x_max + 1))
plt.yticks(range(y_min, y_max + 1))

# x축, y축 간격 1:1로 설정
plt.gca().set_aspect('equal')

# 중복 범례 방지를 위한 체크
labeled = {
    "Apartment": False,
    "Building": False,
    "BandalgomCoffee": False,
    "MyHome": False,
    "ConstructionSite": False,
}

# 구조물 마커 색상 시각화 구현
for _, row in df.iterrows():
    x, y = row["x"], row["y"]
    struct = row["struct_name"]

    if struct == "Empty":
        continue

    if struct == "Apartment":
        plt.scatter(x, y, marker="o", color="brown", label="Apartment" if not labeled["Apartment"] else None)
        labeled["Apartment"] = True
    elif struct == "Building":
        plt.scatter(x, y, marker="o", color="brown", label="Building" if not labeled["Building"] else None)
        labeled["Building"] = True
    elif struct == "BandalgomCoffee":
        plt.scatter(x, y, marker="s", color="green", label="BandalgomCoffee" if not labeled["BandalgomCoffee"] else None)
        labeled["BandalgomCoffee"] = True
    elif struct == "MyHome":
        plt.scatter(x, y, marker="^", color="green", label="MyHome" if not labeled["MyHome"] else None)
        labeled["MyHome"] = True

# 건설 현장 마지막에 덮어쓰기
for _, row in df[df["ConstructionSite"] == 1].iterrows():
    x, y = row["x"], row["y"]
    if not labeled["ConstructionSite"]:
        plt.scatter(x, y, marker="s", color="gray", label="ConstructionSite")
        labeled["ConstructionSite"] = True
    else:
        plt.scatter(x, y, marker="s", color="gray") 

plt.legend(
    loc='upper left',
    bbox_to_anchor=(1.05, 1),
    borderaxespad=0.
)
plt.tight_layout()
plt.savefig("result/map.png", bbox_inches='tight')
plt.close()