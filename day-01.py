filename = 'day-1.txt'


with open(filename) as file:
    elf_calorie = 0
    elf_calories = []

    def process_elf_calorie():
        global max_elf_calorie, elf_calorie
        print(f"found elf_calorie: {elf_calorie}")
        elf_calories.append(elf_calorie)
        elf_calorie = 0

    while (line := file.readline()):
        if line != '\n':
            elf_calorie += int(line)
        else:
            process_elf_calorie()

    process_elf_calorie()

    elf_calories = sorted(elf_calories)

    print(elf_calories[-3:])
    print(sum(elf_calories[-3:]))


