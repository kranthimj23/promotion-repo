CREATE VIEW CustomerAccountSummary AS
SELECT c.CustomerID, c.FirstName, c.LastName,
       a.AccountID, a.AccountType, a.Balance
FROM Customers c
JOIN Accounts a ON c.CustomerID = a.CustomerID;

CREATE VIEW ActiveLoans AS
SELECT l.LoanID, c.FirstName, c.LastName,
       l.LoanAmount, l.InterestRate, l.Status
FROM Loans l
JOIN Customers c ON l.CustomerID = c.CustomerID
WHERE l.Status = 'Approved';