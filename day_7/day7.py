import itertools

def get_input():
    data = []
    with open('input', 'r') as file:
        for line in file:
            line = line.strip()

            result = line.split(':')
            result[0] = int(result[0])
            result[1] = list(map(int, result[1].strip().split(' ')))
            data.append(result)
    return data

def get_combinations(number_of_combos):
    values = ['+', '*', "||"]

    # Generate all combinations of '+', '*', "||"
    combinations = list(itertools.product(values, repeat=number_of_combos))
    return combinations

def part_one(data):
    total_sum = 0
    for value, parts in data:
        
        combinations = get_combinations(len(parts))
        
        for combination in combinations:
            tally = parts[0]
            for index in range(1, len(combination)):
                if combination[index] == '+':
                    tally = tally + parts[index]
                
                if combination[index] == '*':
                    tally = tally * parts[index]
                
                if combination[index] == '||':
                    tally = int(str(tally) + str(parts[index]))                

            if tally == value:
                total_sum = total_sum + value
                break
    return total_sum


def main():
    input = get_input()
    print(part_one(input))


if __name__ == "__main__":
    main()
