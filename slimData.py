outfile = open('export2021.xml', 'w')
with open('apple_health_export/export.xml') as in_file:
    for i in range(135):
        outfile.write(in_file.readline())
    for i in range(1766023 - 135):
        line = in_file.readline()
        if line.find('creationDate="2021') != -1:
            outfile.write(line)
outfile.close()
