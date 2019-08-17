
import pandas as pd
import numpy as np
import os
import json
from flask import Flask, request, make_response, jsonify



# laoding data and json
client_table = pd.read_excel('client_table.xlsx')


# possible queries
def process_count_intent(req):
    columns_names = req.get('queryResult').get('parameters').get('column_entity_1')
    t1 = ''
    t2 = ''
    t3 = ''

    for col in columns_names:
        if col == 'manager_id':
            managers_count = len(client_table['manager_id'].unique())
            t1 = str(managers_count) + ' managers '

        if col == 'client_id':
            client_count = len(client_table['client_id'].unique())
            t2 = str(client_count) + ' clients '

        if col == 'employees':
            employees_count = client_table['employees_on_project'].sum()
            t3 = str(employees_count) + ' employees'

    final_text = 'There are total  ' + t1+  t2 +  t3
 #   print(final_text)
    response_json = {'fulfillmentText': final_text}
    res = json.dumps(response_json, indent=4)
    return make_response(res)



def process_manager_summary(req):
    manager_name = req.get('queryResult').get('parameters').get('any').lower()
    manager_name1 = manager_name.lower().strip().split()
    manager_name1 = ''.join(manager_name1)
    client_table['manager_name_concat'] = client_table['manager_name'].str.lower().str.strip().str.split().str.join('')
    try:
        filtered_table = client_table.loc[client_table['manager_name_concat'] == manager_name1, : ]
        total_clients = len(filtered_table.client_name.unique())
        total_revenue = filtered_table.client_revenue.sum()
        total_employees_on_projects = filtered_table.employees_on_project.sum()
        max_client = filtered_table.client_name[filtered_table.client_revenue == max(filtered_table.client_revenue)].values[0]
        max_client_revenue = max(filtered_table.client_revenue)
        message = 'Here is the summary for manager {} \nTotal Clients Handeling: {} \nTotal Revenue from clients: {} \nHighest Paying client: {} \nRevenue from {}: {} \nEmployees on Projects: {}'.format(manager_name, total_clients, total_revenue, max_client, max_client, max_client_revenue, total_employees_on_projects)


    except:
        message = 'No client with name {} found. Please check the name again'.format(manager_name)

#    print(message)
    response_json = {'fulfillmentText': message}
    res = json.dumps(response_json, indent=4)
    return make_response(res)


#    response_json = {'fulfillmentText': final_text}
 #   res = json.dumps(response_json, indent=4)
  #  return make_response(res)


# flask app for webhook
app = Flask(__name__)
log = app.logger


@app.route('/', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    #printing the request json
   # print(req)
    # writing json to file
#    with open('request.json', 'w') as f:
 #       json.dump(req, f
    intent_name = req.get('queryResult').get('intent').get('displayName')
  #  print(intent_name)
    if intent_name == 'count-intent':
        return process_count_intent(req)

    if intent_name == 'manager-summary-followup':
        return process_manager_summary(req)


if __name__ == '__main__':
    app.run(port=9999)

# exec(intent_dict.get(intent_name))

