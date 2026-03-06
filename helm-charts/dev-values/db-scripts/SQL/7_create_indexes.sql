CREATE INDEX idx_customer_email ON Customers(Email);
CREATE INDEX idx_account_customer ON Accounts(CustomerID);
CREATE INDEX idx_transaction_account ON Transactions(AccountID);
CREATE INDEX idx_loan_customer ON Loans(CustomerID);
CREATE INDEX idx_card_customer ON Cards(CustomerID);