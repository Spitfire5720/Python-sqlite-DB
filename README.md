README.md

This program is using Python 3.12 and SQLite3 on VSCode.
Run "Rocketdb.py", as the code runs it will create a database file, a table, and then populate it with the seeded data. 
To properly make use of the HTTP endpoints a JSON file must be provided in the request body(POST) or as query parameters (GET).

Python and FastAPI were used as a requirement of the assesment.
I used VSCode, because it seemed like the most powerful IDE to use. 
The built in terminal in VSCode was useful in troubleshooting imports and extensions, etc. 
I used SQLite3, because it feels easier to install and lightweight in use. 
I used Postman as a reliable tester of API connections. 

Node structure is created recursively and then inserted into the database. 

BRIEF DESCRIPTION OF KEY CHALLENGES:
1. Setting up SQLite3 took longer than expected, and instructions were slightly vague but accomplishable. 
2. Understanding the hierarchy, from the limited instructions, was slighly vague but accomplishable. 
3. Database set up required consistency between variables and methods. Major refactoring at certain points was required.  
4. VSCode extensions provided minor glitches and acted inconsistently, requiring individual troubleshooting. 
5. Contemplated switching IDE to PyCharm, but valued speed in executing the task. 
6. Referenced several resources (ie. StackOverflow, texts, and other projects) to get the imports, and extensions working properly. 
7. Getting the HTTP endpoints to operate and communicate as required with Postman. 
8. Postman required more FastAPI related troubleshooting, still shows 404 error.

Additional security protocols would have to be considered in the real world applications of this code. I look forward to understanding the team's approach to safety considerations in protecting all vulnerable parts of the infrastructure. 

The vulnerabilities I can see are: SQL injection, no input validations, debug mode enabled, authentication and authorization needs, data exposure, error disclosure, a lack of HTTPs, and potential path traversal.

A best effort was considered when approaching the question and solution that would be effective in daily practice, if I were selected to join the RocketLab team. 

In a production environment, I understand developer environments are more uniform. 
I would also be given access to critical teammember knowledge, proprietary tools and wikis, and additional resources to find solutions faster and more effficiently. 

In my current role, we have a peer review process for code. 
This code is then approved after extensive managerial testing. 
Further supporting, that no engineer should work alone for the best results. 

I look forward to more and efficient ways to learn and work with a new team to find solutions to these problems. 