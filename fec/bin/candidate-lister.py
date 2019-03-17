import json
import requests
import pandas
import numpy

key = "apikeyhere"
base_candidate = "https://api.open.fec.gov/v1/candidates"
add = {}

state_abbr = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
    'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
   
def candidates(state_inp, office_inp, year_inp):
    parameters = {"election_year": year_inp, "office": office_inp, "state": state_inp, "api_key": key, "per_page":100}
    response = requests.get(base_candidate, params=parameters)
    print(response.url)
    answer = response.json()
    for num in range(int(answer["pagination"]["count"])):
        operating_expenditure = total(answer["results"][num]["candidate_id"], year_inp)
        answer["results"][num]["operating_expenditure"] = operating_expenditure
    #writes = json.dumps(answer, indent=2)
    
    add["{}".format(state_inp)] = answer
    
def total (candidate_id, year):
    
    base_total = "https://api.open.fec.gov/v1/candidate/{}/totals".format(candidate_id)
    parameters = {"cycle":year, "per_page":100, "full_election":"true", "page": 1, "api_key":key}
    response = requests.get(base_total, params=parameters)
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
    
    # x = total returns a value of either 0 or net expenditure, this connects to candidates () line 23

def results(office, year): # adding election vote counts from excelspread sheet to the dict which will got to json
    office_letter =""
    if office == "S":
        office_letter= "Senate"
    elif office == "H":
        office_letter = "House"

    df = pandas.read_excel("fec/data/{}/federalelections{}.xls".format(year, year), sheet_name="{} US {} Results by State".format(year, office_letter))
    df["STATE ABBREVIATION"].fillna (" ", inplace=True) 
    df["PRIMARY VOTES"].fillna (0, inplace=True) 
    df["PRIMARY %"].fillna (0, inplace=True)   # so that for loop does not return nan as keyerror
    df["GENERAL VOTES"].fillna (0, inplace=True)    
    df["GENERAL %"].fillna (0, inplace=True)   # so that for loop does not return nan as keyerror
    
    
    for state in add:
            for individual_candidate in add[state]["results"]:
                #basically going through every candidates with these two loops
                if individual_candidate["candidate_id"] in str(df["FEC ID#"].values):
                    found = df.loc[ df ["FEC ID#"] == str(individual_candidate ["candidate_id"]) ]
                    individual_candidate["primary_votes"] = found["PRIMARY VOTES"].values[0]
                    individual_candidate["primary_share"] = found["PRIMARY %"].values[0]
                    individual_candidate["general_votes"] = found["GENERAL VOTES"].values[0]
                    individual_candidate["general_share"] = found["GENERAL %"].values[0]
                

def main (office, year):
    
    for state_query in state_abbr:
        candidates(state_query, office, year)

    with open ("fec/data/{}/{}-{}-datasets-financial.json".format(year, office, year), "w+") as financial_f:
        #test run so that result fail wont delete the whole thing writing a json file
        json.dump(add, financial_f, indent=2)

    #results(office, year)

    #with open ("fec/data/{}/{}-{}-datasets.json".format(year, office, year), "w+") as final:
        #finally writing a json file
    #    json.dump(add, fiann_f, indent=2)
        # not dump"s", in this case use dump
    

#print ("rquests made total :", counter + 50)

    #with open ("fec/senators2016-json.json", "r") as r:
        #load = json.loads(r.read())

    #with open ("fec/senators2016-json.json", "w") as w:
        #json.dump(load, w, indent=2)


