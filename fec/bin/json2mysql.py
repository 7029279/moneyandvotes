import mysql.connector
import json
import csv

def dbtry():
	mydb = mysql.connector.connect( 
		host="localhost",
		user="root",
		passwd="root"
		  )
	cur = mydb.cursor()
	cur.execute ("CREATE DATABASE test2") 
	mydb.close()


def add_candidates_S(office, year):
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
	cur.execute ("ALTER TABLE {}{} ADD COLUMN primary_votes INT".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN primary_share FLOAT".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN general_votes INT".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN general_share FLOAT".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN office VARCHAR(255)".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN general_win VARCHAR(255)".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN primary_win VARCHAR(255)".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN unopposed VARCHAR(255)".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN nodata VARCHAR(255)".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN spending_share FLOAT".format(office,year))
	cur.execute ("ALTER TABLE {}{} ADD COLUMN performance FLOAT".format(office,year))


# sqlid state party fecid ranas name
# expenditure primary_votes, primary_share 
# general_votes general _share office primary_win general_win

	with open ("fec/data/{}/{}-{}-datasets-2.json".format (year, office, year), "r") as f:
		read = json.load(f)

		for state in read:
			print (state)
			for individual in read[state]["results"]:
				if individual["primary_votes"] == "Unopposed":
					unopposed = "Unopposed"
				else: 
					unopposed = "No"

				if individual["operating_expenditure"] == "No Data":
					nodata = "Data unavailable"
				else:
					nodata = "Data available"
					
				if individual["operating_expenditure"] == 0 and individual["primary_votes"] == 0:
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
				sql1 = "INSERT INTO {}{} (fecid, state, party, name, ranas, expenditure, primary_votes, primary_share, general_votes, general_share, office, primary_win, general_win, unopposed, nodata, spending_share, performance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s)".format (office, year)
				val1 = (individual["candidate_id"], individual["state"], individual["party_full"], 
				individual["name"], individual["incumbent_challenge_full"], 
				individual["operating_expenditure"], individual["primary_votes"], individual["primary_share"],
				individual["general_votes"], individual["general_share"], individual["office_full"],
				individual["primary_win"], individual["general_win"], unopposed, nodata, individual["spending_share"], individual["performance"])

				cur.execute(sql1, val1)

	cur.execute ("COMMIT")

	cur.close()
	mydb.close() # dont forget to close connections


def add_candidates_H (office, year):
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


def drop (office, year): 
	mydb = mysql.connector.connect( 
		host="localhost",
		user="root",
		passwd="root",
		database='moneyandvotes'
	)
	cur = mydb.cursor()
	cur.execute ("set @@sql_mode = ''")
	if type(year) == int:
		cur.execute ("DROP TABLE `moneyandvotes`.`{}{}`".format(office,year))
	elif year == "stats":
		cur.execute ("DROP TABLE `moneyandvotes`.`{}`".format("stats"))
	elif year == "all":
		cur.execute ("DROP TABLE `moneyandvotes`.`{}{}`".format(office,2016))
		cur.execute ("DROP TABLE `moneyandvotes`.`{}{}`".format(office,2014))
		cur.execute ("DROP TABLE `moneyandvotes`.`{}{}`".format(office,2012))
		cur.execute ("DROP TABLE `moneyandvotes`.`{}{}`".format(office,2010))
		cur.execute ("DROP TABLE `moneyandvotes`.`{}{}`".format(office,2008))
		cur.execute ("DROP TABLE `moneyandvotes`.`{}{}`".format(office,2006))
		cur.execute ("DROP TABLE `moneyandvotes`.`{}{}`".format(office,2004))
		cur.execute ("DROP TABLE `moneyandvotes`.`{}`".format("stats"))

#drop("all")
#for num in [2016, 2014, 2012, 2010, 2008, 2006, 2004 ]: 
#	add_candidates_S ("S", num)


#for race in [2016, 2014, 2012, 2010, 2008, 2006, 2004]:
#	try:
#		drop ("H", race)
#	except:
#		pass
#		add_candidates_H("H", race)

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
		cur.execute ("ALTER TABLE stats ADD COLUMN office VARCHAR(255)")
		cur.execute ("ALTER TABLE stats ADD COLUMN district VARCHAR(255)")

		cur.execute ("ALTER TABLE stats ADD COLUMN average_spending FLOAT")
		cur.execute ("ALTER TABLE stats ADD COLUMN topspender_share FLOAT")
		cur.execute ("ALTER TABLE stats ADD COLUMN correlation_coef FLOAT")
		cur.execute ("ALTER TABLE stats ADD COLUMN correlation_sample VARCHAR(255)")

	except mysql.connector.errors.ProgrammingError:
		pass

	with open ("fec/data/{}/{}-{}-datasets-2.json".format (year, office, year), "r") as f:
		read = json.load(f)
		if office == "S":
			district = "SEN"  
			for state in read:
				sql1 = "INSERT INTO stats (oysd, state, year, office, district, average_spending, topspender_share, correlation_coef, correlation_sample) VALUES ( %s, %s,  %s, %s, %s, %s, %s, %s, %s)"
				val1 = ("{}{}{}{}".format(office, year, state, district), state, year, 
				office, district, read[state]["stats"]["average_spending"],
				read[state]["stats"]["topspender_share"], read[state]["stats"]["correlation_coef"], 
				read[state]["stats"]["correlation_sample"])
				cur.execute(sql1, val1)
			cur.execute ("COMMIT")

		elif office == "H":
			for state in read:
				for district in read[state]["stats"]:
					if district == "ALL":
						continue
					else:
						sql1 = "INSERT INTO stats (oysd, state, year, office, district, average_spending, topspender_share) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
						val1 = ("{}{}{}".format(office, year, district), state, year, 
						office, district, read[state]["stats"][district]["average_spending"],
						read[state]["stats"][district]["topspender_share"])
						cur.execute(sql1, val1)
					# for individual districts
					
				sql1 = "INSERT INTO stats (oysd, state, year, office, district, average_spending, topspender_share, correlation_coef, correlation_sample) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				val1 = ("{}{}{}{}".format(office, year, state, 0), state, year, 
				office, district, read[state]["stats"]["ALL"]["average_spending"],
				read[state]["stats"]["ALL"]["topspender_share"], read[state]["stats"]["ALL"]["correlation_coef"], 
				str(read[state]["stats"]["ALL"]["correlation_sample"]))
				# for "ALL" statewide stats
				cur.execute(sql1, val1)
				#try:
				#	cur.execute(sql1, val1)
				#except:
				#	print (cur.statement)
			cur.execute ("COMMIT")

	
		if office == "B":
			district = "BOTH" 
			for state in read:
				print (state)
				sql1 = "INSERT INTO stats (oysd, state, year, office, district, average_spending, topspender_share, correlation_coef, correlation_sample) VALUES ( %s, %s,  %s, %s, %s, %s, %s, %s, %s)"
				val1 = ("{}{}{}{}".format(office, year, state, district), state, year, 
				office, district, read[state]["stats"]["average_spending"],
				read[state]["stats"]["topspender_share"], read[state]["stats"]["correlation_coef"], 
				read[state]["stats"]["correlation_sample"])
				cur.execute(sql1, val1)
			cur.execute ("COMMIT")

	cur.close()
	mydb.close() # dont forget to close connections
