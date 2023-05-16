print('Product of the numbe...', product)
is_consecutive = True

for i in range(len(numbers) - 1):

if numbers[i] + 1 != numbers[i + 1]:

is_consecutive = False
break

print('The numbers are cons...', is_consecutive)

