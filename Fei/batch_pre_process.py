def add_statistics_measure(df, grain_size, time_length):
    temp_col = [i for i in range(time_length)]
    for i in range(time_length):
        df[temp_col[i]] = df.loc[
        (df[grain_size]==df[grain_size].shift(-i)) &
        (df['date']==df['date'].shift(-i) - datetime.timedelta(days=i))
        , 'sales']
        df[temp_col[i]] = df[temp_col[i]].shift(i)
    new_column_name_prefex = grain_size + '_paste_' + time_length + '_'
    # mean value
    df[new_column_name_prefex + 'ave'] = df[temp_col].mean(axis=1)
    # max value
    df[new_column_name_prefex + 'max'] = df[temp_col].max(axis=1)
    # min value
    df[new_column_name_prefex + 'min'] = df[temp_col].min(axis=1)
    # standard deviation
    df[new_column_name_prefex + 'std'] = df[temp_col].std(axis=1)
    df.drop(columns=temp_col, inplace=True)
    df_train.merge(df.drop(columns='sales'), left_on=['item', 'date'],
                    right_on=['item', 'date'], how='outer')

dfs = [df_train_item_store_sorted, df_train_item_sorted, df_train_store_sorted]
grain_sizes = ['store_item', 'item', 'store']
time_lengths = [7, 30]

for grain_size_num in range(2):
    for time_length in time_lengths:
        add_statistics_measure(dfs[grain_size_num], grainsizes[grain_size_num], time_length)
