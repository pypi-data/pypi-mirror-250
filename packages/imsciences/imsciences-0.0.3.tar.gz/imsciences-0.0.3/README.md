The IMS package is a python library for processing incomming data into a format that we can use for projects. IMS processing comes with the ability to:

1. remove_rows(df, number_of_rows):

    This function takes in a data frame and number of rows that you wish to remove and returns a data frame with that number of rows less

1. aggregate_to_wc(df, date_column, group_columns, sum_columns, wc):

    Aggregates daily data into weekly data, starting on either Sundays or Mondays as specified, 
    and groups the data by additional specified columns. It sums specified numeric columns, 
    and pivots the data to create separate columns for each combination of the group columns 
    and sum columns. NaN values are replaced with 0.
