def number_operations(numbers):
    # Check if the list is empty
    if not numbers:
        print("The list is empty.")
        return

    # Calculate the sum of the numbers
    total_sum = 0
    for num in numbers:
        total_sum += num
    print("Sum of the numbers:", total_sum)

    # Calculate the average of the numbers
    average = total_sum / len(numbers)
    print("Average of the numbers:", average)

    # Find the minimum and maximum numbers
    min_number = numbers[0]
    max_number = numbers[0]
    for num in numbers:
        if num < min_number:
            min_number = num
        if num > max_number:
            max_number = num
    print("Minimum number:", min_number)
    print("Maximum number:", max_number)

    # Sort the numbers in ascending order using bubble sort
    sorted_numbers = numbers.copy()
    n = len(sorted_numbers)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if sorted_numbers[j] > sorted_numbers[j + 1]:
                sorted_numbers[j], sorted_numbers[j +
                                                  1] = sorted_numbers[j + 1], sorted_numbers[j]
    print("Numbers in ascending order:", sorted_numbers)

    # Calculate the median of the numbers
    sorted_numbers_length = len(sorted_numbers)
    if sorted_numbers_length % 2 == 0:
        median = (sorted_numbers[sorted_numbers_length // 2 - 1] +
                  sorted_numbers[sorted_numbers_length // 2]) / 2
    else:
        median = sorted_numbers[sorted_numbers_length // 2]
    print("Median of the numbers:", median)

    # Calculate the range of the numbers
    number_range = max_number - min_number
    print("Range of the numbers:", number_range)

    # Calculate the variance of the numbers
    squared_differences = [(x - average) ** 2 for x in numbers]
    variance = sum(squared_differences) / len(numbers)
    print("Variance of the numbers:", variance)

    # Calculate the standard deviation of the numbers
    standard_deviation = variance ** 0.5
    print("Standard Deviation of the numbers:", standard_deviation)

    # Find the mode of the numbers
    counts = {}
    for num in numbers:
        if num in counts:
            counts[num] += 1
        else:
            counts[num] = 1
    max_count = max(counts.values())
    mode = [num for num, count in counts.items() if count == max_count]
    print("Mode of the numbers:", mode)

    # Perform additional calculations
    odd_numbers = [num for num in numbers if num % 2 != 0]
    even_numbers = [num for num in numbers if num % 2 == 0]
    positive_numbers = [num for num in numbers if num > 0]
    negative_numbers = [num for num in numbers if num < 0]

    print("Odd numbers:", odd_numbers)
    print("Even numbers:", even_numbers)
    print("Positive numbers:", positive_numbers)
    print("Negative numbers:", negative_numbers)

    # Calculate the product of all numbers
    product = 1
    for num in numbers:
        product *= num
    print("Product of the numbers:", product)

    # Check if the numbers are consecutive
    is_consecutive = True
    for i in range(len(numbers) - 1):
        if numbers[i] + 1 != numbers[i + 1]:
            is_consecutive = False
            break

    print("The numbers are consecutive:", is_consecutive)
