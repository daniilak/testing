from lib import *

# Второе задание
def read_zip_file(name_tmp_folder: str) -> None:
    zip_archive = ZipFile(f"res/{name_tmp_folder}.zip", "r")

    for file_info in zip_archive.infolist():
        xml_data = zip_archive.read(file_info.filename)
    
    root = fromstring(xml_data)

    first = [root.find(".//*[@name='id']").get('value'), root.find(".//*[@name='level']").get('value')]
    second = [elem.get('value') for elem in root.find("objects").findall("object")]
    
    return first, second


# Пока что без паралелльного вычисления
csv_data_1 = []
csv_data_2 = []
for i in range(1, 51):
    first, second = read_zip_file(str(i))
    csv_data_1.append(first)
    for el in second:
        csv_data_2.append([first[0], el])

df1 = pd.DataFrame(csv_data_1)
df2 = pd.DataFrame(csv_data_2)
df1.to_csv('res1.csv', encoding='utf-8', header=False, index=False)
df2.to_csv('res2.csv', encoding='utf-8', header=False, index=False)
