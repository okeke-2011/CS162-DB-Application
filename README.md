# Implementation Details
### Recap of Project specifications
- We have offices around the world.
- Each agent is assigned to one or more offices
- Each house that is listed is assigned to an office, a seller and an agent.
- Sellers can sell several houses.
- A sale requires a buyer and a sale date (should be after the listing date). When a sale is made, the house is marked as sold

### Commands to run my submission
First ensure you are in the right directory (CS162-DB-Application)

```
python3.6 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements.txt

python3 clean_up.py // only if you are re_run the assignment

python3 create.py // Sufficient as the first command for your first run
python3 insert_data.py
python3 get_all_tables.py // Just to see what's in the DB
python3 query_data.py
python3 clean_up.py
```

### File explanations:
- create.py: Establishes database connection and specifies the database schema
- insert_data.py: inserts example data
- get_all_tables.py: Shows all the data in the database
- query_data.py: runs queries required by the assignment 
- clean_up.py: closes the session and deletes all data in the tables
- requirements.txt: contains all library requirements to run this project
- test_queries.py: Tests the functionality of my code

### My Tables:
- Offices: Stores the different offices we have
- Agents: Stores name and contact info of our agents
- AgentOffice: Defines the many-to-many relationship between agents and offices in line with normalization principles
- Seller: Stores name and contact info of sellers
- Buyers: Stores name and contact info of buyers
- Houses: Stores house info including the agent, office, and seller associated with the house
- Sales: Stores all required information about houses that have been sold 

For further insight into the database schema examine the create.py file.

### Data normalization, Indices and Transactions 

**Data Normalization**
- **1NF**:
    - each column has only one value assigned to it per row entry
    - all values in a column are of the same type
    - all columns have unique names
- **2NF**:
    - 1NF
    - no partial dependency: columns are only dependent on the primary key, and nothing else
- **3NF**:
    - 2NF
    - no transitive dependency

It is worth noting that I didn't normalize these tables after the fact. 
I kept the normalization principles in mind while I created the tables.

Inspect the create.py file to get a better sense of how I applied normalization 
in my database schema.



**Indices**
- In SQLAlchemy, indexing is just a matter of setting the index argument to True in the appropriate Column definition 
- Every primary key (in most popular databases) are automatically indexed, so I didn't add this argument to those columns
- Any joins occurring in this implementation are based on foreign key constraints. Hence, I indexed the foreign key fields as well
- I also index fields that were required by the queries in this assignment (to make data retrieval faster).
- To my understanding, no other indices would improve performance of the queries.

To get a better sense of how I used indexes examine the create.py file


**Transactions**
- I made use of transactions when carrying out bundled operation (like selling a house) which leads to multiple changes to the database. 
- For a transaction, all these changes need to go. If not, then it's better if no change goes.
- To implement this, I used SQLAlchemy's session. 
  - Tasks are added to the transaction using `session.add()` and executed using `session.commit()`. If the transaction runs into an error, it rolls back to the previous state before the transaction was executed.