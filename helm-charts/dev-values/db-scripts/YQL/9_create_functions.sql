CREATE FUNCTION GetCustomerTotalBalance(p_customer_id INT)
RETURNS DECIMAL(15,2)
READS SQL DATA
BEGIN
    DECLARE total_balance DECIMAL(15,2);

    SELECT SUM(Balance)
    INTO total_balance
    FROM Accounts
    WHERE CustomerID = p_customer_id;

    RETURN COALESCE(total_balance, 0);
END;