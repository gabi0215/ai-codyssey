import pandas as pd
import os
import matplotlib.pyplot as plt

# 1단계에서 생성된 결과 파일 경로를 지정합니다.
csv_path = os.path.join("result", "caffe_map.csv")
print(os.path.exists(csv_path))  # True가 나오면 존재함
# csv 파일 읽기
df = pd.read_csv(csv_path)

# print(df.head())

x_min, x_max = df["x"].min(), df["x"].max()
y_min, y_max = df["y"].min(), df["y"].max()


# plt 객체를 불러와서 그래프 임의로 크기 생성
plt.figure(figsize=(8, 6))
# 격자선 표시
plt.grid(True)
# Get Current Axes y좌표축 반전
plt.gca().invert_yaxis

# 구조물 마커 색상 시각화 구현
for _, row in df.iterrows():
    x, y = row["x"], row["y"]
    struct = row["struct_name"]

    if struct == "Apartment":
        plt.scatter(x, y, marker="o", color="brown", label="Apartment")
    elif struct == "Building":
        plt.scatter(x, y, marker="o", color="brown", label="Building")
    elif struct == "BandalgomCoffee":
        plt.scatter(x, y, marker="s", color="green", label="BandalgomCoffee")
    elif struct == "MyHome":
        plt.scatter(x, y, marker="^", color="green", label="MyHome")

already_labeled = False
for _, in row in df[df["ConsturctionSite"] == 1].iterrows():
    x, y = row["x"], row["y"]
    if not already_labeled:
        plt.scatter(x, y, marker="s", color="gray", label="ConstructionStie")
        already_labeled = True
    else:
        plt.scatter(x, y, marker="s", color="gray") 
