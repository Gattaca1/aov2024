def main():
    list_one, list_two = get_lists()
    list_one.sort()
    list_two.sort()

    #part_one(list_one, list_two)
    
    histogram = get_histogram(list_two)
    part_two(list_one, histogram)


def get_lists():
    with open('input', 'r') as file:
        list_one = []
        list_two = []

        for line in file:
            # Strip any leading/trailing whitespace and split by whitespace
            numbers = line.strip().split()

            # Ensure we have exactly two numbers
            if len(numbers) == 2:
                num1 = int(numbers[0])
                num2 = int(numbers[1])

                list_one.append(num1)
                list_two.append(num2)
        
        return [list_one, list_two]


def part_one(list_one, list_two):
    sum = 0
    for i in range(len(list_one)):
        print("%d - %d = %d" % (list_one[i], list_two[i], abs(list_one[i] - list_two[i])))
        sum += abs(list_one[i] - list_two[i])
    
    print(sum)


def get_histogram(numbers):
    histogram = {}

    for number in numbers:
        if number in histogram:
            histogram[number] += 1
        else:
            histogram[number] = 1
    
    return histogram


def part_two(list_one, histogram):
    difference_score = 0

    for number in list_one:
        if number in histogram:
            difference_score += number * histogram[number]
    
    print(difference_score)

if __name__ == "__main__":
    main()