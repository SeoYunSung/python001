items = []
repair_history = []

while True:
    item_name = input("Enter item name (or enter 'q' to quit): ")
    if item_name == 'q':
        break

    items.append(item_name)
    item_repair = input("Enter repair history for " + item_name + ": ")
    repair_history.append(item_repair)

print("Items:", items)
print("Repair History:", repair_history)

