import pandas
import random
from samplingrule.samplingrule import dowellsamplingrule


def normal_distribution(data, stage_input_list, number_of_variable):
    df = pandas.DataFrame(data)
    try:
        if stage_input_list:
            df = df.astype({'C/10001': 'float64', 'B/10002': 'float64', 'C/10003': 'float64', 'D/10004': 'float64'})
            # filter for all stages
            for stage in stage_input_list:
                d = stage['data_type']
                if d == 'lot':
                    df = filter_lot_database(df, stage)
                    if df.empty:
                        raise Exception('selection is not matching the required lot size')
                    continue
                if d == 0:
                    break

                if stage['m_or_A_selction'] == 'population_average':
                    df = filter_df_population_average(df, d, stage)
                else:
                    df = filter_df_max_point(df, d, stage)
                if df.empty:
                    raise Exception("not matched for datatype " + str(d))

        distribution_result_data = df.to_dict('dict')
        n = len(distribution_result_data)
        is_acceptable, sample_size, status = dowellsamplingrule(n, 1, number_of_variable)

        result = {
            "is_error": False,
            "data": distribution_result_data,
            "sampling_status": is_acceptable,
            "sampling_status_text": status,
        }

        return result

    except Exception as e:
        result = {
            "is_error": True,
            "error_text": e,
        }
        return result


def filter_lot_database(df, stage):
    proportion_selection = stage['p_r_selection']
    first_position = stage['first_position']
    last_position = stage['last_position']
    dataframe_size = len(df.index)

    if proportion_selection == "proportion":
        lot_size = int(dataframe_size * stage['proportion'] / 100)
        if first_position + lot_size - 1 <= dataframe_size:
            df = df[first_position - 1:lot_size]
            return df
        else:
            return pandas.DataFrame([])
    else:

        random_lot_size = random.randint(0, dataframe_size)
        if first_position + random_lot_size - 1 > dataframe_size:
            return pandas.DataFrame([])
        else:
            df = df[first_position - 1:random_lot_size]
            return df


def filter_df_population_average(df, column_name, stage):
    newpanda = df.sort_values(by=[column_name])
    start = float(stage['start_point'])
    r = stage['r']
    range_end = start + r
    end = float(stage['end_point'])
    population_average = stage['m_or_A_value']
    a = stage['a']
    error_percent = stage['error']
    population_average_min = population_average - population_average * error_percent / 100
    population_average_max = population_average + population_average * error_percent / 100
    taken = 0
    summation = 0

    sum_of_taken_numbers = 0
    taken_number_count = 0

    for index, row in newpanda.iterrows():
        try:
            current_mean = sum_of_taken_numbers / taken_number_count
        except Exception:
            current_mean = 0

        if current_mean == population_average:
            newpanda.drop(newpanda.index[index:], inplace=True)
            break
        if current_mean >= population_average_max or row[column_name] > end:
            newpanda.drop(newpanda.index[index:], inplace=True)
            break

        if start < row[column_name] < range_end:
            if taken >= a:
                newpanda.drop(index, inplace=True)
            else:
                expected_sum_of_taken_numnbers = sum_of_taken_numbers + row[column_name]
                expected_taken_number_count = taken_number_count + 1
                expected_mean = expected_sum_of_taken_numnbers / expected_taken_number_count

                if expected_mean <= population_average_max:
                    taken = taken + 1
                    taken_number_count = expected_taken_number_count
                    sum_of_taken_numbers = expected_sum_of_taken_numnbers
                else:
                    newpanda.drop(index, inplace=True)
        else:
            while True:
                taken = 0
                start = range_end
                range_end = start + r

                if start < row[column_name] < range_end:
                    expected_sum_of_taken_numnbers = sum_of_taken_numbers + row[column_name]
                    expected_taken_number_count = taken_number_count + 1
                    expected_mean = expected_sum_of_taken_numnbers / expected_taken_number_count

                    if expected_mean <= population_average_max:
                        taken = taken + 1
                        taken_number_count = expected_taken_number_count
                        sum_of_taken_numbers = expected_sum_of_taken_numnbers
                    else:
                        newpanda.drop(index, inplace=True)
                    break
                if range_end > end:
                    newpanda.drop(index, inplace=True)
                    break

    try:
        current_mean = sum_of_taken_numbers / taken_number_count
    except:
        current_mean = 0

    if population_average_min <= current_mean <= population_average_max:
        return newpanda
    else:
        return pandas.DataFrame([])


def filter_df_max_point(df, column_name, stage):
    newpanda = df.sort_values(by=[column_name])
    start = float(stage['start_point'])
    r = stage['r']
    range_end = start + r
    end = float(stage['end_point'])
    error_percent = stage['error']
    max_sum = stage['m_or_A_value']

    max_sum_min = max_sum - max_sum * error_percent / 100
    max_sum_max = max_sum + max_sum * error_percent / 100
    a = stage['a']

    taken = 0
    summation = 0

    for index, row in newpanda.iterrows():
        if summation >= max_sum_max or row[column_name] > end:
            newpanda.drop(index, inplace=True)
            continue

        if start < row[column_name] < range_end:
            if taken >= a:
                newpanda.drop(index, inplace=True)
            else:
                if summation + row[column_name] < max_sum_max:
                    taken = taken + 1
                    summation = summation + row[column_name]
                else:
                    newpanda.drop(index, inplace=True)
        else:
            while True:
                taken = 0
                start = range_end
                range_end = start + r
                if start < row[column_name] < range_end:
                    if summation + row[column_name] < max_sum_max:
                        taken = taken + 1
                        summation = summation + row[column_name]
                    else:
                        newpanda.drop(index, inplace=True)
                    break
                if range_end > end:
                    newpanda.drop(index, inplace=True)
                    break

    if max_sum_min <= summation <= max_sum_max:
        return newpanda
    else:
        return pandas.DataFrame([])