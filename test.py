
for j in range(10):
    print(f"j: {j}")
    for i in range(10):
        input(f"i:{i}")
        if i == 3:
            j += 1
            break