#drop("stats", "stats")
#add_stats("H", 2016)

#for office in ["S", "H", "B"]:
#	for race in [2016, 2014, 2012, 2010, 2008, 2006, 2004]:
#		print (race, office)
#		add_stats(office, race)



def tocsv (office, year):  ## add csv files
	with open ("fec/data/{}/{}-{}-datasets-2.json".format (year, office, year), "r") as r:
		read = json.load(r)
		
		add = [["state","average_spending","topspender_share", "correlation_coef"]]
		for state in read:
			if read[state]["stats"]["correlation_coef"] < 0.5:
				read[state]["stats"]["correlation_coef"] = 0.5
			if read[state]["stats"]["topspender_share"] < 0.5:
				read[state]["stats"]["topspender_share"] = 0.5
			if read[state]["stats"]["average_spending"] > 4000000:
				read[state]["stats"]["average_spending"] = 4000000

			row = [state, read[state]["stats"]["average_spending"], read[state]["stats"]["topspender_share"], 
			read[state]["stats"]["correlation_coef"]]
			add.append(row)

		csv.register_dialect('myDialect',
			quoting=csv.QUOTE_ALL,
			skipinitialspace=True)

		with open("fec/data/stats/{}-{}-stats.csv".format (office, year), "w+") as w:
			writer = csv.writer(w, dialect='myDialect')
			for row in add:
				writer.writerow(row)

		w.close()

for num in [2016, 2014, 2012, 2010, 2008, 2006, 2004]:
    tocsv("B", num)