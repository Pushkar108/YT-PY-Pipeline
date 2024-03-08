import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.graph_objs as go
import plotly.express as px
import glob
from datetime import datetime

# Function to load and preprocess the CSV files
def load_data(file):
    df = pd.read_csv(file)
    df['ds'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df = df[['ds', 'Qty.', 'Item']]
    df = df.rename(columns={'Qty.': 'y'})
    return df

# Streamlit app
def main():
    st.title('Sales Forecasting with Prophet')

    path = "C:\Pegasus_Internship\data"
    all_files = glob.glob(path + "//*.csv", recursive=True)
    file_names = [file.split("/")[-1] for file in all_files]

    selected_file = st.selectbox('Select a CSV file', file_names)

    df = load_data(all_files[file_names.index(selected_file)])
    
    m = Prophet()
    m.fit(df)

    # Create a DataFrame for future predictions starting from today
    today = datetime.now().date()
    future = pd.DataFrame({'ds': pd.date_range(start=today, periods=7)})
    
    # Make predictions
    forecast = m.predict(future)

    st.subheader('Forecasted Sales:')
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper',]])

    st.subheader('Forecast Components:')
    fig_components = plot_components_plotly(m, forecast)
    st.plotly_chart(fig_components)

    st.subheader('Future Sales Predictions:')
    future_forecast = forecast[forecast['ds'] > df['ds'].max()]
    fig_future = go.Figure()
    fig_future.add_trace(go.Scatter(x=future_forecast['ds'], y=future_forecast['yhat'], mode='lines', name='Predicted'))                    
    fig_future.update_layout(title='Future Sales Predictions',
                             xaxis_title='Date',
                             yaxis_title='Sales')
    st.plotly_chart(fig_future)

    st.subheader('Future Sales Predictions(Upper and Lower Bound):')
    future_forecast = forecast[forecast['ds'] > df['ds'].max()]
    fig_future = go.Figure()
    fig_future.add_trace(go.Scatter(x=future_forecast['ds'], y=future_forecast['yhat_lower'], mode='lines', name='Lower Bound'))
    fig_future.add_trace(go.Scatter(x=future_forecast['ds'], y=future_forecast['yhat_upper'], mode='lines', name='Upper Bound'))
    fig_future.update_layout(title='Future Sales Predictions',
                             xaxis_title='Date',
                             yaxis_title='Sales')
    st.plotly_chart(fig_future)

if __name__ == '_main_':
    main()