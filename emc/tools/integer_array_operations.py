a = "2172 5163 7500 8187 8208 8238 10975 10985 11007 12964 13000" # input(">>> ")
b = "8238 8187 12964"# input(">>> ")

a = [int(i.strip()) for i in filter(lambda i: bool(i), a.split(' '))]
b = [int(i.strip()) for i in filter(lambda i: bool(i), b.split(' '))]

a = set(a) 
b = set(b)

c = ' '.join([str(i) for i in list(eval(input(">>> "), {"a": a, "b": b}))])

print(c)


