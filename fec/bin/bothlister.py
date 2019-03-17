import json
import numpy

state_abbr = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 
'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO',
'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 
'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

add_2 = {}

def both (year):
    with open ("fec/data/{}/S-{}-datasets-2.json".format(year, year), "r") as senate_f:
        sn = json.load (senate_f)

    with open ("fec/data/{}/H-{}-datasets-2.json".format(year, year), "r") as house_f:
        hs = json.load (house_f)

    for state in state_abbr:
        spending = []
        votes = []
        for district in hs[state]["results"]:
            for candidate in hs[state]["results"][district]:
                if candidate["general_votes"] == 0 or candidate["general_votes"] == "Unopposed":
                    pass
                elif candidate["spending_share"] == "No Data" or candidate["general_votes"] == "No Data":
                    pass
                elif candidate["general_win"] == "ploser" or candidate["operating_expenditure"] == 0:
                    pass
                elif candidate["operating_expenditure"] == "No Data":
                    pass
                else:
                    spending.append(candidate["spending_share"])
                    votes.append(candidate["general_share"])

        for candidate in sn[state]["results"]:
            if candidate["general_votes"] == 0 or candidate["general_votes"] == "Unopposed":
                pass
            elif candidate["spending_share"] == "No Data" or candidate["spending_share"] == 0 or candidate["general_votes"] == "No Data":
                pass
            elif candidate["primary_win"] == "ploser" or candidate["operating_expenditure"] == 0:
                pass
            elif candidate["operating_expenditure"] == "No Data":
                pass
            else:
                spending.append(candidate["spending_share"])
                votes.append(candidate["general_share"])

        x = numpy.array(spending).astype(numpy.float)
        y = numpy.array(votes).astype(numpy.float)
        print (len(spending), len(votes))


        if len (spending) < 3 or len (votes) < 3:
            print (state, " ", res.tolist()[0][1])
            add_2[state] = {"stats": { "correlation_coef": 0,
            "correlation_sample": "Not enough data sample  {}".format(len(spending))}}

        else:
            res = numpy.corrcoef(x, y)
            if res.tolist()[0][1] == res.tolist()[0][1]:
                print (state, " ", res.tolist()[0][1])
                add_2[state] = {"stats": { "correlation_coef": res.tolist()[0][1],
                "correlation_sample": len(spending)}}
            else:
                add_2[state] = {"stats": { "correlation_coef": 0,
                 "correlation_sample": "Not enough data sample  {}".format(len(spending))}}


        
    for state in state_abbr:
        spending_agg = 0
        spending_counter = 0
        for district in hs[state]["results"]:
            for candidate in hs[state]["results"][district]:
                
                if candidate["operating_expenditure"] == "No Data":
                    pass
                elif candidate["general_votes"] == 0:
                    pass
                else:
                    spending_counter +=1
                    spending_agg = spending_agg + candidate["operating_expenditure"]
        for candidate in sn[state]["results"]:
            if candidate["operating_expenditure"] == "No Data":
                pass
            elif candidate["general_votes"] == 0:
                pass
            else:
                spending_counter +=1
                spending_agg = spending_agg +candidate["operating_expenditure"]
        
        print (spending_agg, spending_counter)
        print (add_2)
        add_2[state]["stats"]["average_spending"] =  spending_agg/spending_counter
        
    for state in state_abbr:
        topspender_agg = 0
        topspender_counter = 0  
        for district in hs[state]["stats"]:
            if district == "ALL":
                pass
            else:
                topspender_agg = topspender_agg + hs[state]["stats"][district]["topspender_share"]
                topspender_counter +=1
        
        if len (sn[state]["results"]) == 0:
            pass
        else:
            topspender_agg = topspender_agg + sn[state]["stats"]["topspender_share"]
            topspender_counter +=1
        
        add_2[state]["stats"]["topspender_share"] = topspender_agg/topspender_counter

        

    #################NATIONAL STUFF #########################
    spending_na = []
    votes_na = []
    for state in hs:
        for district in hs[state]["results"]:
            for candidate in hs[state]["results"][district]:
                if candidate["general_votes"] == 0 or candidate["general_votes"] == "Unopposed":
                    pass
                elif candidate["spending_share"] == "No Data" or candidate["general_votes"] == "No Data":
                    pass
                elif candidate["general_win"] == "ploser" or candidate["operating_expenditure"] == 0:
                    pass
                elif candidate["operating_expenditure"] == "No Data":
                    pass
                else:
                    spending_na.append(candidate["spending_share"])
                    votes_na.append(candidate["general_share"])


    for state in sn:
        for candidate in sn[state]["results"]:
            if candidate["general_votes"] == 0 or candidate["general_votes"] == "Unopposed":
                pass
            elif candidate["spending_share"] == "No Data" or candidate["spending_share"] == 0 or candidate["general_votes"] == "No Data":
                pass
            elif candidate["primary_win"] == "ploser" or candidate["operating_expenditure"] == 0:
                pass
            elif candidate["operating_expenditure"] == "No Data":
                pass
            else:
                spending_na.append(candidate["spending_share"])
                votes_na.append(candidate["general_share"])


    x = numpy.array(spending_na).astype(numpy.float)
    y = numpy.array(votes_na).astype(numpy.float)
    print (len(spending_na), len(votes_na))
    if len (spending_na) < 3 or len (votes_na) < 3:
        print (state, " pass" )
        add_2["NA"] = {"stats": { "correlation_coef": 0,
        "correlation_sample": "Not enough data sample  {}".format(len(spending_na))}}
    else:
        res = numpy.corrcoef(x, y)
        if res.tolist()[0][1] == res.tolist()[0][1]:
            print (state, " ", res.tolist()[0][1])
            add_2["NA"] = {"stats": {"correlation_coef": res.tolist()[0][1],
            "correlation_sample": len(spending_na)}}
        else:
            add_2["NA"] = {"stats": { "correlation_coef": 0,
            "correlation_sample": "Not enough data sample  {}".format(len(spending_na))}}


    spending_agg_na = 0
    spending_counter_na = 0
    for state in state_abbr:
        for district in hs[state]["results"]:
            for candidate in hs[state]["results"][district]:
                if candidate["operating_expenditure"] == "No Data":
                    pass
                elif candidate["general_votes"] == 0:
                    pass
                else:
                    spending_counter_na +=1
                    spending_agg_na = spending_agg_na +candidate["operating_expenditure"]
        for candidate in sn[state]["results"]:
            if candidate["operating_expenditure"] == "No Data":
                pass
            elif candidate["general_votes"] == 0:
                pass
            else:
                spending_counter_na +=1
                spending_agg_na = spending_agg_na +candidate["operating_expenditure"]
        
    print (spending_agg_na, spending_counter_na)
    add_2["NA"]["stats"]["average_spending"] = spending_agg_na/spending_counter_na

    topspender_agg_na = 0
    topspender_counter_na = 0
    for state in state_abbr:  
        for district in hs[state]["stats"]:
            if district == "ALL":
                pass
            else:
                topspender_agg_na = topspender_agg_na + hs[state]["stats"][district]["topspender_share"]
                topspender_counter_na +=1
        
        if len (sn[state]["results"]) == 0:
            pass
        else:
            topspender_agg_na = topspender_agg_na + sn[state]["stats"]["topspender_share"]
            topspender_counter_na +=1
        
    add_2["NA"]["stats"]["topspender_share"] = topspender_agg_na/topspender_counter_na



    with open ("fec/data/{}/B-{}-datasets-2.json".format(year, year), "w+") as write_f:
        json.dump(add_2, write_f, indent=2)


for race in [2016, 2014, 2012, 2010, 2008, 2006, 2004]:
    print (race)
    both (race)