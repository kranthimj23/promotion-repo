CREATE PROCEDURE TransferFunds(
    IN p_from_account INT,
    IN p_to_account INT,
    IN p_amount DECIMAL(15,2)
)
BEGIN
    UPDATE Accounts
    SET Balance = Balance - p_amount
    WHERE AccountID = p_from_account;

    UPDATE Accounts
    SET Balance = Balance + p_amount
    WHERE AccountID = p_to_account;

    INSERT INTO Transactions
    (TransactionID, AccountID, TransactionType, Amount, TransactionDate, Description)
    VALUES
    (FLOOR(RAND()*100000), p_from_account, 'Transfer Out', p_amount, CURRENT_TIMESTAMP, 'Fund Transfer'),
    (FLOOR(RAND()*100000), p_to_account, 'Transfer In', p_amount, CURRENT_TIMESTAMP, 'Fund Transfer');
END;