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
    
    do_pattern = r"do\(\)"    
    do_sections = re.split(do_pattern, data)

    dont_pattern = r"don't\(\)"

    for section in do_sections:
        dont_sections = re.split(dont_pattern, section)
        
        if(len(dont_sections) > 1):
            total = total + calc_sum(dont_sections[0])
        else:
            total = total + calc_sum(section)
    
    print(total)


def calc_sum(section):
    temp_total = 0
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, section)

    for match in matches:
        temp_total = temp_total + (int(match[0]) * int(match[1]))
    return temp_total

if __name__ == "__main__":
    main()