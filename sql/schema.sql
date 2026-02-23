DROP DATABASE IF EXISTS final_project;
CREATE DATABASE final_project;
SHOW DATABASES;
USE final_project;

DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS User_Favourite;
DROP TABLE IF EXISTS Beer;
DROP TABLE IF EXISTS Brewery;
DROP TABLE IF EXISTS FriendRequest;
DROP TABLE IF EXISTS User;



CREATE TABLE Brewery (
    Brewery_ID INT PRIMARY KEY,
    Brewery_Name VARCHAR(100) NOT NULL,
    Headquarters_address VARCHAR(255),
    NrOfBeer INT DEFAULT 0
);


CREATE TABLE Beer (
    Beer_ID INT PRIMARY KEY,
    Beer_Name VARCHAR(100) NOT NULL,
    Beer_Type VARCHAR(50),
    Official_Description TEXT,
    Ingredients TEXT,
    Brewery_ID INT,
    NrOfReviews INT DEFAULT 0,
    AverageRating FLOAT,
    FOREIGN KEY (Brewery_ID) REFERENCES Brewery(Brewery_ID)
);


CREATE TABLE User (
    UserID INT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    NrOfReviews INT DEFAULT 0
);

CREATE TABLE Review (
    ReviewID INT PRIMARY KEY,
    UserID INT,
    Beer_ID INT,
    Rating INT CHECK (Rating BETWEEN 1 AND 10),
    ReviewText TEXT,
    DateTime DATETIME,
    Picture_Address VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (Beer_ID) REFERENCES Beer(Beer_ID)
);

CREATE TABLE FriendRequest (
    SenderID INT,
    ReceiverID INT,
    DateTime DATETIME,
    Status INT,
    PRIMARY KEY (SenderID, ReceiverID),
    FOREIGN KEY (SenderID) REFERENCES User(UserID),
    FOREIGN KEY (ReceiverID) REFERENCES User(UserID)
);

CREATE TABLE User_Favourite (
    UserID INT,
    Beer_ID INT,
    PRIMARY KEY (UserID, Beer_ID),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (Beer_ID) REFERENCES Beer(Beer_ID)
);


DROP TRIGGER IF EXISTS UpdateRating;
DELIMITER $$
CREATE TRIGGER UpdateRating
AFTER
INSERT ON Review FOR EACH ROW
BEGIN
	UPDATE Beer
    SET 
        AverageRating = (SELECT AVG(Rating) FROM Review WHERE Beer_ID = NEW.Beer_ID),
        NrOfReviews = (SELECT COUNT(*) FROM Review WHERE Beer_ID = NEW.Beer_ID)
    WHERE Beer_ID = NEW.Beer_ID;
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS UpdateUserReviewNr;
DELIMITER $$
CREATE TRIGGER UpdateUserReviewNr
AFTER
INSERT ON Review FOR EACH ROW
BEGIN
	UPDATE User
    SET 
        NrOfReviews = (SELECT COUNT(*) FROM Review WHERE UserID = NEW.UserID)
    WHERE UserID = NEW.UserID;
END $$
DELIMITER ;

DROP TRIGGER IF EXISTS UpdateNrOfBeer;
DELIMITER $$
CREATE TRIGGER UpdateNrOfBeer
AFTER
INSERT ON Beer FOR EACH ROW
BEGIN
	UPDATE Brewery
    SET 
        NrOfBeer = (SELECT COUNT(*) FROM Beer WHERE Brewery_ID = NEW.Brewery_ID)
    WHERE Brewery_ID = NEW.Brewery_ID;
END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS NewFriendRequest;
DELIMITER $$
CREATE PROCEDURE NewFriendRequest (IN UserID_1 INT, IN UserID_2 INT, IN Datum DATETIME, OUT Result INT)
BEGIN
	DECLARE checking BOOL;
    
    SELECT EXISTS(
		SELECT 1
			FROM FriendRequest
            WHERE (SenderID = UserID_1 AND ReceiverID = UserID_2) OR (SenderID = UserID_2 AND ReceiverID = UserID_1))
	INTO checking;
    
    IF (UserID_1 = UserID_2) THEN
		SET Checking := true;
    END IF;
    
    IF (checking = true) THEN
		SET Result := -1;
    ELSE 
		INSERT INTO FriendRequest (SenderID, ReceiverID, DateTime, Status) VALUES
		(UserID_1, UserID_2, Datum, 1);
        SET Result := 0;
    END IF;
END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS FriendRequestAccept;
DELIMITER $$
CREATE PROCEDURE FriendRequestAccept (IN UserID_1 INT, IN UserID_2 INT, IN Datum DATETIME, OUT Result INT)
BEGIN
	DECLARE checking BOOL;
    
    SELECT EXISTS(
		SELECT 1
			FROM FriendRequest
            WHERE SenderID = UserID_1 AND ReceiverID = UserID_2 AND Status = 1)
            INTO checking;
	IF (checking = 0) THEN
		SET Result := -1;
	ELSE 
		UPDATE FriendRequest
        SET Status = 2, DateTime = Datum
        WHERE SenderID = UserID_1 AND ReceiverID = UserID_2;
        SET Result := 0;
	END IF;
END $$
DELIMITER ;

DROP PROCEDURE IF EXISTS FriendRequestReject;
DELIMITER $$
CREATE PROCEDURE FriendRequestReject (IN UserID_1 INT, IN UserID_2 INT, IN Datum DATETIME, OUT Result INT)
BEGIN
	DECLARE checking BOOL;
    
    SELECT EXISTS(
		SELECT 1
			FROM FriendRequest
            WHERE SenderID = UserID_1 AND ReceiverID = UserID_2 AND Status = 1)
            INTO checking;
	IF (checking = 0) THEN
		SET Result := -1;
	ELSE 
		DELETE FROM FriendRequest
		WHERE SenderID = UserID_1 AND ReceiverID = UserID_2;
        SET Result := 0;
	END IF;
END $$
DELIMITER ;