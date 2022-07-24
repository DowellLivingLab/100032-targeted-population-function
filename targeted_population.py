from get_data_tools import get_data_for_distribution
from normal_distribution import normal_distribution
from poisson_distribution import poisson_distribution
from binomial_distribution import binomial_distribution


def targeted_population(distribution_input, database_details, time_input, number_of_variable, stage_input_list):
    data, start_dowell_time, end_dowell_time = get_data_for_distribution(time_input,
                                                                         stage_input_list, database_details)
    print(data)
    distribution_results = {}

    if distribution_input['normal'] == 1:
        distribution_results['normal'] = normal_distribution(data, stage_input_list, number_of_variable)

    if distribution_input['poisson'] == 1:
        distribution_results['poisson'] = poisson_distribution(data, start_dowell_time, end_dowell_time,
                                                               stage_input_list, number_of_variable)

    if distribution_input['binomial'] == 1:
        number_of_variables=5
        split_choice = "simple"
        distribution_results['binomial'] = binomial_distribution(event_id="event_id", data=data, number_of_variables=number_of_variables, split_choice=split_choice, error="0", split_decision="Eliminate", user_choice="normal", function="=", marginal_error="0")

    if distribution_input['bernoulli'] == 1:

        distribution_results['bernoulli'] = "work in progress"

    return distribution_results

print()