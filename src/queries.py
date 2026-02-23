from db import get_connection
from datetime import datetime

def get_all_breweries():
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Brewery ORDER BY Brewery_Name")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_brewery_by_id(brewery_id: int):
    connection = get_connection()
    if not connection:
        return None
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Brewery WHERE Brewery_ID = %s", (brewery_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def create_brewery(brewery_id: int, name: str, address: str = None):
    connection = get_connection()
    if not connection:
        return None
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Brewery (Brewery_ID, Brewery_Name, Headquarters_address) VALUES (%s, %s, %s)",
        (brewery_id, name, address)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return brewery_id

def get_all_beers():
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT BE.*, BR.Brewery_Name 
        FROM Beer BE 
        LEFT JOIN Brewery BR ON BE.Brewery_ID = BR.Brewery_ID 
        ORDER BY BE.Beer_Name
    """)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_beer_by_id(beer_id: int):
    connection = get_connection()
    if not connection:
        return None
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT BE.*, BR.Brewery_Name 
        FROM Beer BE 
        LEFT JOIN Brewery BR ON BE.Brewery_ID = BR.Brewery_ID 
        WHERE BE.Beer_ID = %s
    """, (beer_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def create_beer(beer_id: int, name: str, beer_type: str, brewery_id: int, 
                description: str = None, ingredients: str = None):
    connection = get_connection()
    if not connection:
        return None
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO Beer (Beer_ID, Beer_Name, Beer_Type, Official_Description, Ingredients, Brewery_ID) 
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (beer_id, name, beer_type, description, ingredients, brewery_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return beer_id

def get_all_users():
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User ORDER BY Username")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_user_by_id(user_id: int):
    connection = get_connection()
    if not connection:
        return None
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def create_user(user_id: int, username: str, email: str):
    connection = get_connection()
    if not connection:
        return None
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO User (UserID, Username, Email) VALUES (%s, %s, %s)",
        (user_id, username, email)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return user_id

def get_reviews_for_beer(beer_id: int):
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT RE.*, US.Username 
        FROM Review RE 
        LEFT JOIN User US ON RE.UserID = US.UserID 
        WHERE RE.Beer_ID = %s 
        ORDER BY RE.DateTime DESC
    """, (beer_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_reviews_by_user(user_id: int):
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT RE.*, BE.Beer_Name 
        FROM Review RE 
        LEFT JOIN Beer BE ON RE.Beer_ID = BE.Beer_ID 
        WHERE RE.UserID = %s 
        ORDER BY RE.DateTime DESC
    """, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def create_review(review_id: int, user_id: int, beer_id: int, rating: int, 
                  review_text: str = None, picture_address: str = None):
    connection = get_connection()
    if not connection:
        return None
    cursor = connection.cursor()
    cursor.execute(
        """INSERT INTO Review (ReviewID, UserID, Beer_ID, Rating, ReviewText, DateTime, Picture_Address) 
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (review_id, user_id, beer_id, rating, review_text, datetime.now(), picture_address)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return review_id

def get_top_rated_beers(limit: int = 5):
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT BE.Beer_Name, BE.AverageRating, BE.NrOfReviews, BR.Brewery_Name
        FROM Beer BE
        LEFT JOIN Brewery BR ON BE.Brewery_ID = BR.Brewery_ID
        WHERE BE.NrOfReviews > 0
        ORDER BY BE.AverageRating DESC
        LIMIT %s
    """, (limit,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_friends_reviews(user_id: int):
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT BE.Beer_Name, US.Username AS Friend, RE.Rating, 
               RE.ReviewText, RE.Picture_Address, RE.DateTime
        FROM FriendRequest FR
        LEFT JOIN User US ON (SenderID = US.UserID OR ReceiverID = US.UserID) 
        LEFT JOIN Review RE ON US.UserID = RE.UserID
        LEFT JOIN Beer BE ON BE.Beer_ID = RE.Beer_ID
        WHERE FR.Status = 2 AND US.UserID != %s AND (FR.SenderID = %s OR FR.ReceiverID = %s)
        ORDER BY RE.DateTime DESC
    """, (user_id, user_id, user_id))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_friends(user_id: int):
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT US.UserID, US.Username, US.Email
        FROM FriendRequest FR
        LEFT JOIN User US ON (
            (FR.SenderID = %s AND US.UserID = FR.ReceiverID) OR 
            (FR.ReceiverID = %s AND US.UserID = FR.SenderID)
        )
        WHERE FR.Status = 2 AND US.UserID IS NOT NULL
    """, (user_id, user_id))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_pending_friend_requests(user_id: int):
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT FR.SenderID, FR.ReceiverID, FR.DateTime, US.Username AS SenderName
        FROM FriendRequest FR
        LEFT JOIN User US ON FR.SenderID = US.UserID
        WHERE FR.ReceiverID = %s AND FR.Status = 1
        ORDER BY FR.DateTime DESC
    """, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def send_friend_request(sender_id: int, receiver_id: int):
    connection = get_connection()
    if not connection:
        return -1
    cursor = connection.cursor()
    try:
        result_args = cursor.callproc('NewFriendRequest', [sender_id, receiver_id, datetime.now(), 0])
        connection.commit()
        result = result_args[3]
    except Exception as e:
        print(f"Error: {e}")
        result = -1
    finally:
        cursor.close()
        connection.close()
    return result

def accept_friend_request(sender_id: int, receiver_id: int):
    connection = get_connection()
    if not connection:
        return -1
    cursor = connection.cursor()
    try:
        result_args = cursor.callproc('FriendRequestAccept', [sender_id, receiver_id, datetime.now(), 0])
        connection.commit()
        result = result_args[3]
    except Exception as e:
        print(f"Error: {e}")
        result = -1
    finally:
        cursor.close()
        connection.close()
    return result

def reject_friend_request(sender_id: int, receiver_id: int):
    connection = get_connection()
    if not connection:
        return -1
    cursor = connection.cursor()
    try:
        result_args = cursor.callproc('FriendRequestReject', [sender_id, receiver_id, datetime.now(), 0])
        connection.commit()
        result = result_args[3]
    except Exception as e:
        print(f"Error: {e}")
        result = -1
    finally:
        cursor.close()
        connection.close()
    return result

def add_favourite(user_id: int, beer_id: int):
    connection = get_connection()
    if not connection:
        return False
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO User_Favourite (UserID, Beer_ID) VALUES (%s, %s)",
            (user_id, beer_id)
        )
        connection.commit()
        success = True
    except Exception:
        success = False
    finally:
        cursor.close()
        connection.close()
    return success

def remove_favourite(user_id: int, beer_id: int):
    connection = get_connection()
    if not connection:
        return False
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM User_Favourite WHERE UserID = %s AND Beer_ID = %s",
            (user_id, beer_id)
        )
        connection.commit()
        success = True
    except Exception:
        success = False
    finally:
        cursor.close()
        connection.close()
    return success

def get_user_favourites(user_id: int):
    connection = get_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT BE.Beer_ID, BE.Beer_Name, BE.Beer_Type, BE.AverageRating, BR.Brewery_Name
        FROM User_Favourite UF
        LEFT JOIN Beer BE ON UF.Beer_ID = BE.Beer_ID
        LEFT JOIN Brewery BR ON BE.Brewery_ID = BR.Brewery_ID
        WHERE UF.UserID = %s
        ORDER BY BE.Beer_Name
    """, (user_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
