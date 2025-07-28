import random
import string

def generate_password(length):
    if length < 4:
        print("Password length should be at least 4 characters for security.")
        return None
    
    # define possible characters
    all_characters = string.ascii_letters + string.digits + string.punctuation
    
    # generate password
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

def main():
    print("=== Password Generator ===")
    try:
        length = int(input("Enter desired password length: "))
        password = generate_password(length)
        if password:
            print("\nGenerated Password:")
            print(password)
    except ValueError:
        print("Please enter a valid number.")

if __name__ == "__main__":
    main()
