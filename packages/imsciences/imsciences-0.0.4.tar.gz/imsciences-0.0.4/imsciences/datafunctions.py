import pandas as pd

class dataprocessing:
    
    def hello(self):
        print("Hello from IMS, this is the data processing package")

    def remove_rows(self, data_frame, num_rows_to_remove):
        """
        Removes the specified number of rows from the given data frame, including the top row containing column names. 
        The next row will be treated as the new set of column headings.

        Parameters:
        - data_frame: pandas DataFrame
            The input data frame.
        - num_rows_to_remove: int
            The number of rows to remove from the data frame, starting from the original header.

        Returns:
        - pandas DataFrame
            The modified data frame with rows removed and new column headings.

        Raises:
        - TypeError: If num_rows_to_remove is not an integer.
        - ValueError: If num_rows_to_remove is negative or exceeds the total number of rows.
        """
        
        if not isinstance(num_rows_to_remove, int):
            raise TypeError("num_rows_to_remove must be an integer")

        if num_rows_to_remove < 0 or num_rows_to_remove >= len(data_frame):
            raise ValueError("Number of rows to remove must be non-negative and less than the total number of rows in the data frame.")

        if num_rows_to_remove == 0:
            return data_frame

        new_header = data_frame.iloc[num_rows_to_remove - 1]
        modified_data_frame = data_frame[num_rows_to_remove:] 
        modified_data_frame.columns = new_header

        return modified_data_frame
    
    def aggregate_to_wc(self, df, date_column, group_columns, sum_columns, wc):
        """
        Aggregates daily data into weekly data, starting on either Sundays or Mondays as specified, 
        and groups the data by additional specified columns. It sums specified numeric columns, 
        and pivots the data to create separate columns for each combination of the group columns 
        and sum columns. NaN values are replaced with 0.

        Parameters:
        - df: pandas DataFrame
            The input DataFrame containing daily data.
        - date_column: string
            The name of the column in the DataFrame that contains date information.
        - group_columns: list of strings
            Additional column names to group by along with the weekly grouping.
        - sum_columns: list of strings
            Numeric column names to be summed during aggregation.
        - wc: string
            The week commencing day ('sun' for Sunday or 'mon' for Monday).

        Returns:
        - pandas DataFrame
            A new DataFrame with weekly aggregated data. The index is the start of the week,
            and columns represent the grouped and summed metrics. The DataFrame is in wide format,
            with separate columns for each combination of grouped metrics.
        """

        # Make a copy of the DataFrame
        df_copy = df.copy()

        # Convert the date column to datetime and set it as the index
        df_copy[date_column] = pd.to_datetime(df_copy[date_column])
        df_copy.set_index(date_column, inplace=True)

        # Convert sum_columns to numeric
        for col in sum_columns:
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce').fillna(0).astype(int)

        # Group by week and additional columns, then sum the numeric columns
        if wc == "sun":
            weekly_grouped = df_copy.groupby([pd.Grouper(freq='W-SUN')] + group_columns)[sum_columns].sum()
        elif wc == "mon":
            weekly_grouped = df_copy.groupby([pd.Grouper(freq='W-MON')] + group_columns)[sum_columns].sum()
        else:
            return print("That is not the correct date input")
            
        # Reset index to turn the multi-level index into columns
        weekly_grouped_reset = weekly_grouped.reset_index()

        # Pivot the data to wide format
        wide_df = weekly_grouped_reset.pivot_table(index=date_column, 
                                                columns=group_columns, 
                                                values=sum_columns,
                                                aggfunc='first')

        # Flatten the multi-level column index and create combined column names
        wide_df.columns = [' '.join(col).strip() for col in wide_df.columns.values]

        # Fill NaN values with 0
        wide_df = wide_df.fillna(0)

        # Adding total columns for each unique sum_column
        for col in sum_columns:
            total_column_name = f'Total {col}'
            # Columns to sum for each unique sum_column
            columns_to_sum = [column for column in wide_df.columns if col in column]
            wide_df[total_column_name] = wide_df[columns_to_sum].sum(axis=1)

        return wide_df
