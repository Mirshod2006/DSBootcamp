import sys

def to_set(lst):
    return set(lst)

def call_center(clients, receipints):
    return clients - receipints

def potential_clients(clients, participants):
    return participants - clients

def loyalty_program(clients, participants):
    return clients - participants

def marketing(task):
    clients = to_set(['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
    'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
    'elon@paypal.com', 'jessica@gmail.com'])
    participants = to_set(['walter@heisenberg.com', 'vasily@mail.ru',
    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com'])
    recipients = to_set(['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is'])

    tasks = {
        'call_center' : call_center,
        'potential_clients' : potential_clients,
        'loyalty_program' : loyalty_program
    }
    if task not in tasks.keys():
        raise ValueError("Invalid task name. Choose from: call_center, potential_clients, loyalty_program")
    
    result = tasks[task](clients, participants if task != "call_center" else recipients)
    print(result)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 marketing.py <task_name>")
        exit(1)

    task_name = sys.argv[1]
    marketing(task_name)