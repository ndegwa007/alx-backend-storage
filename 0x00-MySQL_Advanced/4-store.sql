-- script creates a trigger
-- trigger decreases the quantity of an item
-- after adding a new order
DELIMITER //
CREATE TRIGGER update_quantity_items
AFTER INSERT ON orders FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - NEW.number
	WHERE name = New.item_name;
END;
//
DELIMITER ;
