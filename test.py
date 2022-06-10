import requests

from examples.example import number_of_variables

url = 'http://127.0.0.1:5000/api/targeted_population/'
database_details = {
    'database_name': 'mongodb',
    'collection': 'day001',
    'database': 'Bangalore',
    'fields': ['C/10001']
}
time_input = {
    'column_name': 'Date',
    'split': 'week',
    'period': 'life_time',
    'start_point': '2021/01/08',
    'end_point': '2021/01/25',
}
stage_input_list = [
    {
        'd': 0,
        'm_or_A_selction': 'population_average',
        'm_or_A_value': 300,
        'error': 10,
        'r': 100,
        'start_point': 0,
        'end_point': 700,
        'a': 2,
    },

]
distribution_input = {
    'normal': 1,
    'poisson': 0,
    'binomial': 0,
    'bernoulli': 1

}
request_data = {
    'database_details': database_details,
    'distribution_input': distribution_input,
    'number_of_variable': number_of_variables,
    'stages': stage_input_list,
    'time_input': time_input,
}

headers = {'content-type': 'application/json'}

response = requests.post(url, json=request_data, headers=headers)

print(response.text)