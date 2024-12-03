from enum import Enum

class MonotonicState(Enum):
    NULL = 0
    INCREASING = 1
    DECREASING = 2

def main():
    data = get_data()
    test(data)


def get_data():
    with open('input2', 'r') as file:
        data = []

        for line in file:
            numbers = [int(x) for x in line.strip().split()]
            data.append(numbers)
        
        return data


def is_safe(num_array):
    array_direction = MonotonicState.NULL
    for index in range(len(num_array)):
        # Don't gotta check against first number
        if(index == 0):
            continue
        
        # Set the initial state of increasing or decreasing
        if(index == 1):
            if num_array[index] > num_array[index - 1]:
                array_direction = MonotonicState.INCREASING
            elif num_array[index] < num_array[index - 1]:
                array_direction = MonotonicState.DECREASING
        
        # Check for duplicate value
        if(num_array[index] == num_array[index - 1]):
            return False
        
        # Break out if current index value and previous index value differ by more than 3            
        difference = abs(int(num_array[index]) - int(num_array[index - 1]))
        if(difference > 3):
            return False
        
        # Break out if current index values direction isn't the same as array direction
        if(array_direction == MonotonicState.INCREASING and num_array[index] < num_array[index - 1]):
            return False
        elif(array_direction == MonotonicState.DECREASING and num_array[index] > num_array[index - 1]):
            return False
    
    return True


def test(data):
    safe_tally = 0
    for num_array in data:
        if is_safe(num_array):
            safe_tally += 1
        else:
            # try again but with each value removed in sequence
            for i in range(len(num_array)):
                temp_array = num_array[:i] + num_array[i+1:]
                if is_safe(temp_array):
                    safe_tally += 1
                    break
    print(safe_tally)
                
                


            
            
            

            

            


if __name__ == "__main__":
    main()