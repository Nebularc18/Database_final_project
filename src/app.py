import queries

current_user = None

def clear_screen():
    print("\n" + "="*50 + "\n")

def press_enter():
    input("\nPress Enter to continue...")

def display_main_menu():
    print("\n" + "="*50)
    print("       BEER REVIEW DATABASE")
    print("="*50)
    if current_user:
        print(f"\nLogged in as: {current_user['Username']}")
    print("\n1. Browse Beers")
    print("2. Browse Breweries")
    print("3. Browse Users")
    print("4. Top Rated Beers")
    print("5. Login / Switch User")
    print("6. Logout")
    if current_user:
        print("7. My Account")
    print("0. Exit")
    print("-"*50)

def browse_beers():
    while True:
        beers = queries.get_all_beers()
        print("\n--- ALL BEERS ---\n")
        for beer in beers:
            rating = f"{beer['AverageRating']:.1f}" if beer['AverageRating'] else "N/A"
            print(f"{beer['Beer_ID']}: {beer['Beer_Name']} ({beer['Beer_Type']}) - {beer['Brewery_Name']} - Rating: {rating}")
        
        print("\n1. View Beer Details")
        print("2. Add Review (requires login)")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            try:
                beer_id = int(input("Enter Beer ID: "))
                view_beer_details(beer_id)
            except ValueError:
                print("Invalid ID")
        elif choice == "2":
            if not current_user:
                print("Please login first")
            else:
                try:
                    beer_id = int(input("Enter Beer ID: "))
                    add_review(beer_id)
                except ValueError:
                    print("Invalid ID")
        elif choice == "0":
            break

def view_beer_details(beer_id: int):
    beer = queries.get_beer_by_id(beer_id)
    if not beer:
        print("Beer not found")
        return
    
    print(f"\n--- {beer['Beer_Name']} ---")
    print(f"Type: {beer['Beer_Type']}")
    print(f"Brewery: {beer['Brewery_Name']}")
    print(f"Description: {beer['Official_Description'] or 'N/A'}")
    print(f"Ingredients: {beer['Ingredients'] or 'N/A'}")
    rating = f"{beer['AverageRating']:.1f}" if beer['AverageRating'] else "N/A"
    print(f"Rating: {rating} ({beer['NrOfReviews']} reviews)")
    
    reviews = queries.get_reviews_for_beer(beer_id)
    if reviews:
        print("\n--- Reviews ---")
        for rev in reviews:
            print(f"\n{rev['Username']} - Rating: {rev['Rating']}/10")
            print(f"'{rev['ReviewText'] or 'No text'}' ({rev['DateTime']})")
    
    if current_user:
        favs = queries.get_user_favourites(current_user['UserID'])
        is_fav = any(f['Beer_ID'] == beer_id for f in favs)
        if is_fav:
            print("\n[This beer is in your favourites]")
            if input("Remove from favourites? (y/n): ").lower() == 'y':
                queries.remove_favourite(current_user['UserID'], beer_id)
                print("Removed from favourites")
        else:
            if input("\nAdd to favourites? (y/n): ").lower() == 'y':
                queries.add_favourite(current_user['UserID'], beer_id)
                print("Added to favourites")

def add_review(beer_id: int):
    beer = queries.get_beer_by_id(beer_id)
    if not beer:
        print("Beer not found")
        return
    
    print(f"\nReviewing: {beer['Beer_Name']}")
    
    try:
        rating = int(input("Rating (1-10): "))
        if rating < 1 or rating > 10:
            print("Rating must be 1-10")
            return
    except ValueError:
        print("Invalid rating")
        return
    
    review_text = input("Review (optional): ").strip() or None
    
    reviews = queries.get_reviews_for_beer(beer_id)
    review_id = max([r['ReviewID'] for r in reviews], default=0) + 1
    
    result = queries.create_review(review_id, current_user['UserID'], beer_id, rating, review_text)
    if result:
        print("Review added!")
    else:
        print("Failed to add review")

