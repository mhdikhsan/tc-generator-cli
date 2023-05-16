if num < min_number:

min_number = num

if num > max_number:

max_number = num

for num in numbers:

print('Minimum number:', min_number)
print('Maximum number:', max_number)
sorted_numbers = numbers.copy()
n = len(sorted_numbers)

for i in range(n - 1):

print('Numbers in ascending...', sorted_numbers)
sorted_numbers_length = len(sorted_numbers)

if sorted_numbers_length % 2 == 0:

median = sorted_numbers[sorted_numbers_length // 2]

print('Median of the number...', median)
number_range = max_number - min_number
print('Range of the numbers...', number_range)
squared_differences = [((x - average) ** 2) for x in numbers]
variance = sum(squared_differences) / len(numbers)
print('Variance of the numb...', variance)
standard_deviation = variance ** 0.5
print('Standard Deviation o...', standard_deviation)
counts = {}

for num in numbers:

max_count = max(counts.values())
mode = [num for num, count in counts.items() if count == max_count]
print('Mode of the numbers:...', mode)
odd_numbers = [num for num in numbers if num % 2 != 0]
even_numbers = [num for num in numbers if num % 2 == 0]
positive_numbers = [num for num in numbers if num > 0]
negative_numbers = [num for num in numbers if num < 0]
print('Odd numbers:', odd_numbers)
print('Even numbers:', even_numbers)
print('Positive numbers:', positive_numbers)
print('Negative numbers:', negative_numbers)
product = 1

for num in numbers:

print('Product of the numbe...', product)
is_consecutive = True

for i in range(len(numbers) - 1):

print('The numbers are cons...', is_consecutive)

