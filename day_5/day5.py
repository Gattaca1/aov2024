from typing import List

def get_input():
    pipe_separated_dict = {}
    comma_separated = []

    with open('input', 'r') as file:
        for line in file:
            line = line.strip()

            if '|' in line:
                key, value = map(int, line.split('|'))

                # If the key is already in the dictionary, append the value to the list
                if key not in pipe_separated_dict:
                    pipe_separated_dict[key] = []
                pipe_separated_dict[key].append(value)
            elif ',' in line:
                numbers = list(map(int, line.split(',')))
                comma_separated.append(numbers)
    
    return pipe_separated_dict, comma_separated


def is_valid_ordering(ordering, rules):
    # is there any value to the left that violates the rules?
    # step through them backwards

    for i in range(len(ordering) - 1, -1, -1):

        # skip checking this number if it doesn't have any associated rules
        if ordering[i] not in rules:
            continue
        
        for j in range(i - 1, -1, -1):
            if ordering[j] in rules[ordering[i]]:
                return False
    
    return True
    

def get_mid_value(ordering):
    return ordering[len(ordering) // 2]

def main():
    rules, orderings = get_input()

    tally = 0
    for ordering in orderings:
        if is_valid_ordering(ordering, rules):
            tally = tally + get_mid_value(ordering)
    
    print(tally)


if __name__ == "__main__":
    main()