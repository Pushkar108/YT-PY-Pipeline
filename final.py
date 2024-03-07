import pandas as pd
from prophet import Prophet
import streamlit as st
import os

# Function to read and preprocess data
def read_and_preprocess_data(folder_path):
    all_files = os.listdir(folder_path)
    all_data = []

    for file in all_files:
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(folder_path, file))
            all_data.append(df)

    df_all = pd.concat(all_data)
    return df_all

# Function to forecast sales for a dish using Prophet
def forecast_dish_sales(dish_data):
    model = Prophet()
    model.fit(dish_data)
    future = model.make_future_dataframe(periods=365)  # Forecast for one year
    forecast = model.predict(future)
    return forecast

# Streamlit web application
def main():
    st.title('Dish Sales Forecast')

    # Read and preprocess data
    folder_path = "C:\Pegasus_Internship\data"
    df_all = read_and_preprocess_data(folder_path)

    # Dropdown menu to select dish
    unique_dishes = df_all['Item'].unique()
    selected_dish = st.selectbox('Select Dish', unique_dishes)

    # Filter data for selected dish
    selected_dish_data = df_all[df_all['Item'] == selected_dish]

    # Forecast sales for selected dish
    forecast = forecast_dish_sales(selected_dish_data)

    # Display forecast plot
    st.subheader('Forecast Plot')
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

if __name__ == "_main_":
    main()