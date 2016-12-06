Extract Association Rules
COMS E6111 Advanced Database Systems

a) Group Information

Project 3 Group 17
Team Members:
Yuhao Zhang (yz3044), Kan Zhu (kz2250)

b) File List

main.py (entry of our program)
apriori.py (the python script of the implementation of the a-priori algorithm)
processCSV.py (the python script to process the original dataset)
INTEGRATED-DATASET.csv (processed dataset)
NYC_Jobs.csv (original dataset)
example-run.txt (interesting results of our program)
README.txt 

c) Description of dataset
(a) 
We use "NYC_Jobs.csv" dataset to generate the INTEGRATED-DATASET file
url: https://data.cityofnewyork.us/City-Government/NYC-Jobs/kpav-sd4t

(b)
Enter the "group17-proj3" directory. Type: python processCSV.py NYC_Jobs.csv.
The python script "processCSV.py" would transform the original data "NYC_Jobs.csv" to the “INTEGRATED-DATASET.csv” file.

The process contains two procedures:
1. remove useless attributes
Some attributes are too specific for each jobs, like "Job ID", "Work Location". Some are mostly empty, like "Post Unitl", "Recruitment Contact". Some are not very useful for our rule extraction, like "Posting Updates", "Process Date". So we remove these attributes and retain only attributes of ['Agency', 'Posting Type', 'Business Title', 'Civil Service Title', 'Level', 'Salary Range From', 'Division/Work Unit']
For the 'Posting Type' attribute, ‘Internal' means postings available to city employees while 'External' means postings available to the general public are included.

2. format data
Type of data such as numbers have to be formatted for the a-priori algorithm. So for the "Salary Range From" attribute, we set all the number below 50000 as string "Below 50k", and all the number above 50000 as string "Above 50k". i.e. 60000 -> "Above 50k", 40000 -> "Below 50K"

(c)
Our dataset contains current job postings available on the City of New York’s official jobs site. It provides diverse and comprehensive information for the job market of New York City. From the dataset, we can see what kind of jobs are mostly needed in New York City, what the salary range is for each job and what kind of level required for each job. By extracting rules from our dataset, we can have a better understanding of the job market of New York City.

d) Run the Program

Enter the "group17-proj3" directory. Then type: python main.py <INTEGRATED-DATASET.csv> <minSupp> <minConf>

where:
<INTEGRATED-DATASET.csv> is the filename of our INTEGRATED-DATASET
<minSupp> is the threshold of support(between 0 and 1)
<minConf> is the threshold of confidence(between 0 and 1)

e) Internal Design

The program is consist of three source files: main.py, apriori.py, processCSV.py

--main.py--
It is the entry of the program. It receives the arguments from the terminal and start to extract rules from our INTEGRATED-DATASET.csv file.

--apriori.py--
It constains all the methods of the a-priori algorithm

extractRules(): extract frequent itemsets and association rules from the list of transactions and items by a-priori algorithm

apriori(): implementation of the a-priori algorithm in the section 2.1 of the paper
Our a-priori algorithm contains the following steps:
1. Generate large 1-itemsets L_1
2. While L_k is not empty, generate the next candidate C_k by the aprioriGen() method. 
3. Remove the candidate in Ck whose support is below the minSupp
4. Store all the L_k into an itemsets

aprioriGen(): this function is to generate the next candidate itemsets
Our aprioriGen method is the same with the one in the paper. It contains the following two steps:
1. Join the L_k with L_k, like 
	insert into C_k
	select p.item_1, p.item_2, ... , p.item_{k-1}, q.item_{k-1}
	from L_{k-1} p, L_{k-1} q
	where p.item_1 = q.item_1, ..., p.item_{k-2} = q.item_{k-2},
		p.item_{k-1} < q.item_{k-1}
2. remove candidates from C_k whose subsets are not in L_{k-1} by the isSubset() method.

isSubset(): this function is to judge whether a candidate is a subset in L_{k-1}

writeFile(): this function is to output the frequent itemsets and association rules to a file

--processCSV.py--
It contains all the methods to process the original dataset into our INTEGRATED-DATASET.csv file.

transformCSV(): transform the csv file into our integrated dataset.

formatDate(): retain only the information of year for the data type of datetime

formateSalary(): For salary attribute, divide it into two categories, i.e. above 50k or below 50k

removeAttr(): remove the specific attribute from the dataset

Program Flow:
The program starts from the main() method in the main.py. The main() then calls the extractRules(). In the extractRules() function, it call apriori() function to get two variables, the first is a dictionary containing all the L_k and the second is a dictionary including each itemset with its count number. 

After the call of apriori(), it gets frequent itemsets by calculating the support of each itemset and selecting these with support above the minSupp. To extract rules, it first chooses one item from the itemset as the right hand side of the rule and the rest as the left hand side. Then calculate the confidence of the rule and store these whose confidence is above the minConf.

Finally, the program call writeFile() method to output the result into the "output.txt" file.

f) Interesting results

By using the following command line:
python main.py INTEGRATED-DATASET.csv 0.03 0.7
You can get a lot of interesting results. Here we only list some of the interesting observations of our results.

1. starting salary
['Above 50K'] , 64.00% vs ['Below 50K'] , 36.00%
These two frequent itemsets show that the starting salary in New York City is mainly above 50k

2. level of job requirement 
['00'] , 32.21% vs ['01'] , 20.01% vs ['02'] , 18.77% vs ['03'] , 8.50% vs ['M1'] , 7.51% vs ['M2'] , 4.31%
These frequent itemsets show that most of the jobs in New York City are hiring entry level employee(around 1/3). And the number of positions decreases when the required level is higher.

3. interesting rules
['COMMUNITY COORDINATOR'] => ['00'] (Conf: 100.00% Supp: 5.45%)
It shows that most of the position of 'COMMUNITY COORDINATOR' are entry level.

['COMPUTER SPECIALIST (SOFTWARE)'] => ['Above 50K'] (Conf: 100.00% Supp: 3.84%)
['COMPUTER SYSTEMS MANAGER'] => ['Above 50K'] (Conf: 97.79% Supp: 3.30%)
['CITY RESEARCH SCIENTIST'] => ['Above 50K'] (Conf: 97.15% Supp: 6.77%)
["ADMIN FOR CHILDREN'S SVCS"] => ['Above 50K'] (Conf: 90.91% Supp: 3.22%)
It shows that most of the jobs within the above four category have starting salaries above 50k.

['M2'] => ['Above 50K'] (Conf: 100.00% Supp: 4.31%)
['M1'] => ['Above 50K'] (Conf: 98.35% Supp: 7.39%)
This shows that most of the manager-2 or manager-1 level positions offer starting salaries above 50k.

['CITY RESEARCH SCIENTIST'] => ['DEPT OF HEALTH/MENTAL HYGIENE'] (Conf: 81.14% Supp: 5.65%)
It shows that most of the 'CITY RESEARCH SCIENTIST' positions are hired by the 'DEPT OF HEALTH/MENTAL HYGIENE'.

By above information, we can better understand the current job market and prepare ourselves for a better job.
