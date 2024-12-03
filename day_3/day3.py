import re


def main():
    data = get_data()
    calculate(data)


def get_data():
    with open('input', 'r') as file:
        file_content = file.read()
        
    return file_content


def calculate(data):
    total = 0
       
    do_sections = re.split(r"do\(\)", data)

    for section in do_sections:
        dont_sections = re.split(r"don't\(\)", section)
        
        # Only add the first section if there are "don't" splits
        if(len(dont_sections) > 1):
            total = total + calc_sum(dont_sections[0])
        else:
            total = total + calc_sum(section)
    
    print(total)


def calc_sum(section):
    temp_total = 0
    
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", section)

    for match in matches:
        temp_total = temp_total + (int(match[0]) * int(match[1]))
    return temp_total


if __name__ == "__main__":
    main()