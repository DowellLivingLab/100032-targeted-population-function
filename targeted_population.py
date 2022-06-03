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
        distribution_results['bernoulli'] = bernoulli_distribution()

    return distribution_results
