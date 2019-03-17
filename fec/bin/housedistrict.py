import json 
import pandas

df = pandas.read_excel("fec/data/house-districts.xlsx")

add = {}
for index, item in df.iterrows():
    add[item["State"]] = {"districts": item["Seats2000"], "stats":{}, "results":{}}
    print (item)
    total = int(item["Seats2000"])+1
    for num in range(1, total):
        district = "{}{}".format(item["State"], num)
        add[item["State"]]["results"][district] = []
        add[item["State"]]["stats"][district] = []
    
with open ("fec/data/HouseSeats2000census.json", "w+") as write:
    json.dump(add, write, indent=2)

