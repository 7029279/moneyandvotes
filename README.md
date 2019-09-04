# moneyandvotes
I wrote scripts in python to collect data from FEC API and analyze them statistically. 

In data, there are several json files and csv files:

2016 - 2004 contains data for the year's individual races. 

X = S >>> Senate, H >>> House, or B >>> Both house and senate.

X-YEAR-datasets-financial.json >>> fianancial data without votes information, data straight from OpenFEC API
X-YEAR-datasets-2.json >>> financial dat and votes information. It also has a bunch of statistics are added. Probably most usable.

B-YEAR-datasets-2.json contains stats of each state and NA (nationwide)

In B-YEAR-datasets-2.json: 
"correlation_coef" >>> correlation coefficient between the funding (the campaign's spending / total spending by all candidates) and electoral performance (the candidate's vote / entire votes cast in the race)

"average_spending" >>> total spending by all candidates / number of candidates

"topspender_share" >>> the 

In bin, there are scripts that I used to collect and analyze these data:

hosuelister.py >>> collect and analyze data for HOUSE races.
candidate-lister.py >>> collect and analyze data for SENATE races.
bothlister >>> reads datasets-2 files and calculate statistics for Senate and House combined.

json2sql >>> reads json files and throw them into sql relational database. I used mysql.

housdistrict.py >>> inside each state, creates lists of districts according to how many districts there are in that state 


Data used in this project are collected from FEC under the condition of Non-Commercial use.

Visit votesandmoney.com

![clicakble-map](https://user-images.githubusercontent.com/28686892/64263100-baa18380-cef4-11e9-9e6e-7940fdbb0abc.png)
![statistics-page](https://user-images.githubusercontent.com/28686892/64263103-bc6b4700-cef4-11e9-92da-05d288c19098.png)


(Update 4/Sep/2019)
The website is temporarily taken down because the GCP sql database was costing too much everyday.




