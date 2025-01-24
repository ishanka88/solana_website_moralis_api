from website import create_app
from website.modles import FinderRunningBreak  # Import your model

app = create_app()

def add_initial_data():
    with app.app_context():
        # Check if the row already exists to avoid duplicates
        existing_entry = FinderRunningBreak.query.first()
        if not existing_entry:
            # Create a new entry
            FinderRunningBreak.add_item(value=False)
                        
            print("Initial data added to FinderRunning table.")
        else:
            print("FinderRunning table already has data.")


if __name__ == '__main__':
    add_initial_data()
    app.run(debug=True )