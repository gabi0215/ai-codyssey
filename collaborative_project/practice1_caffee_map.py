import zipfile
import os
import pandas as pd

# 압축 파일 경로(해당 파일이 폴더 내 존재할 때)
zip_path = "dataFile.zip"

# 압축해제 할 위치(프로젝트 폴더 내 압축 해제할 폴더 생성)
extract_dir = "./area_csv"

# 압축 해제하기.
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# 압축 해제된 파일 경로 3가지
map_path = os.path.join(extract_dir, 'area_map.csv')
struct_path = os.path.join(extract_dir, 'area_struct.csv')
category_path = os.path.join(extract_dir, 'area_category.csv')

# 압축이 해제된 3가지 파일의 경로를 변수 지정했으니 Panddas로 불러오기
df_map = pd.read_csv(map_path)
df_struct = pd.read_csv(struct_path)
df_category = pd.read_csv(category_path)

# 전체 구조 요약(df_변수명.info())

# # 225개의 행, 3개의 컬럼(x, y,ConsturctionsSite 225개, 결측치X type->int64
# print("📊 area_map.csv 구성:")
# print(df_map.info())
# print()

# # 225개의 행, 4개의 컬럼(x, y, category, area 225개, 결측치X type->int64
# print("📊 area_struct.csv 구성:")
# print(df_struct.info())
# print()

# # 4개의 행, 2개의 컬럼(category, struct 4개, 결측치X type->int64+문자열
# print("📊 area_category.csv 구성:")
# print(df_category.info())

# df_struct의 category 컬럼의 숫자형 ID를 구조물 이름으로 매핑
df_struct_named = pd.merge(df_struct, df_category, on='category', how='left')

# 공백 컬럼 정리 (중요!)
df_struct_named.columns = df_struct_named.columns.str.strip()

# 매핑된 컬럼의 이름을 변경합니다.
df_struct_named = df_struct_named.rename(columns={'struct': 'struct_name'})

# 컬럼 확인
print(df_struct_named.columns)

# 추가 및 컬럼명 수정 결과 확인하기
print("구조물 이름이 매핑된 df_struct:")
print(df_struct_named.head())

# map과 struct_named 를 merge 합니다.
df_merged = pd.merge(df_map, df_struct_named, on=['x', 'y'], how = 'left')

# area == 1 필터링
# 1과 같다면 Booleand 배열로 1이면 True, 행만 골라 반환
df_area_1 = df_merged[df_merged['area'] == 1]

print(df_area_1.columns)


# 구조물 통계 처리(Pandas 메서드 groupby,size,reset_index)
struct_summary = df_area_1.groupby('struct_name').size().reset_index(name='count')
print(struct_summary)

# 결과 저장 폴더
result_dir = "result"

# 폴더 없으면 자동 생성
os.makedirs(result_dir, exist_ok=True)

# 파일 경로 설정
result_path = os.path.join(result_dir, "caffe_map.csv")

# 저장하기
df_area_1.to_csv(result_path, index=False)

print(f"csv 파일 저장 완료: {result_path}")