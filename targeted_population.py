from get_data_tools import get_data_for_distribution
from normal_distribution import normal_distribution
from poisson_distribution import poisson_distribution
from binomial_distribution import binomial_distribution
from bernoulli_distribution import bernoulli_distribution


def targeted_population(distribution_input, database_details, time_input, number_of_variable, stage_input_list):
    data, start_dowell_time, end_dowell_time = get_data_for_distribution(time_input, database_details)
    distribution_results = {}
    fields = database_details['fields']
    split = time_input['split']

    """
    don't change the above lines
    ----------------------------------
    example of the function parameter datatype
    ----------------------------------
    distribution_input={
    'normal': 1,
    'poisson':0,
    'binomial':0,
    'bernoulli':0
    }
    -----------------------------------
    time_input = {
    'column_name': 'Date',
    'split': 'week',
    'period': 'last_30_days',
    'start_point': '2021/01/01',
    'end_point': '2022/01/25',
    }
    -------------------------------------
    'fields':['eventId', 'dowell_time']
    -------------------------------------
    number_of_variable is an integer value
    --------------------------------------
    stage_input_list = [
    ]
    --------------------------------------
    distribution_input, database_details, time_input, number_of_variable, stage_input_list
    """

    if distribution_input['normal'] == 1:
        distribution_results['normal'] = normal_distribution(data, stage_input_list, fields, number_of_variable)

    if distribution_input['poisson'] == 1:
        distribution_results['poisson'] = poisson_distribution(data, start_dowell_time, end_dowell_time,
                                                               split, stage_input_list, fields, number_of_variable)

    if distribution_input['binomial'] == 1:
        split_variable = 5
        split_choice = "simple"
        distribution_results['binomial'] = binomial_distribution(data, split_variable, split_choice)

    if distribution_input['bernoulli'] == 1:
        params = {
            "deck": 100,  # enter any number more than 100
            "error": 0.168,  # any float number
            "test_num": 7,  # integer number
            "deck_items": '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100'
            # items to be shuffled
        }
        selection_start_point = 3
        items_to_be_selected = 50

        distribution_results['bernoulli'] = bernoulli_distribution(params, selection_start_point, items_to_be_selected)

    return distribution_results
