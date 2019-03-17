import mysql.connector
import json
import csv

def add_candidates (office, year):
    mydb = mysql.connector.connect( 
        host="localhost",
        user="root",
        passwd="root",
        database='moneyandvotes'
    )   

    cur = mydb.cursor()
    cur.execute ("set @@sql_mode = ''")
    cur.execute ("CREATE TABLE IF NOT EXISTS {}{} (sqlid INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), state VARCHAR(255))".format(office, year)) 
    # you cannot use - for the name of table 
    cur.execute ("ALTER TABLE {}{} ADD COLUMN party VARCHAR(255)".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN fecid VARCHAR(255)".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN ranas VARCHAR(255)".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN expenditure INT".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN general_votes INT".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN general_share FLOAT".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN office VARCHAR(255)".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN general_win VARCHAR(255)".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN unopposed VARCHAR(255)".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN nodata VARCHAR(255)".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN spending_share FLOAT".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN performance FLOAT".format(office,year))
    cur.execute ("ALTER TABLE {}{} ADD COLUMN district VARCHAR(255)".format(office,year))

        # sqlid state party fecid ranas name
        # expenditure primary_votes, primary_share 
        # general_votes general _share office primary_win general_win		
    with open ("fec/data/{}/{}-{}-datasets-2.json".format (year, office, year), "r") as f:
        read = json.load(f)
        for state in read:                              
            for distrrict in read[state]["results"]:
                for individual in read[state]["results"][distrrict]:
                    if individual["general_votes"] == "Unopposed":
                        unopposed = "Unopposed"
                    else: 
                        unopposed = "No"

                    if individual["operating_expenditure"] == "No Data":
                        nodata = "Data unavailable"
                    else:
                        nodata = "Data available"
                        
                    if individual["operating_expenditure"] == 0 and individual["general_win"] == "ploser":
                        continue  ##elminating non-serious candidates
                    else:
                        pass
                        
                    if individual["party_full"] == "REPUBLICAN PARTY":
                        individual["party_full"] = "REPUBLICAN"
                    elif individual["party_full"] == "DEMOCRATIC PARTY":
                        individual["party_full"] = "DEMOCRAT"
                    elif individual["party_full"] == "LIBERTARIAN PARTY":
                        individual["party_full"] = "LIBERTARIAN"
                    elif individual["party_full"] == "GREEN PARTY":
                        individual["party_full"] = "GREEN"
                    
                    print (individual)
                    sql1 = "INSERT INTO {}{} (fecid, state, party, name, ranas, district , expenditure, general_votes, general_share, office,  general_win, unopposed, nodata, spending_share, performance) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s)".format (office, year)
                    val1 = (individual["candidate_id"], individual["state"], individual["party_full"], 
                    individual["name"], individual["incumbent_challenge_full"], individual["district"],
                    individual["operating_expenditure"], individual["general_votes"], individual["general_share"], individual["office_full"],
                    individual["general_win"], unopposed, nodata, individual["spending_share"], individual["performance"])

                    cur.execute(sql1, val1)

    cur.execute ("COMMIT")

    cur.close()
    mydb.close() # dont forget to close connections

#dbtry()


def drop (year): 
    mydb = mysql.connector.connect( 
        host="localhost",
        user="root",
        passwd="root",
        database='moneyandvotes'
    )
    cur = mydb.cursor()
    cur.execute ("set @@sql_mode = ''")
    print (year)
    if type(year) == int:
        print (year)
        cur.execute ("DROP TABLE `moneyandvotes`.`H{}`".format(year))
    if year == "stats":
        cur.execute ("DROP TABLE `moneyandvotes`.`{}`".format("stats"))
    elif year == "all":
        cur.execute ("DROP TABLE `moneyandvotes`.`H{}`".format(2016))
        cur.execute ("DROP TABLE `moneyandvotes`.`H{}`".format(2014))
        cur.execute ("DROP TABLE `moneyandvotes`.`H{}`".format(2012))
        cur.execute ("DROP TABLE `moneyandvotes`.`H{}`".format(2010))
        cur.execute ("DROP TABLE `moneyandvotes`.`H{}`".format(2008))
        cur.execute ("DROP TABLE `moneyandvotes`.`H{}`".format(2006))
        cur.execute ("DROP TABLE `moneyandvotes`.`H{}`".format(2004))
        cur.execute ("DROP TABLE `moneyandvotes`.`H{}`".format("stats"))

#drop("all")
#for num in [2016, 2014, 2012, 2010, 2008, 2006, 2004 ]: 
#	add_candidates ("S", num)

#drop (2016)
#add_candidates ("H", 2016)



def add_stats (office, year):
        

    mydb = mysql.connector.connect( 
        host="localhost",
        user="root",
        passwd="root",
        database='moneyandvotes'
    )

    cur = mydb.cursor()
    cur.execute ("set @@sql_mode = ''")
    try:
        cur.execute ("CREATE TABLE IF NOT EXISTS stats (id INT AUTO_INCREMENT PRIMARY KEY, oysd VARCHAR(255))")  
        cur = mydb.cursor()              ## yosd stands for office-y-state-district, for senate distict is 0
        cur.execute ("ALTER TABLE stats ADD COLUMN state VARCHAR(255)")
        cur.execute ("ALTER TABLE stats ADD COLUMN year INT")
        cur.execute ("ALTER TABLE stats ADD COLUMN office INT")
        cur.execute ("ALTER TABLE stats ADD COLUMN district VARCHAR(255)")

        cur.execute ("ALTER TABLE stats ADD COLUMN average_spending FLOAT")
        cur.execute ("ALTER TABLE stats ADD COLUMN topspender_share FLOAT")

    except mysql.connector.errors.ProgrammingError:
        pass

    if office == "S":
        district = 0   
    elif office == "H":
        pass
        

    with open ("fec/data/{}/{}-{}-datasets-2.json".format (year, office, year), "r") as f:
        read = json.load(f)
        for state in read:
            for district in read[state]["stats"]:
                if district == "ALL":
                    continue
                else:
                    sql1 = "INSERT INTO stats (oysd, state, year, office, district, average_spending, topspender_share) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                    val1 = ("{}{}{}{}".format(office, year, state, district), state, year, 
                    office, district, read[state]["stats"][district]["average_spending"],
                    read[state]["stats"][district]["topspender_share"])
                    cur.execute(sql1, val1)
                # for individual districts
                
            sql1 = "INSERT INTO stats (oysd, state, year, office, district, average_spending, topspender_share) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
            val1 = ("{}{}{}{}".format(office, year, state, 0), state, year, 
            office, district, read[state]["stats"]["ALL"]["average_spending"],
            read[state]["stats"]["ALL"]["topspender_share"])
            # for "ALL" statewide stats
            cur.execute(sql1, val1)
        cur.execute ("COMMIT")

## add csv files

    cur.close()
    mydb.close() # dont forget to close connections
drop("stats")
add_stats("H", 2016)

#for race in [2016, 2014, 2012, 2010, 2008, 2006, 2004]:
#	add_stats("S", race)

def tocsv (office, year):
    with open ("fec/data/{}/{}-{}-datasets-2.json".format (year, office, year), "r") as r:
        read = json.load(r)
        
        add = [["state","average_spending","topspender_share"]]
        for state in read:
            if len(read[state]["results"]) == 0:
                print (state)
                continue
            
                   ## skipping states that do not have election
            row = [state, read[state]["stats"]["average_spending"], read[state]["stats"]["topspender_share"]]
            add.append(row)

        csv.register_dialect('myDialect',
            quoting=csv.QUOTE_ALL,
            skipinitialspace=True)

        with open("fec/data/stats/{}-{}-stats.csv".format (office, year), "w+") as w:
            writer = csv.writer(w, dialect='myDialect')
            for row in add:
                writer.writerow(row)

        w.close()

#for num in [2016, 2014, 2012, 2010, 2008, 2006, 2004]:
#	tocsv("S", num)