## this function does not involve sending api requests.
def spreadsheet(office, year): # adding election vote counts from excelspread sheet to the dict which will got to json
    office_letter =""
    if office == "S":
        office_letter= "Senate"
    elif office == "H":
        office_letter = "House"

    with open ("fec/data/{}/{}-{}-datasets-financial.json".format(year, office, year), "r") as financial_read:
        #test run so that result fail wont delete the whole thing writing a json file
        add_2 = json.load(financial_read)
        df = pandas.read_excel("fec/data/{}/federalelections{}.xlsx".format(year, year), sheet_name="{} US {} Results by State".format(year, office_letter))
        df["STATE ABBREVIATION"].fillna (" ", inplace=True) 
        df["PRIMARY VOTES"].fillna (0, inplace=True) 
        df["PRIMARY %"].fillna (0, inplace=True)   # so that for loop does not return nan as keyerror
        df["GENERAL VOTES"].fillna (0, inplace=True)     
        df["GENERAL %"].fillna (0, inplace=True)   # so that for loop does not return nan as keyerror
        df = df.drop(df[df["PARTY"] == "W(R)"].index)  # for new hampshire has wiwered primary results
        df = df.drop(df[df["PARTY"] == "W(D)"].index)

        try:  # a GE Winner indicator for 2010 that does not have one
            df["GE WINNER INDICATOR"].fillna ("NG", inplace=True)
        except KeyError:
            pass
    
        for state in add_2:
            for individual_candidate in add_2[state]["results"]:
                del individual_candidate["last_f2_date"]
                del individual_candidate["last_file_date"]
                del individual_candidate["cycles"]
                del individual_candidate["election_years"]
                del individual_candidate["load_date"]
                ## remove some non-needed values
                del individual_candidate["first_file_date"]
                del individual_candidate["election_districts"]
                del individual_candidate["active_through"]

                ## original value zero
                individual_candidate["primary_votes"] = 0
                individual_candidate["primary_share"] = 0
                individual_candidate["general_votes"] = 0
                individual_candidate["general_share"] = 0
                individual_candidate["primary_win"] = 0
                individual_candidate["general_win"] = 0
                #basically going through every candidates with these two loops
                found = df[df["FEC ID#"].str.contains(individual_candidate["candidate_id"], na=False)]
                
                # do not use "if in" python generic check, it does not work for some senators
                if len(found["PRIMARY VOTES"].values.tolist()) == 0:
                    individual_candidate["primary_votes"] = 0
                else:
                    individual_candidate["primary_votes"] = found["PRIMARY VOTES"].values.tolist()[0]
        
                if len(found["PRIMARY %"].values.tolist()) == 0:
                    individual_candidate["primary_share"] = 0
                else:
                    individual_candidate["primary_share"] = found["PRIMARY %"].values.tolist()[0]

                if len(found["GENERAL VOTES"].values.tolist()) == 0:
                    individual_candidate["general_votes"] = 0
                else:
                    individual_candidate["general_votes"] = found["GENERAL VOTES"].values.tolist()[0]

                if len(found["GENERAL %"].values.tolist()) == 0:
                    individual_candidate["general_share"] = 0
                else:
                    individual_candidate["general_share"] = found["GENERAL %"].values.tolist()[0]

                            # .tolist() is needed to avoid numy array thing thats in excel sheet. 
                if individual_candidate["general_votes"] != 0:
                    individual_candidate["primary_win"] = "pwinner"
                elif individual_candidate["general_votes"] == 0:
                    individual_candidate["primary_win"] = "ploser"
                    ## adding results 
            # a GE Winner indicator for 2010 that does not have one add all number to the list and add get the heighest
            general_votes_list = [0]
                
            for candidate in add_2[state]["results"]:
                if candidate["general_votes"] == "#" or candidate["general_votes"] == "##":
                    pass
                else:           
                    print (candidate)
                    general_votes_list.append(candidate["general_votes"])
                    general_votes_list.sort(reverse = True)
        
            for candidate in add_2[state]["results"]:
                if general_votes_list[0] == candidate["general_votes"]:
                    candidate["general_win"] = "gwinner"
                else:
                    candidate["general_win"] = "gloser"

      
        ##################### adding state average spending and spending share ##################
        for state in add_2:
            gen_state_aggregate = 0
            gen_agg_counter = 0
            for candidates in add_2[state]["results"]:
            
