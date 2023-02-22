def multiplication_table(n):
    for i in range(1, 10):
        print(n, "x", i, "=", n*i)

number = int(input("Enter the number for the multiplication table: "))
multiplication_table(number)