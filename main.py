import requests
from flask import Flask, render_template
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Function to retrieve COVID-19 data from the API
def get_covid_data(api_key):
    url = "https://api.covidactnow.org/v2/states.json?apiKey=" + api_key
    response = requests.get(url)
    data = response.json()
    return data

def extract_plot_data(data):
    states = []
    cases = []
    deaths = []
    
    for state_data in data:
        states.append(state_data['state'])
        cases.append(state_data['actuals']['cases'])
        deaths.append(state_data['actuals']['deaths'])
    
    return states, cases, deaths

@app.route('/')
def covid_dashboard():
    api_key = "6091611d37e64ef483227fc4e5b22438"
    data = get_covid_data(api_key)
    states, cases, deaths = extract_plot_data(data)

    # Create plot traces
    case_trace = go.Bar(x=states, y=cases, name='Cases')
    death_trace = go.Bar(x=states, y=deaths, name='Deaths')

    # Plot layout
    layout = go.Layout(title='COVID-19 Cases and Deaths by State',
                       xaxis=dict(title='States'),
                       yaxis=dict(title='Count'))

    # Configure plot figures
    case_figure = go.Figure(data=[case_trace], layout=layout)
    death_figure = go.Figure(data=[death_trace], layout=layout)

    case_graph = case_figure.to_html(full_html=False)
    death_graph = death_figure.to_html(full_html=False)

    return render_template('covid_dashboard.html', case_graph=case_graph, death_graph=death_graph)

if __name__ == '__main__':
    app.run(debug=True)
