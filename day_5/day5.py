from typing import List

def get_input():
    pipe_separated_dict = {}
    comma_separated = []

    with open('input', 'r') as file:
        for line in file:
            line = line.strip()

            if '|' in line:
                key, value = map(int, line.split('|'))

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


def sort(ordering, rules):
    made_change = False

    # is there any value to the left that violates the rules?
    # step through them backwards

    for i in range(len(ordering) - 1, -1, -1):

        if ordering[i] not in rules:
            continue
        
        for j in range(i - 1, -1, -1):
            if ordering[j] in rules[ordering[i]]:

                # move ordering[j] to the right of ordering[i]
                value_to_move = ordering.pop(j)
                ordering.insert(i + 1, value_to_move)
                
                made_change = True
                break

        if made_change:
            break

    # if a change was made, call sort again to recheck for rule violations
    if made_change:
        sort(ordering, rules)

    return ordering


def main():
    rules, orderings = get_input()

    tally = 0
    incorrects_tally = 0
    for ordering in orderings:
        if is_valid_ordering(ordering, rules):
            tally = tally + get_mid_value(ordering)
        else:
            incorrects_tally = incorrects_tally + get_mid_value(sort(ordering, rules))
    
    print(tally)
    print(incorrects_tally)


if __name__ == "__main__":
    main()