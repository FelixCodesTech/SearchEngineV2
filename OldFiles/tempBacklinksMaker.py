# This is a temporary script file that will make a new csv
# that is basically the same as the classic data.csv but with an added column called backlinks

import csv


# Open the data.csv file
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
    lengthData = len(data)
    
    # Open the new file
    with open('dataWithBacklinks.csv', 'w', newline='') as newFile:
        writer = csv.writer(newFile)
        
        # Write the new data to the new file and count backlinks
        for i, row in enumerate(data):
            # Check how many times the 'URL' column is mentioned in other rows 'extLinks' column
            currURL = row[0]
            backlinks = 0

            for row2 in data:
                extLinks = row2[1]#.split(',')

                if currURL in extLinks:
                    backlinks += 1

            # Add the backlinks count to the row
            row.append(backlinks)
            writer.writerow(row)

            # Statistics
            print(f'Current count backlinks {backlinks} for {currURL}')
            print(f'Already done {round(i/lengthData, 2)*100}% ({i} out of {lengthData})')
        
