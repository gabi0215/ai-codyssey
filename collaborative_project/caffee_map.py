import zipfile
import os
import pandas as pd

# 압축 파일 경로(해당 파일이 폴더 내 존재할 때)
zip_path = "dataFile.zip"

# 압축해제 할 위치(프로젝트 폴더 내 압축 해제할 폴더 생성)
extract_dir = "./area_csv"

# 폴더 없으면 자동 생성
os.makedirs(extract_dir, exist_ok=True)

# 압축 해제하기.
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# 압축 해제된 3가지 파일 경로 
map_path = os.path.join(extract_dir, 'area_map.csv')
struct_path = os.path.join(extract_dir, 'area_struct.csv')
category_path = os.path.join(extract_dir, 'area_category.csv')

# 압축이 해제된 3가지 파일의 경로를 변수 지정했으니 Panddas로 불러오기
df_map = pd.read_csv(map_path)
df_struct = pd.read_csv(struct_path)
df_category = pd.read_csv(category_path)

# area_categoty.csv 컬럼중 공백을 제거합니다.
df_category.columns = df_category.columns.str.strip()

# df_struct의 category 컬럼의 숫자형 ID를 구조물 이름으로 매핑
df_struct_named = pd.merge(df_struct, df_category, on='category', how='left')

# 매핑된 컬럼의 이름을 변경합니다.
df_struct_named = df_struct_named.rename(columns={'struct': 'struct_name'})

# struct_name 컬럼 값 내부 공백 제거
df_struct_named['struct_name'] = df_struct_named['struct_name'].str.strip()

# MyHome 을 직접 좌표값을 지정
myhome_row = pd.DataFrame([{
    'x': 2,
    'y': 10,
    'category': 3,
    'area': 1,
    'struct_name': 'MyHome'
}])

# 공백 제거 및 직접 좌표값이 지정된 것을 concat
df_struct_named = pd.concat([df_struct_named, myhome_row], ignore_index=True)

# map과 struct_named 를 merge 합니다.
df_merged = pd.merge(df_map, df_struct_named, on=['x', 'y'], how = 'left')

# area == 1 필터링
# 1과 같다면 Booleand 배열로 1이면 True, 행만 골라 반환
df_area_1 = df_merged[df_merged['area'] == 1]

# 구조물 통계 처리(Pandas 메서드 groupby,size,reset_index)
struct_summary = df_area_1.groupby('struct_name').size().reset_index(name='count')

# 결과 저장 폴더
result_dir = "result"

# 폴더 없으면 자동 생성
os.makedirs(result_dir, exist_ok=True)

# 통계 요약 결과 저장
summary_path = os.path.join(result_dir, "struct_summary.csv")
struct_summary.to_csv(summary_path, index=False)

# 파일 경로 설정
result_path = os.path.join(result_dir, "caffee_map.csv")

# 저장하기
df_area_1.to_csv(result_path, index=False)

# print(f"csv 파일 저장 완료: {result_path}")

