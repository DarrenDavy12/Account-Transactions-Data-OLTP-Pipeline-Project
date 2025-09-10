-- OLTP Schema: normalized transactional model

-- Schema: Simple payments system





-- customers table


CREATE TABLE IF NOT EXISTS customers (
  customer_id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);


-- accounts table

CREATE TABLE IF NOT EXISTS accounts (
  account_id SERIAL PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
  account_type TEXT NOT NULL,
  balance NUMERIC(14,2) DEFAULT 0.00,
  currency CHAR(3) DEFAULT 'USD',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE(customer_id, account_type)
);


-- transactions table

CREATE TABLE IF NOT EXISTS transactions (
  transaction_id BIGSERIAL PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES accounts(account_id),
  amount NUMERIC(14,2) NOT NULL,
  currency CHAR(3) NOT NULL,
  type TEXT NOT NULL, -- 'debit' or 'credit'
  status TEXT NOT NULL DEFAULT 'pending', -- pending/posted/failed
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);



-- indexing certain fields 


-- create index for customer_id field
CREATE INDEX IF NOT EXISTS idx_accounts_customer ON accounts(customer_id);


-- create index for account_id field
CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account_id);


-- create index for created_at field 
CREATE INDEX IF NOT EXISTS idx_transactions_created ON transactions(created_at); 



