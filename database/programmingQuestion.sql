CREATE DEFINER=`admin`@`%` FUNCTION `programmingQuestion`(q VARCHAR(100), r TEXT) RETURNS int
BEGIN

	INSERT INTO CONVERSATION (CONVERSATION_QUESTION, CONVERSATION_QUESTION_TIME, CONVERSATION_RESPONSE)
	VALUES (q, CURRENT_TIMESTAMP, r);
    
RETURN LAST_INSERT_ID();
END