def browse_breweries():
    breweries = queries.get_all_breweries()
    print("\n--- ALL BREWERIES ---\n")
    for br in breweries:
        print(f"{br['Brewery_ID']}: {br['Brewery_Name']} ({br['NrOfBeer']} beers)")
        print(f"   Address: {br['Headquarters_address'] or 'N/A'}")
    
    print("\n1. View Brewery Details")
    print("0. Back")
    
    choice = input("\nChoice: ").strip()
    
    if choice == "1":
        try:
            br_id = int(input("Enter Brewery ID: "))
            view_brewery_details(br_id)
        except ValueError:
            print("Invalid ID")

def view_brewery_details(brewery_id: int):
    brewery = queries.get_brewery_by_id(brewery_id)
    if not brewery:
        print("Brewery not found")
        return
    
    print(f"\n--- {brewery['Brewery_Name']} ---")
    print(f"Address: {brewery['Headquarters_address'] or 'N/A'}")
    print(f"Number of Beers: {brewery['NrOfBeer']}")
    
    beers = queries.get_all_beers()
    brewery_beers = [b for b in beers if b['Brewery_ID'] == brewery_id]
    
    if brewery_beers:
        print("\nBeers:")
        for b in brewery_beers:
            rating = f"{b['AverageRating']:.1f}" if b['AverageRating'] else "N/A"
            print(f"  - {b['Beer_Name']} ({b['Beer_Type']}) - Rating: {rating}")

def browse_users():
    users = queries.get_all_users()
    print("\n--- ALL USERS ---\n")
    for u in users:
        print(f"{u['UserID']}: {u['Username']} ({u['NrOfReviews']} reviews)")
    
    print("\n1. View User Profile")
    print("0. Back")
    
    choice = input("\nChoice: ").strip()
    
    if choice == "1":
        try:
            user_id = int(input("Enter User ID: "))
            view_user_profile(user_id)
        except ValueError:
            print("Invalid ID")

def view_user_profile(user_id: int):
    user = queries.get_user_by_id(user_id)
    if not user:
        print("User not found")
        return
    
    print(f"\n--- {user['Username']} ---")
    print(f"Reviews: {user['NrOfReviews']}")
    
    reviews = queries.get_reviews_by_user(user_id)
    if reviews:
        print("\nRecent Reviews:")
        for r in reviews[:5]:
            print(f"  - {r['Beer_Name']}: {r['Rating']}/10")
    
    if current_user and current_user['UserID'] != user_id:
        friends = queries.get_friends(current_user['UserID'])
        is_friend = any(f['UserID'] == user_id for f in friends)
        
        if is_friend:
            print("\n[This user is your friend]")
        else:
            pending = queries.get_pending_friend_requests(user_id)
            has_pending = any(p['SenderID'] == current_user['UserID'] for p in pending)
            
            if has_pending:
                print("\n[Friend request pending]")
            else:
                if input("\nSend friend request? (y/n): ").lower() == 'y':
                    result = queries.send_friend_request(current_user['UserID'], user_id)
                    if result == 0:
                        print("Friend request sent!")
                    else:
                        print("Could not send request (already friends or pending)")

def top_rated_beers():
    beers = queries.get_top_rated_beers(5)
    print("\n--- TOP RATED BEERS ---\n")
    for i, b in enumerate(beers, 1):
        print(f"{i}. {b['Beer_Name']} ({b['Brewery_Name']})")
        print(f"   Rating: {b['AverageRating']:.1f} ({b['NrOfReviews']} reviews)")

def login():
    global current_user
    users = queries.get_all_users()
    
    print("\n--- LOGIN ---\n")
    print("Available users:")
    for u in users:
        print(f"  {u['UserID']}: {u['Username']}")
    
    try:
        user_id = int(input("\nEnter User ID: "))
        user = queries.get_user_by_id(user_id)
        if user:
            current_user = user
            print(f"\nLogged in as {user['Username']}")
        else:
            print("User not found")
    except ValueError:
        print("Invalid ID")

