# Account Transactions Data OLTP Pipeline Project 🚀

This project demonstrates the design and implementation of a simple **OLTP (Online Transaction Processing) pipeline** 

- **Docker** to host postgres in container 
- **Postgres/PSQL** (Dockerized) as the transactional database
- **SQL** for schema creation
- **Python** to insert sample and synthetic data
- **Dbeaver** to showcase tables in database format and prepared for querying
- **Azure Blob Storage** for backing up raw data
- **Git** for version control and project collaboration

It’s a hands-on, end-to-end mini-project to practice skills required in real-world data engineering.

---

## 📂 Project Structure

```text
oltp-pipeline-demo/
├── docker-compose.yml        # Spins up Postgres
├── sql/
│   └── oltp_schema.sql       # Schema for customers, accounts, transactions
├── app/
│   ├── oltp_client.py        # Insert sample customers, accounts, transactions
│   ├── generate_data.py      # Synthetic data generator
│   └── backup_to_azure.py    # Export data to Azure Blob
├── .gitignore                # Ignore venv, keys, etc.
├── requirements.txt          # Python dependencies
└── README.md                 # Project description, setup steps
```

## 🏗️ Architecture

Docker + Postgres → Run a local OLTP database in a container.

Schema creation → Customers, Accounts, Transactions.

Python client → Insert initial data and perform transactions.

Synthetic data → Generate test transactions for scale.

Backup → Export raw tables into Azure Blob Storage.


## ⚙️ Setup Instructions

1. Clone the repository
```
git clone https://github.com/<your-username>/Account-Transactions-Data-OLTP-Pipeline-Project.git
cd Account-Transactions-Data-OLTP-Pipeline-Project
```

2. Start Postgres with Docker
```
docker-compose up -d
```


3. Check if container is running:
```
docker ps
```

4. Apply schema
```
docker cp sql/oltp_schema.sql oltp_pg:/tmp/
docker exec -u postgres oltp_pg psql -d oltp_db -f /tmp/oltp_schema.sql
```

## 🧑‍💻 Running the Clients

5. Insert initial customers/accounts
```
python3 app/oltp_client.py
```



6. Generate synthetic data
```
python3 app/generate_data.py
```

This will create multiple customers, accounts, and random transactions.





## 🧑‍💻 Connected dockerized postgres to dbeaver and ran queries. 


Used Inner Join to match values in both tables 'customers' and 'accounts' using both customer_id and account_id 
Shows customers, accounts, and balances 





Used case statement to show total credits/debits per account and transaction count






Used case statement and aggregate function SUM, to show daily profit/loss (net flow) by summing credits and debits per day. 





## ☁️ Backup to Azure Blob

Export data with Python:
```
python3 app/backup_to_azure.py
```

Make sure you have set environment variables for:
```
export AZURE_STORAGE_ACCOUNT_NAME=<your-storage-account>
export AZURE_STORAGE_ACCOUNT_KEY=<your-access-key>
```

The script will upload CSVs to your Azure Blob container (raw/transactions.csv, etc).

🧹 .gitignore

Make sure secrets and venv don’t get committed:

venv/
__pycache__/
*.pyc
.env
*.log
*.key


