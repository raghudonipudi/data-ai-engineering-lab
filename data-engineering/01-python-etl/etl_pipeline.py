csv_file = "/Volumes/Transcend/data-ai-engineering-lab/data-samples/01.first.csv"

process_dict={}
list_with_dict = []

with open(csv_file, "r") as f:
    header = f.readline()
    #header = header.strip("\n")
    header = header.strip("\n").split(",")
    #header_cnt = len(header)

    #d1, d2, d3 = header.split(",")
        
    for line in f:
        row_values = line.strip("\n").split(",") 
        #col_count = len(line.strip("\n").split(","))
        process_dict = dict(zip(header, row_values))
        #for n in range(header_cnt):
        #    process_dict[header[n]] = line.strip("\n").split(",")[n]
        #dr1, dr2, dr3 = line.strip("\n").split(",")
        list_with_dict.append(process_dict)
        #process_dict = {}

print(list_with_dict)