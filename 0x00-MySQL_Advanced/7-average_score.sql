-- scripts computes an average score of a student
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	DECLARE average DECIMAL(5, 2);
	SELECT AVG(score) INTO average FROM corrections AS U WHERE U.user_id = user_id;
	UPDATE users SET average_score = average WHERE id = user_id;
END;
$$

DELIMITER ;
