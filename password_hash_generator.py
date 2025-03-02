from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def generate_password_hash(password):
    """Generate a bcrypt password hash"""
    return bcrypt.generate_password_hash(password).decode('utf-8')

def main():
    """Generate password hashes for the SQL script"""
    print("Password Hash Generator for LCC Issue Tracker")
    print("---------------------------------------------")
    print("This tool helps you generate password hashes for your database population script.")
    print("For each user, enter a password and the tool will generate a hash you can copy into your SQL script.")
    print("Press Ctrl+C to exit at any time.\n")
    
    try:
        while True:
            password = input("Enter password: ")
            if not password:
                print("Password cannot be empty. Try again.")
                continue
                
            password_hash = generate_password_hash(password)
            print(f"Password hash: '{password_hash}'")
            print("Copy this hash into your SQL INSERT statement.")
            print("---------------------------------------------\n")
    except KeyboardInterrupt:
        print("\nExiting password hash generator. Goodbye!")

if __name__ == "__main__":
    main()