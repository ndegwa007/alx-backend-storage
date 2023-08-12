-- script creates trigger to check email changes
DELIMITER //
CREATE TRIGGER check_email_update
BEFORE UPDATE ON users FOR EACH ROW
BEGIN
	IF OLD.email != NEW.email THEN
		SET NEW.valid_email = 0;
	END IF;
END;
//
DELIMITER ;
