# import json

# for i in range(2,15):
#     filename = f"case_redis_{i}.jl"
#     with open(filename, mode="r", encoding="utf-8") as f:
#         for line in f:
#             case = json.loads(line.strip())
#             doc_id = case.get("DocId", "")
#             case_number = case.get("CaseNo", "")
#             with open("panjueshu_source_id.dat", mode="a", encoding="utf-8") as s:
#                 s.write(doc_id + "\n")
#             with open("panjueshu_case_number.dat", mode="a", encoding="utf-8") as s:
#                 s.write(case_number + "\n")
count = 0
for i in range(15):
    filename = f"case_redis_{i}.jl"
    with open(filename, mode="r", encoding="utf-8") as f:
        for line in f:
            filename = str(count // 100000)
            with open(f"{filename}.dat", mode="a", encoding="utf-8") as s:
                s.write(line)
            count += 1
