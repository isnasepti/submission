import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Helper function
def monthly_sharing(df):
    monthly_sharing = df.resample(rule='M', on='dteday').agg({
        'cnt': "sum"
    })
    monthly_sharing = monthly_sharing.reset_index()
    monthly_sharing.rename(columns={
        'cnt': 'total_sharing'
    }, inplace=True)
    
    return monthly_sharing

# Helper function
def hourly_sharing(df):
    hourly_sharing = df.groupby('hr')['cnt'].sum().reset_index()

    return hourly_sharing

# Helper function
def user_comparison(df):
    comparison_data = df[['casual', 'registered']].sum().reset_index()
    comparison_data.columns = ['user_type', 'total_sharing']
    
    labels = comparison_data['user_type'].tolist()
    sizes = comparison_data['total_sharing'].tolist()
    
    return labels, sizes

all_df = pd.read_csv('dashboard/main_data.csv') 
datetime_columns = ["dteday"]

all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

# Create sidebar 
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Select Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
#filter on date (side bars)
filtered_df = all_df[(all_df["dteday"] >= pd.to_datetime(start_date)) & 
                     (all_df["dteday"] <= pd.to_datetime(end_date))]

# Create tabs
tab1, tab2, tab3 = st.tabs(["Trend", "High Sharing", "User Comparison"])

# Tab 1: Trend in the Number of Bike Sharing
with tab1:
    st.header('Trend in the Number of Bike Sharing ')
    monthly_data = monthly_sharing(filtered_df)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly_data, x='dteday', y='total_sharing', marker='o', ax=ax)
    ax.set_title('Total Bike Sharing per Month', fontsize=16)
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Sharing')
    
    st.pyplot(fig)
    st.caption("From the monthly analysis,the bike sharing increase at the beginning to middle of the year. It might caused by seasonal factors such a great weather situation (Clear, few clouds), spring and fall season. That's also supported by the high of number sharing in these time. The decreasing in the end of the year is also might caused by the winter season. People commonly rare using bike because the temperature that really not support to use bicycle. From that, the habit of people in sharing bike is so depend on the environment condition.")

# Tab 2: The Times when Bike Sharing are Highest
with tab2:
    st.header('The Times when Bike Sharing are Highest')
    hourly_data = hourly_sharing(filtered_df)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=hourly_data, x='hr', y='cnt', color='blue', ax=ax)
    ax.set_title('Total Bike Sharing by Hour of Day', fontsize=16)
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Total Sharing')
    
    st.pyplot(fig)
    st.caption("The peak of sharing around 5pm may reflect the need of users to go home from work, refreshing, or social activities. In this case, bicycle sharing is such a great solution on their leisure time. ")

# Tab 3: Comparison of Casual and Registered Users
with tab3:
    st.header("Proportion of Casual vs Registered Renters")
    
    labels, sizes = user_comparison(filtered_df)
    colors = ['blue', 'orange']
    explode = (0.1, 0) 

    # Create a pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)

    plt.title('Proportion of Casual vs Registered Renters', fontsize=16)
    plt.axis('equal')  

    st.pyplot(plt)
    st.caption("With 81.2% proportion for registered, this suggest that most people are more committed to the services, another option is that registered class may use bike more often.")



st.caption('Data Source: Bike Sharing Dataset\n https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset/data')
