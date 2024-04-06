import json

# Constants
ROWS = 20
COLS = 26
SEAT_AVAILABLE = 'a'
SEAT_OCCUPIED = 'X'
TICKET_PRICES = {
    "Front": 80,
    "Middle": 50,
    "Back": 25
}
STATE_TAX_RATE = 0.0725
MASK_FEE = 5.00

# Initialize seating data
seats = [[SEAT_AVAILABLE] * COLS for _ in range(ROWS)]

# Function to print seating layout
def print_seating():
    print("   " + " ".join(chr(i) for i in range(ord('a'), ord('z') + 1)))
    for i, row in enumerate(seats):
        print(f"{i+1:2d} {' '.join(row)}")

# Function to purchase tickets and show the price of ticket 
def purchase_tickets(row, col, num_tickets, ticket_type):
    if any(seats[row][col+i] != SEAT_AVAILABLE for i in range(num_tickets)):
        return False, "One or more seats already occupied."
    seats[row][col:col+num_tickets] = [SEAT_OCCUPIED] * num_tickets
    total_price = TICKET_PRICES[ticket_type] * num_tickets
    total_price *= 1 + STATE_TAX_RATE
    total_price += MASK_FEE * num_tickets
    return True, total_price

# Function to generate receipt
def generate_receipt(name, email, num_tickets, ticket_type, total_price):
    receipt = {
        "Name": name,
        "Email": email,
        "Number of Tickets": num_tickets,
        "Ticket Type": ticket_type,
        "Total Price": total_price
    }
    with open("receipt.json", "w") as file:
        json.dump(receipt, file, indent=4)

# Function to search by name
def search_by_name(name):
    found = False
    for i, row in enumerate(seats):
        for j, seat in enumerate(row):
            if seat == name:
                print(f"Seat {chr(j+ord('a')).upper()}{i+1} - {name}")
                found = True
    if not found:
        print("No tickets found for this name.")

# Function to display all purchases
def display_purchases():
    total_income = 0
    with open("purchases.json") as file:
        purchases = json.load(file)
        for purchase in purchases:
            print(f"Name: {purchase['Name']}, Email: {purchase['Email']}, Tickets: {purchase['Number of Tickets']}, Ticket Type: {purchase['Ticket Type']}, Total Price: ${purchase['Total Price']:.2f}")
            total_income += purchase['Total Price']
    print(f"Total Income: ${total_income:.2f}")

# Function to save purchases
def save_purchase(name, email, num_tickets, ticket_type, total_price):
    purchase = {
        "Name": name,
        "Email": email,
        "Number of Tickets": num_tickets,
        "Ticket Type": ticket_type,
        "Total Price": total_price
    }
    with open("purchases.json", "a") as file:
        json.dump(purchase, file)
        file.write('\n')

# Main function
def main():
    print("Welcome to the Outdoor Park Concert App!")
    print_seating()

    running = True
    while running:
        choice = input("\nMenu: [V]iew seating, [B]uy ticket(s), [S]earch by name, [D]isplay purchases, [Q]uit: ").upper()
        if choice == 'V':
            print_seating()
        elif choice == 'B':
            buy_tickets()
        elif choice == 'S':
            name = input("Enter name to search: ")
            search_by_name(name)
        elif choice == 'D':
            display_purchases()
        elif choice == 'Q':
            print("Thank you for using the Outdoor Park Concert App!")
            running = False
        else:
            print("Invalid choice. Please try again.")

# Function to handle ticket purchasing
def buy_tickets():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    row = int(input("Enter row number: ")) - 1
    col_input = input("Enter column letter: ").lower()
    if not col_input.isalpha() or col_input < 'a' or col_input > 'z':
        print("Invalid column letter. Please enter a letter between 'a' and 'z'.")
        return
    col = ord(col_input) - ord('a')
    num_tickets = int(input("Enter number of tickets: "))
    ticket_type = input("Enter ticket type (Front/Middle/Back): ").capitalize()
    success, total_price = purchase_tickets(row, col, num_tickets, ticket_type)
    if success:
        print(f"Purchase successful! Total price: ${total_price:.2f}")
        generate_receipt(name, email, num_tickets, ticket_type, total_price)
        save_purchase(name, email, num_tickets, ticket_type, total_price)
    else:
        print("Error:", total_price)

if __name__ == "__main__":
    main()
