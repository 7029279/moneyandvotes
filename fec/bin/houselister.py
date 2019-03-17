import json
import requests
import pandas
import numpy
import time
from datetime import datetime
add = {}
key = "apikey here"

state_abbr = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 
'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

api_count = 0

def timer ():
    global api_count 
    api_count +=1
    if api_count == 450:
        print ("begin sleep at ", datetime.now())
        time.sleep(1800)
        api_count = 0
    else:
        pass

def candidates(state_inp, office_inp, year_inp):
    base_candidate = "https://api.open.fec.gov/v1/candidates"
    parameters = {"election_year": year_inp, "office": office_inp, "state": state_inp, "page":1, "api_key": key, "per_page":100}
    response = requests.get(base_candidate, params=parameters)
    timer()
    print(response.url)
    answer = response.json()
    if answer["pagination"]["pages"] > 1:
        for page in range (2, answer["pagination"]["pages"]+1):
            parameters["page"] = page
            response = requests.get(base_candidate, params=parameters)
            print(response.url)
            answer_rest = response.json()
            answer["results"] = answer["results"]+answer_rest["results"]
        
    for num in range(len(answer["results"])):
        operating_expenditure = total(answer["results"][num]["candidate_id"], year_inp)
        answer["results"][num]["operating_expenditure"] = operating_expenditure
    
    add["{}".format(state_inp)] = answer
    
def total (candidate_id, year):
    
    base_total = "https://api.open.fec.gov/v1/candidate/{}/totals".format(candidate_id)
    parameters = {"cycle":year, "per_page":100, "full_election":"true", "page": 1, "api_key":key}
    response = requests.get(base_total, params=parameters)
    timer()
    print (response.url)
    answer = response.json()
    if answer["pagination"]["count"] == 0:
        return "No Data"
    elif answer["pagination"]["count"] == None:
        return "No Data"
    if year == 2004:  ## 2004 candidates have data in "operating_expenditures" but not in net_ eoperating_expenditures
        operating_expenditure = answer["results"][0]["operating_expenditures"]
        return operating_expenditure
    else:
        operating_expenditure = answer["results"][0]["net_operating_expenditures"]
        return operating_expenditure
    


def districtize (office, year):
    if year in [2016, 2014, 2012]:
        redistricting = 2010
    elif year in [2010, 2008, 2006, 2004]: 
        redistricting = 2000
    
    with open ("fec/data/{}/{}-{}-datasets-financial.json".format(year, office, year), "r") as financial_read:
        #test run so that result fail wont delete the whole thing writing a json file
        fread = json.load(financial_read)
        for state in fread:
            for candidate in fread[state]["results"]:
                if candidate["election_districts"][0] is None or candidate["district_number"] is None:
                    continue
                this_year = candidate["election_years"].index(year)
                this_yaer_district = int(candidate["election_districts"][this_year])
                candidate["district_number"] = this_yaer_district
            
                del candidate["last_f2_date"]
                del candidate["last_file_date"]
                del candidate["cycles"]
                del candidate["election_years"]
                del candidate["load_date"]
                ## remove some non-needed values
                del candidate["first_file_date"]
                del candidate["election_districts"]
                del candidate["active_through"]
                
        
                if candidate["district_number"] == None:
                    continue
                elif candidate["district_number"] == 0:
                    candidate["district_number"] = 1
                    candidate["district"] = "{}{}".format(state, candidate["district_number"])
                else:
                    candidate["district"] = "{}{}".format(state, candidate["district_number"])

          

        with open ("fec/data/HouseSeats{}census.json".format(redistricting), "r") as distr_read:
            dread = json.load (distr_read)
            
            for state in dread:
                for district in dread[state]["results"]:
                    in_this_district = []
                    for candidate in fread[state]["results"]:
                        print (candidate["district"])
                        if candidate["district"] == str(district):
                            in_this_district.append(candidate)
                            dread[state]["results"][district] = in_this_district
                        
            
    with open ("fec/data/{}/{}-{}-datasets-distr.json".format(year, office, year), "w+") as distr:
            #test run so that result fail wont delete the whole thing writing a json file
            json.dump(dread, distr, indent=2)
                    

