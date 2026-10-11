import json
csv_file = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/01.first.csv"
clean_file = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/01.clean.json"

process_dict={}
list_with_dict = []

with open(csv_file, "r") as f:
    header = f.readline()
    #header = header.strip("\n")
    header = header.strip("\n").split(",")
    #print(header)
    header = [col.strip(" ").strip("'").strip('"').strip() for col in header]
    #header = [col.replace(" ", "").replace("'", "") for col in header]
    #header = [col.replace(" ", "") for col in header]
    #header = header.strip("\n")
    #header = header.strip(" ")
    #print(header)
    #header = header.split(",")

    #header_cnt = len(header)

    #d1, d2, d3 = header.split(",")
        
    for line in f:
        row_values = line.strip("\n").split(",")
        #print(row_values[0].strip("'").strip('"').strip(" "))
        row_values = [row.strip().strip("'").strip('"').strip() for row in row_values]
        #col_count = len(line.strip("\n").split(","))
        process_dict = dict(zip(header, row_values))
        #print(process_dict["Salary"])
        #print(process_dict)
        #print(process_dict)
        process_dict['Age'] = int(process_dict['Age'])
        salary = process_dict["Salary"].strip()

        try:
            
            if not salary:
                raise ValueError(f"{process_dict["Name"]} has no salary value, cant process.")
            elif int(process_dict["Salary"]) <= 0:
                raise ValueError(f"{process_dict["Name"]} has zero or negative salary, cant process.")
            else:
                process_dict['Salary'] = int(process_dict['Salary'])
                list_with_dict.append(process_dict)
        except Exception as e:
            print(f"Invalid Salary", e)
            continue
        #process_dict["Age"] = int(process_dict["Age"])
        #for n in range(header_cnt):
        #    process_dict[header[n]] = line.strip("\n").split(",")[n]
        #dr1, dr2, dr3 = line.strip("\n").split(",")
        
        #process_dict = {}
with open(clean_file, "w") as f:
    json.dump(list_with_dict, f, indent=4)
#print(list_with_dict)
#print(json.dumps(list_with_dict))


"""
str = '"Name Raghu"'
print(str)
print(str.replace(" ", ""))
"""

"""
str = "'O'Conner'"
print(str.strip("'"))
print(str.replace("'",""))
"""