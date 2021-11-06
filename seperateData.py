with open('export2021.xml') as in_file:
    source_names = set()
    for line in in_file:
        if line.find('sourceName=') != -1:
            beginning_index = line.index(' ', 17)
            first_quote = line.index('"', beginning_index)
            second_quote = line.index('"', first_quote + 1)
            source_names.add(line[first_quote + 1:second_quote])
print(source_names)