def main (office, year):
    try:
        for state_query in state_abbr:
            candidates(state_query, office, year)
        with open ("fec/data/{}/{}-{}-datasets-financial.json".format(year, office, year), "w+") as financial_f:
            #test run so that result fail wont delete the whole thing writing a json file
            json.dump(add, financial_f, indent=2)
    except KeyError:
        with open ("fec/data/{}/{}-{}-datasets-financial.json".format(year, office, year), "w+") as financial_f:
            #test run so that result fail wont delete the whole thing writing a json file
            json.dump(add, financial_f, indent=2)

    districtize (office, year)

    
#time.sleep(3600)
for year in [2016, 2014, 2012, 2010, 2008, 2006, 2004]:
    districtize ("H", year)
#    main("H", year)
#time.sleep(1800)
#main("H", 2006)
#time.sleep(2000)
#main("H", 2004)


def spreadsheet(office, year): # adding election vote counts from excelspread sheet to the dict which will got to json
    office_letter =""
    if office == "S":
        office_letter= "Senate"
    elif office == "H":
        office_letter = "House"

    with open ("fec/data/{}/{}-{}-datasets-distr.json".format(year, office, year), "r") as distr_read:
        #test run so that result fail wont delete the whole thing writing a json file
        add_2 = json.load(distr_read)

        df = pandas.read_excel("fec/data/{}/federalelections{}.xlsx".format(year, year), sheet_name="{} US {} Results by State".format(year, office_letter))
        df["STATE ABBREVIATION"].fillna (" ", inplace=True) 
        df["GENERAL VOTES"].fillna (0, inplace=True)     
        df["GENERAL %"].fillna (0, inplace=True)   # so that for loop does not return nan as keyerror
        df = df.drop(df[df["PARTY"] == "W(R)"].index)  # for new hampshire has wiwered primary results
        df = df.drop(df[df["PARTY"] == "W(D)"].index)

        try:  # a GE Winner indicator for 2010 that does not have one
            df["GE WINNER INDICATOR"].fillna ("NG", inplace=True)
        except KeyError:
            pass
    
        for state in add_2:
            for district in add_2[state]["results"]:
                for candidate in add_2[state]["results"][district]:
                    ## original value zero
                    candidate["general_votes"] = 0
                    candidate["general_share"] = 0
                    candidate["general_win"] = 0
                    candidate["unopposed"] = "No"

                #basically going through every candidates with these three loops
                    found = df[df["FEC ID#"].str.contains(candidate["candidate_id"], na=False)]
                
                # do not use "if in" python generic check, it does not work for some senators
            
                    if len(found["GENERAL VOTES"].values.tolist()) == 0:
                        candidate["general_votes"] = 0
                    else:
                        candidate["general_votes"] = found["GENERAL VOTES"].values.tolist()[0]

                    if len(found["GENERAL %"].values.tolist()) == 0:
                        candidate["general_share"] = 0
                    else:
                        candidate["general_share"] = found["GENERAL %"].values.tolist()[0]

                        # .tolist() is needed to avoid numy array thing thats in excel sheet. 
            # a GE Winner indicator for 2010 that does not have one add all number to the list and add get the heighest
            
             # counting how many district there are and putting it under state[stats] 
            
            for district in add_2[state]["results"]:
                general_votes_list = [0]
                for candidate in add_2[state]["results"][district]:
                    if candidate["general_votes"] == "#" or candidate["general_votes"] == "##":
                        candidate["general_votes"] = 0
                    elif candidate["general_votes"] == "Unopposed":
                        candidate["unopposed"] = "Unopposed" #default is already "No"
                        candidate["general_win"] = "gwinner"
                    else:           
                        general_votes_list.append(candidate["general_votes"])
                
                print (general_votes_list, year, district)
                general_votes_list.sort(reverse = True)
            
                for candidate in add_2[state]["results"][district]:
                    if general_votes_list[0] == candidate["general_votes"]:
                        candidate["general_win"] = "gwinner"
                    else:
                        candidate["general_win"] = "gloser"
               
                for candidate in add_2[state]["results"][district]:
                    if candidate["unopposed"] == "No" and candidate["general_votes"] == 0:
                        print (candidate["name"])
                        candidate["general_win"] = "ploser"

              
        ##################### adding state average spending and spending share ##################
        for state in add_2:
            for district in add_2[state]["results"]:
                district_aggregate = 0
                district_agg_counter=0
                for candidates in add_2[state]["results"][district]:
                    if candidates["operating_expenditure"] == "No Data":
                        pass
                    elif candidates["general_votes"] == 0:
                        pass
                    else:   # to calcurate spending rate, this is calcurating aggregate expenditure in taht state
                        district_agg_counter +=1
                        #print (candidates["name"], candidates["operating_expenditure"], agg_counter)
                        district_aggregate = candidates["operating_expenditure"]+district_aggregate
                    
                             ##dividing the aggregate with a number of people with finanical data
                if  district_agg_counter == 0:
                    add_2[state]["stats"][district] = {"average_spending": 0}
                else:    
                    add_2[state]["stats"][district] = {"average_spending":district_aggregate/district_agg_counter}
                    # now calcurating individual spending share we use general election only data 
            
                for candidate in add_2[state]["results"][district]: 
                    if candidate["operating_expenditure"] == "No Data":
                        candidate["spending_share"] = "No Data"
                        candidate["performance"] = "No Data"
                    
                    elif candidate["general_votes"] == 0:
                        candidate["spending_share"] = "No Data"
                        candidate["performance"] = "No Data"
    
                    else:
                        try:
                        #print (candidate["name"])
                            candidate["spending_share"] = candidate["operating_expenditure"] /district_aggregate #read[state][""]
                        except ZeroDivisionError:
                            candidate["spending_share"] = 0
                        try:
                        #print (candidate["name"])
                            candidate["spending_share"] = candidate["operating_expenditure"] / district_aggregate #read[state][""]
                            candidate["performance"] = candidate["general_share"]/candidate["spending_share"]
                    ## if candidate A got 60% of votes and spent 40% he/she is overperforming by 1.5, (60/40)
                        except ZeroDivisionError:
                            candidate["performance"] = "spending_share was 0"
            
                spending_list = []
                for candidate in add_2[state]["results"][district]:
                    if candidate["spending_share"] == "No Data":
                        pass
                    else: # I wanna keep "No Data" and dont wanna replace no data with 0 to avoid number string mixture, 
                        spending_list.append(candidate["spending_share"])
                
                sorteddic = sorted(spending_list, reverse=True)
                ### sorting the candidates by their spending amount 
                if len(sorteddic) == 0:  ##### topspender's spending share
                    topspender = 0
                    add_2[state]["stats"][district]["topspender_share"] = topspender
                else:
                    topspender = sorteddic[0]
                    add_2[state]["stats"][district]["topspender_share"] = topspender
                
                for candidate in add_2[state]["results"][district]:
                    if topspender == candidate["spending_share"]:
                        add_2[state]["stats"][district]["topspender_name"] = candidate["name"]
            
                if topspender == 0:
                    add_2[state]["stats"][district]["topspender_name"] = "No Data"

    
        for state in add_2:
            state_spending = 0
            state_topspender = 0
            
            for district in add_2[state]["stats"]:
                    state_spending = state_spending + add_2[state]["stats"][district]["average_spending"]
                    state_topspender = state_topspender + add_2[state]["stats"][district]["topspender_share"]

            add_2[state]["stats"]["ALL"] = {"average_spending": state_spending/add_2[state]["districts"], 
            "topspender_share":state_topspender/add_2[state]["districts"]}

        for state in add_2:
            spending = []
            votes = []
            for district in add_2[state]["results"]:
                for candidate in add_2[state]["results"][district]:
                    if candidate["general_votes"] == 0 or candidate["general_votes"] == "Unopposed":
                        pass
                    elif candidate["spending_share"] == "No Data" or candidate["general_votes"] == "No Data":
                        pass
                    elif candidate["general_win"] == "ploser" or candidate["operating_expenditure"] == 0:
                        pass
                    else:
                        spending.append(candidate["spending_share"])
                        votes.append(candidate["general_share"])
            x = numpy.array(spending).astype(numpy.float)
            y = numpy.array(votes).astype(numpy.float)
            print (len(spending), len(votes))

            if len (spending) < 3 or len (votes) < 3:
                add_2[state]["stats"]["ALL"]["correlation_coef"] = 0
                add_2[state]["stats"]["ALL"]["correlation_sample"] = "Not enough data sample  {}".format(len(spending))
            else:
                res = numpy.corrcoef(x, y)
                print (state, " ", res.tolist()[0][1])
                if res.tolist()[0][1] == res.tolist()[0][1]:
                    add_2[state]["stats"]["ALL"]["correlation_coef"] = res.tolist()[0][1]
                    add_2[state]["stats"]["ALL"]["correlation_sample"] = len(spending)
                else:
                    add_2[state]["stats"]["ALL"]["correlation_coef"] = 0
                    add_2[state]["stats"]["ALL"]["correlation_sample"] = "Not enough data sample  {}".format(len(spending))

                
                    

           # calcurating national stats 
        national_spending = 0
        national_spending_count = 0
        national_topspender = 0
        national_topspender_count = 0

        for state in add_2: 
            national_spending_count +=1 
            national_topspender_count +=1
            national_spending = national_spending + add_2[state]["stats"]["ALL"]["average_spending"] 
            national_topspender = national_topspender + add_2[state]["stats"]["ALL"]["topspender_share"]
    
        print (national_spending,
        national_spending_count,
        national_topspender,
        national_topspender_count)

        add_2["NA"] = { "results":[], "stats": { "ALL": {"average_spending": national_spending/national_spending_count, 
        "topspender_share":national_topspender/national_topspender_count, "topspender_name": "No Data"}}}
        

        spending = []
        votes = []
        for state in add_2:
            for district in add_2[state]["results"]:
                for candidate in add_2[state]["results"][district]:
                    if candidate["general_votes"] == 0 or candidate["general_votes"] == "Unopposed":
                        pass
                    elif candidate["spending_share"] == "No Data" or candidate["spending_share"] == "No Data"  or candidate["general_votes"] == "No Data":
                        pass
                    elif candidate["general_win"] == "ploser" or candidate["operating_expenditure"] == 0:
                        pass
                    else:
                        spending.append(candidate["spending_share"])
                        votes.append(candidate["general_share"])

        x = numpy.array(spending).astype(numpy.float)
        y = numpy.array(votes).astype(numpy.float)
        print (len(spending), len(votes))

        if len (spending) < 3 or len (votes) < 3:
            print (state, " pass")
            add_2["NA"]["stats"]["ALL"]["correlation_coef"] = 0
            add_2["NA"]["stats"]["ALL"]["correlation_sample"] = "Not enough data sample : {}".format(len(spending))
    
        else:
            res = numpy.corrcoef(x, y)
            if res.tolist()[0][1] == res.tolist()[0][1]:
                print (state, " ", res.tolist()[0][1])
                add_2["NA"]["stats"]["ALL"]["correlation_coef"] = res.tolist()[0][1]
                add_2["NA"]["stats"]["ALL"]["correlation_sample"] = len(spending)
            else:
                add_2[state]["stats"]["ALL"]["correlation_coef"] = 0
                add_2["NA"]["stats"]["ALL"]["correlation_sample"] = "Not enough data sample : {}".format(len(spending))


        with open ("fec/data/{}/{}-{}-datasets-2.json".format(year, office, year), "w+") as write_f:
            #finally writing a json file
            json.dump(add_2, write_f, indent=2)
            #try:        
            #    json.dump(add_2, write_f, indent=2)
            #except TypeError:
            #    print (add_2)

#time.sleep(1800)
#main("H", 2014)
#spreadsheet("H", 2016)
for race in [2016, 2014, 2012, 2010, 2008, 2006, 2004]:
    spreadsheet("H", race)