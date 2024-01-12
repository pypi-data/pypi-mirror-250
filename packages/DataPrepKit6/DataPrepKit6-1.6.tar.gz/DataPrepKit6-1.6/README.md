this toolkit functions designed to seamlessly read data from various file formats, provide a data summary, handle missing values, and encode categorical data.
1- to read date from various file formats you can do the following:

csv_file_path = 'path/to/your/file.csv'
excel_file_path = 'path/to/your/file.xlsx'
json_file_path = 'path/to/your/file.json'

csv_data = read_csv(csv_file_path)
excel_data = read_excel(excel_file_path)
json_data = read_json(json_file_path)
#Replace 'path/to/your/file.csv', 'path/to/your/file.xlsx',
 and 'path/to/your/file.json' with the actual paths to your CSV, Excel, and JSON files, respectively. 
The read_csv, read_excel, and read_json functions handle the different file formats and return Pandas DataFrames containing the data.

2-provide a data summary as fllowing:
 Assuming csv_data, excel_data, and json_data are DataFrames from the previous example

print("CSV Data Summary:")
data_summary(csv_data)

print("Excel Data Summary:")
data_summary(excel_data)

print("JSON Data Summary:")
data_summary(json_data)
This data_summary function takes a Pandas DataFrame as input and prints key statistical summaries using the describe method for general statistics, 
the mean method for average values,
 and the mode method for the most frequent values for each column.

Replace csv_data, excel_data, and json_data with your actual DataFrames.
 This will give you a summary of statistical information for each dataset, including average values and most frequent values.

 3-for handle missing values:
 Assuming csv_data, excel_data, and json_data are DataFrames from previous examples

 Remove missing values
cleaned_csv_data_remove = handle_missing_values(csv_data, strategy='remove')

 Impute missing values with mean
cleaned_excel_data_mean = handle_missing_values(excel_data, strategy='mean')

 Impute missing values with a constant value
cleaned_json_data_constant = handle_missing_values(json_data, strategy='constant', value=0)

 Display cleaned data
print("Cleaned CSV Data (Remove):")
print(cleaned_csv_data_remove.head())

print("\nCleaned Excel Data (Impute with Mean):")
print(cleaned_excel_data_mean.head())

print("\nCleaned JSON Data (Impute with Constant Value):")
print(cleaned_json_data_constant.head())
Replace csv_data, excel_data, and json_data with your actual DataFrames.
 The handle_missing_values function takes a Pandas DataFrame, a strategy for handling missing values,
 and an optional constant value for imputation. The returned DataFrame will have missing values handled based on the specified strategy.
4-encode categorical data as fllowing:
Assuming csv_data, excel_data, and json_data are DataFrames from previous examples

 One-hot encode categorical columns
categorical_columns = ['Category']  # Replace with your actual categorical column names
one_hot_encoded_csv_data = one_hot_encode(csv_data, columns=categorical_columns)

Label encode a single categorical column
label_encoded_excel_data = label_encode(excel_data, column='Category')

 Display encoded data
print("One-Hot Encoded CSV Data:")
print(one_hot_encoded_csv_data.head())

print("\nLabel Encoded Excel Data:")
print(label_encoded_excel_data.head())

Replace csv_data, excel_data, and json_data with your actual DataFrames. 
Specify the appropriate categorical columns for one-hot encoding in the categorical_columns list.
 The one_hot_encode function uses Pandas get_dummies method for one-hot encoding,
 and the label_encode function uses Pandas Categorical for label encoding.

