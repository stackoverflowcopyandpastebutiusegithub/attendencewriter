import pygsheets

client = pygsheets.authorize(service_account_file='service_account.json')
sheet = client.open('YourSheetName')
worksheet = sheet.worksheet('YourWorksheetName')

data = []  # initialize an empty list to store the data

# define the dropdown options
dropdown_options = ['✔', 'P', 'A']

# dynamically add data to the list
for i in range(10):  # example: 10 rows
    row = []  # initialize an empty list to store the row data
    for j in range(5):  # example: 5 columns
        # create a DataValidation object for the dropdown
        dv = pygsheets.DataValidation(
            'LIST',
            {'values': dropdown_options},
            allowInvalid=False
        )
        # add the DataValidation object to the cell
        worksheet.update_value((i+1, j+1), '', data_validation=dv)
        row.append('')  # add an empty string to the row data
    data.append(row)  # add the row to the data list

worksheet.append_table(data)