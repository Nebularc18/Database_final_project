# ============================================================================
# app.py
# ============================================================================
"""
This is the main entry point for the console application.
It provides the user interface and handles user interaction.

What to include here:
    1. Main menu display and navigation
    2. User input handling (reading from console)
    3. Calling functions from queries.py to interact with the database
    4. Displaying results to the user in a formatted way
    5. Input validation and error handling
    6. Loop structure to keep the application running until user exits

Example structure:
    def display_menu():
        # Print menu options

    def main():
        while True:
            display_menu()
            choice = input("Enter your choice: ")
            # Handle user choice
            # Call appropriate query functions
            # Display results

    if __name__ == "__main__":
        main()

Tips:
    - Keep this file focused on UI/input/output logic
    - Delegate database operations to queries.py
    - Use try-except blocks for error handling
    - Provide clear feedback to the user
    - Consider using a menu class for complex applications
"""