def logout():
    global current_user
    current_user = None
    print("Logged out")

def friend_requests_menu():
    if not current_user:
        print("Please login first")
        return
    
    while True:
        print(f"\n--- FRIEND REQUESTS ({current_user['Username']}) ---\n")
        
        pending = queries.get_pending_friend_requests(current_user['UserID'])
        if pending:
            print("Pending requests:")
            for p in pending:
                print(f"  From: {p['SenderName']} (ID: {p['SenderID']}) - {p['DateTime']}")
            
            print("\n1. Accept Request")
            print("2. Reject Request")
        else:
            print("No pending requests")
        
        friends = queries.get_friends(current_user['UserID'])
        if friends:
            print("\nYour friends:")
            for f in friends:
                print(f"  - {f['Username']}")
        
        print("\n0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1" and pending:
            try:
                sender_id = int(input("Enter sender ID to accept: "))
                result = queries.accept_friend_request(sender_id, current_user['UserID'])
                if result == 0:
                    print("Friend request accepted!")
                else:
                    print("Could not accept request")
            except ValueError:
                print("Invalid ID")
        elif choice == "2" and pending:
            try:
                sender_id = int(input("Enter sender ID to reject: "))
                result = queries.reject_friend_request(sender_id, current_user['UserID'])
                if result == 0:
                    print("Friend request rejected")
                else:
                    print("Could not reject request")
            except ValueError:
                print("Invalid ID")
        elif choice == "0":
            break

def my_favourites():
    if not current_user:
        print("Please login first")
        return
    
    favs = queries.get_user_favourites(current_user['UserID'])
    
    print(f"\n--- MY FAVOURITES ({current_user['Username']}) ---\n")
    
    if favs:
        for f in favs:
            rating = f"{f['AverageRating']:.1f}" if f['AverageRating'] else "N/A"
            print(f"  - {f['Beer_Name']} ({f['Beer_Type']}) - {f['Brewery_Name']} - Rating: {rating}")
    else:
        print("No favourites yet")

def friends_reviews():
    if not current_user:
        print("Please login first")
        return
    
    reviews = queries.get_friends_reviews(current_user['UserID'])
    
    print(f"\n--- FRIENDS' REVIEWS ---\n")
    
    if reviews:
        for r in reviews:
            if r['Beer_Name']:
                print(f"{r['Friend']} reviewed {r['Beer_Name']}: {r['Rating']}/10")
                print(f"  '{r['ReviewText'] or 'No text'}' ({r['DateTime']})\n")
    else:
        print("No reviews from friends yet")

def user_menu():
    while True:
        print(f"\n--- USER MENU ({current_user['Username']}) ---")
        print("\n1. My Reviews")
        print("2. My Favourites")
        print("3. Friend Requests")
        print("4. Friends' Reviews")
        print("0. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            reviews = queries.get_reviews_by_user(current_user['UserID'])
            print(f"\n--- MY REVIEWS ---\n")
            if reviews:
                for r in reviews:
                    print(f"  - {r['Beer_Name']}: {r['Rating']}/10")
                    print(f"    '{r['ReviewText'] or 'No text'}' ({r['DateTime']})\n")
            else:
                print("No reviews yet")
        elif choice == "2":
            my_favourites()
        elif choice == "3":
            friend_requests_menu()
        elif choice == "4":
            friends_reviews()
        elif choice == "0":
            break

def main():
    global current_user
    
    while True:
        display_main_menu()
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            browse_beers()
        elif choice == "2":
            browse_breweries()
        elif choice == "3":
            browse_users()
        elif choice == "4":
            top_rated_beers()
        elif choice == "5":
            login()
        elif choice == "6":
            logout()
        elif choice == "7" and current_user:
            user_menu()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice")
        
        press_enter()

if __name__ == "__main__":
    main()
