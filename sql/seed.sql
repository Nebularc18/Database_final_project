INSERT INTO Brewery (Brewery_ID, Brewery_Name, Headquarters_address, NrOfBeer) VALUES
    (1, 'Omnipollo', 'Kyrkogatan 7, Stockholm', 0),
    (2, 'Stigbergets Bryggeri', 'Slottsskogsgatan 37, Göteborg', 0),
    (3, 'Guinness Storehouse', 'St. James Gate, Dublin', 0),
    (4, 'BrewDog', 'Balmacassie Commercial Park, Ellon', 0);

INSERT INTO Beer (Beer_ID, Beer_Name, Beer_Type, Official_Description, Ingredients, Brewery_ID, NrOfReviews, AverageRating) VALUES
    (101, 'Nebuchadnezzar', 'IIPA', 'A homebrew recipe that went big.', 'Hops, Malt, Yeast, Water', 1, 0, NULL),
    (102, 'West Coast IPA', 'IPA', 'A classic Gothenburg IPA.', 'Barley, Citra Hops', 2, 0, NULL),
    (103, 'Draught Stout', 'Stout', 'Creamy and smooth legendary stout.', 'Roasted Barley, Nitrogen', 3, 0, NULL),
    (104, 'Punk IPA', 'IPA', 'The beer that started it all.', 'Maris Otter Pale Malt, Chinook Hops', 4, 0, NULL),
    (105, 'Zodiac', 'IPA', 'House IPA with a blend of grains.', 'Simcoe, Citra, Centennial Hops', 4, 0, NULL);

INSERT INTO User (UserID, Username, Email, NrOfReviews) VALUES
    (1, 'BeerLover99', 'bob@example.com',0),
    (2, 'Alice_IPA', 'alice@test.se',0),
    (3, 'Stout_King', 'king@stout.com',0),
    (4, 'Charlie_Hop', 'charlie@craft.com',0);

INSERT INTO Review (ReviewID, UserID, Beer_ID, Rating, ReviewText, DateTime, Picture_Address) VALUES
    (1, 1, 101, 9, 'Fantastisk dubbel IPA!', '2023-10-01 18:30:00', 'images/rev1.jpg'),
    (2, 2, 101, 8, 'Lite för besk för min smak men god.', '2023-10-02 20:15:00', 'images/rev2.jpg'),
    (3, 3, 103, 10, 'Perfektion på burk.', '2023-10-05 12:00:00', NULL),
    (4, 1, 104, 7, 'Solid klassiker.', '2023-10-10 19:00:00', 'images/rev4.jpg'),
    (5, 4, 102, 9, 'Grym juice från Göteborg!', '2023-10-12 21:45:00', NULL),
    (6, 3, 101, 10, 'Perfektion på burk.', '2023-10-05 12:00:00', NULL);

INSERT INTO FriendRequest (SenderID, ReceiverID, DateTime, Status) VALUES
    (1, 2, '2023-09-01 10:00:00', 2),
    (1, 3, '2023-09-05 11:30:00', 2),
    (2, 4, '2023-09-10 15:00:00', 1);

INSERT INTO User_Favourite (UserID, Beer_ID) VALUES
    (1, 101),
    (1, 103),
    (2, 101),
    (3, 103),
    (4, 102),
    (4, 105);