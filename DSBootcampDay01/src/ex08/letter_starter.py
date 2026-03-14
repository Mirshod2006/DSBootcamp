import sys

def find_name(email, file_path="employees.tsv"):
    with open(file_path, "r") as file:
        next(file)
        for line in file:
            name, surname, email_in_file = line.strip().split("\t")
            if email_in_file == email:
                return name
    return None

def generate_letter(email):
    name = find_name(email)
    if name:
        print(f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. "
              "That’s a precondition for the professionals that our company hires.")
    else:
        print("Email not found in the employees file.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python welcome_letter.py <email>")
        sys.exit(1)
    
    email_input = sys.argv[1]
    generate_letter(email_input)