# moneyandvotes
scripts to collect data from FEC and data collected from FEC

In data, there are several json files:

S >>> Senate, H >>> House, B >>> Both

X-XXXX-datasets-financial.json >>> without votes information, data straight from OpenFEC API
X-XXXX-datasets-2.json >>> with votes information from excel spread sheets and also bunch of statistics are added. Probably most usable.


In bin, there are scripts that I used to collect and analyze these data:

hosuelister.py >>> collect and analyze data for HOUSE races.
candidate-lister.py >>> collect and analyze data for SENATE races.
bothlister >>> reads datasets-2 files and calculate statistics for Senate and House combined.

json2sql >>> reads json files and throw them into sql relational database. I used mysql.

housdistrict.py >>> inside each state, creates lists of districts according to how many districts there are in that state 


Data used in this project are collected from FEC under the condition of Non-Commercial use.