### creating a new section of json file called "stats" 
# ##KeyError: 'stats' for "add_2[state]["stats"]["average_spending"] ="
                            
                if candidates["operating_expenditure"] == "No Data":
                    pass
                elif candidates["general_votes"] == 0:
                    pass
                else:   # to calcurate spending rate, this is calcurating aggregate expenditure in taht state
                    gen_agg_counter +=1
                    #print (candidates["name"], candidates["operating_expenditure"], agg_counter)
                    gen_state_aggregate = candidates["operating_expenditure"]+gen_state_aggregate
                
                             ##dividing the aggregate with a number of people with finanical data
            if gen_agg_counter == 0:
                add_2[state]["stats"] = {"average_spending": 0}
            else:    
                add_2[state]["stats"] = {"average_spending":gen_state_aggregate/gen_agg_counter}
                # now calcurating individual spending share we use general election only data 
            
            for candidate in add_2[state]["results"]: 
                if candidate["operating_expenditure"] == "No Data":
                    candidate["spending_share"] = "No Data"
                    candidate["performance"] = "No Data"
                
                elif candidate["general_votes"] == 0:
                    candidate["spending_share"] = "No Data"
                    candidate["performance"] = "No Data"
    
                else:
                    try:
                    #print (candidate["name"])
                        candidate["spending_share"] = candidate["operating_expenditure"] / gen_state_aggregate #read[state][""]
                    except ZeroDivisionError:
                        candidate["spending_share"] = 0
                    try:
                    #print (candidate["name"])
                        candidate["spending_share"] = candidate["operating_expenditure"] / gen_state_aggregate #read[state][""]
                        candidate["performance"] = candidate["general_share"]/candidate["spending_share"]
                ## if candidate A got 60% of votes and spent 40% he/she is overperforming by 1.5, (60/40)
                    except ZeroDivisionError:
                        candidate["performance"] = "spending_share was 0"
            
            
            spending_list = []
            for candidate in add_2[state]["results"]:
                if candidate["spending_share"] == "No Data":
                    pass
                else: # I wanna keep "No Data" and dont wanna replace no data with 0 to avoid number string mixture, 
                    spending_list.append(candidate["spending_share"])
            
            sorteddic = sorted(spending_list, reverse=True)
             ### sorting the candidates by their spending amount 
            if len(sorteddic) == 0:  ##### topspender's spending share
                topspender = 0
                add_2[state]["stats"]["topspender_share"] = topspender
            else:
                topspender = sorteddic[0]
                add_2[state]["stats"]["topspender_share"] = topspender
                
            for candidate in add_2[state]["results"]:
                if topspender == candidate["spending_share"]:
                    add_2[state]["stats"]["topspender_name"] = candidate["name"]
            
            if topspender == 0:
                add_2[state]["stats"]["topspender_name"] = "No Data"
                        

        for state in add_2:
            spending = []
            votes = []
            for candidate in add_2[state]["results"]:
                if candidate["general_votes"] == 0 or candidate["general_votes"] == "Unopposed":
                    pass
                elif candidate["spending_share"] == "No Data" or candidate["spending_share"] == 0 or candidate["operating_expenditure"] == 0:
                    pass
                elif candidate["primary_win"] == "ploser" or candidate["general_votes"] == "No Data":
                    pass
                else:
                    spending.append(candidate["spending_share"])
                    votes.append(candidate["general_share"])

            x = numpy.array(spending).astype(numpy.float)
            y = numpy.array(votes).astype(numpy.float)
            print (len(spending), len(votes))

            if len (spending) < 2 or len (votes) < 2:
                print (state, " pass")
                add_2[state]["stats"]["correlation_coef"] = 0
                add_2[state]["stats"]["correlation_sample"] = "Not enough data sample : {}".format(len(spending))
            else:
                res = numpy.corrcoef(x, y)
                if res.tolist()[0][1] == res.tolist()[0][1]:
                    print (state, " ", res.tolist()[0][1])
                    add_2[state]["stats"]["correlation_coef"] = res.tolist()[0][1]
                    add_2[state]["stats"]["correlation_sample"] = len(spending)
                else:
                    add_2[state]["stats"]["correlation_coef"] = 0
                    add_2[state]["stats"]["correlation_sample"] = "Not enough data sample : {}".format(len(spending))
        national_spending = 0
        national_spending_count = 0
        national_topspender = 0
        national_topspender_count = 0

        for state in add_2:
            if len(add_2[state]["results"]) == 0:
                pass
            else:
                national_spending_count +=1 
                national_topspender_count +=1 
                national_spending = national_spending + add_2[state]["stats"]["average_spending"] 
                national_topspender = national_topspender + add_2[state]["stats"]["topspender_share"]
        
        print (national_spending,
        national_spending_count,
        national_topspender,
        national_topspender_count)

        add_2["NA"] = { "results":[], "pagination": {"count": 0}, "stats": {"average_spending": national_spending/national_spending_count, 
        "topspender_share":national_topspender/national_topspender_count, "topspender_name": "No Data"}}
        

        spending = []
        votes = []
        for state in add_2:
            for candidate in add_2[state]["results"]:
                if candidate["general_votes"] == 0 or candidate["general_votes"] == "Unopposed":
                    pass
                elif candidate["spending_share"] == "No Data" or candidate["spending_share"] == 0 or candidate["general_votes"] == "No Data":
                    pass
                elif candidate["primary_win"] == "ploser" or candidate["operating_expenditure"] == 0:
                    pass
                else:
                    spending.append(candidate["spending_share"])
                    votes.append(candidate["general_share"])

        x = numpy.array(spending).astype(numpy.float)
        y = numpy.array(votes).astype(numpy.float)
        print (len(spending), len(votes))


        if len (spending) < 2 or len (votes) < 2:
            print (state, " ", res.tolist()[0][1])
            add_2["NA"]["stats"]["correlation_coef"] = 0
            add_2["NA"]["stats"]["correlation_sample"] = "Not enough data sample : {}".format(len(spending))

        else:
            res = numpy.corrcoef(x, y)
            if res.tolist()[0][1] == res.tolist()[0][1]:
                print (state, " ", res.tolist()[0][1])
                add_2["NA"]["stats"]["correlation_coef"] = res.tolist()[0][1]
                add_2["NA"]["stats"]["correlation_sample"] = len(spending)
            else:
                add_2["NA"]["stats"]["correlation_coef"] = 0
                add_2["NA"]["stats"]["correlation_sample"] = "Not enough data sample : {}".format(len(spending))


        with open ("fec/data/{}/{}-{}-datasets-2.json".format(year, office, year), "w+") as write_f:
            #finally writing a json file
            json.dump(add_2, write_f, indent=2)
            #try:        
            #    json.dump(add_2, write_f, indent=2)
            #except TypeError:
            #    print (add_2)

#main("H", 2016)
#spreadsheet("S", 2016)
for race in [2016, 2014, 2012, 2010, 2008, 2006, 2004]:
    spreadsheet("S", race)


     

