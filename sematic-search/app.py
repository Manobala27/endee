with open("data.txt", "r") as f:
    data = f.readlines()

print("Semantic Search System")

while True:
    query = input("Enter query: ")
    
    if query == "exit":
        break
    
    found = False
    
    for line in data:
        if query.lower() in line.lower():
            print("Result:", line.strip())
            found = True
    
    if not found:
        print("No result found")