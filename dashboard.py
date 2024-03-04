# memuat library yang dibutuhkan
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# membuat helper function
# menyiapkan bike_rent_df
def create_bike_rent_df(df):
    bike_rent_df = df.resample(rule='D', on='date_time').agg({
        "total_count": "sum"
    })
    bike_rent_df = bike_rent_df.reset_index()
    bike_rent_df.rename(columns={
        "total_count": "total_rent"
    }, inplace=True)
    return bike_rent_df

# menyiapkan casual_users_df
def create_casual_users_df(df):
    casual_users_df = df.casual.agg({
                "casual": "sum",
    })  
    casual_users_df = casual_users_df.reset_index()
    casual_users_df.rename(columns={
        "casual": "casual_users",
    }, inplace=True)
    return casual_users_df

# menyiapkan registered_users_df
def create_registered_users_df(df):
    registered_users_df = df.registered.agg({
                "registered": "sum",
    })  
    registered_users_df = registered_users_df.reset_index()
    registered_users_df.rename(columns={
        "registered": "registered_users",
    }, inplace=True)
    return registered_users_df

# menyiapkan users_percentage_df
def create_users_percentage_df(df):
    users_percentage_df = (df.casual.sum(), df.registered.sum())
    return users_percentage_df

# menyiapkan users_rent_df
def create_users_rent_df(df):
    df["date_time"] =  pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str))
    users_rent_df = df.groupby(by='date_time').agg({
                                'casual': 'sum',
                                'registered': 'sum'
                                })
    return users_rent_df

# menyiapkan weather_cond_df
def create_weather_cond_df(df):
    weather_cond_df = df.groupby(by="weather_condt").agg({
                        "total_count": "sum"
                        }).reset_index()
    return weather_cond_df

# menyiapkan season_df
def create_season_df(df):
    season_df = df.groupby(by="season").agg({
                        "total_count": "sum"
                        }).reset_index()
    return season_df

# menyiapkan season_daily_df
def create_season_daily_df(df):
    season_daily_df = df.groupby(by=[df.is_weekday.astype(str), df.season.astype(str)]).agg({
                        "total_count": "sum"
                        }).reset_index()
    return season_daily_df
                      
# menyiapkan season_hour_df
def create_season_hour_df(df):
    season_hour_df = df.groupby(by=[df['hour'], df['season']]).agg({
                        "total_count": "sum"
                        }).reset_index()
    return season_hour_df

# memuat dataset bike sharing
bike_df = pd.read_csv('bike_sharing_hour.csv')

# mengubah tipe data ke datetime
bike_df.reset_index(inplace=True)
bike_df['date_time'] = pd.to_datetime(bike_df['date_time'])

# membuat komponen filter 
# melakukan filter berdasarkan waktu
min_date = bike_df['date_time'].min()
max_date = bike_df['date_time'].max()

# mengambil start_date & end_date dari date_input
start_date, end_date = st.date_input(
    label='Time Interval',min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# menjalankan proses untuk membuat visualisasi data
main_df = bike_df[(bike_df['date_time'] >= str(start_date)) & 
                (bike_df['date_time'] <= str(end_date))]

# memanggil helper function
bike_rent_df = create_bike_rent_df(main_df)
casual_users_df = create_casual_users_df(main_df)
registered_users_df = create_registered_users_df(main_df)
users_percentage_df = create_users_percentage_df(main_df)
users_rent_df = create_users_rent_df(main_df)
weather_cond_df = create_weather_cond_df(main_df)
season_df = create_season_df(main_df)
season_daily_df = create_season_daily_df(main_df)
season_hour_df = create_season_hour_df(main_df)
 

#menambahkan header dashboard
st.header('Bike-Sharing Rental Dashboard:bicyclist:')

# menambahkan subheader
st.subheader('Total Bike Rent') 

# menampilkan informasi total sewa berdasarkan kategori penyewa
col1, col2, col3 = st.columns(3)

with col1:
    total_rent = f"{bike_rent_df.total_rent.sum():,.0f}"
    st.metric("Total Rent", value=total_rent)

with col2:
    registered_users = f"{registered_users_df.registered_users.sum():,.0f}"
    st.metric("Total Registered Users", value=registered_users)

with col3:
    casual_users = f"{casual_users_df.casual_users.sum():,.0f}"
    st.metric("Total Non-registered Users", value=casual_users)

# mengaturkonteks dan gaya plot
sns.set_style('whitegrid')
sns.set_context('paper')

# menambahkan color palette
color_pal = ['#F24C00', '#F68E5F', '#F5DD90', '#485696']

# membuat kolom
col1, col2 = st.columns(2)

with col1:
    # menampilkan pie chart persentase penyewa
    fig, ax = plt.subplots()
    ax.pie(data=users_percentage_df,
        x=(casual_users_df.casual_users.sum(), registered_users_df.registered_users.sum()),
        labels=('Non-registered Users', 'Registered Users'),
        autopct='%1.2f%%',
        colors=('#485696', '#F24C00'),
        explode=(0.1, 0)
    )
    ax.set_title("Bike Rent Percentage by Users", size=15)
    st.pyplot(fig)

with col2:
    # menampilkan line chart tren sewa sepeda berdasarkan kategori penyewa
    main_df['date_time'] = pd.to_datetime(main_df['year'].astype(str) + '-' + main_df['month'].astype(str))
    monthly_rentals = main_df.groupby(by='date_time').agg({
        'casual': ['sum'],
        'registered': ['sum']
    })

    fig, ax = plt.subplots()
    ax.plot(monthly_rentals.index.date, monthly_rentals['casual'], label='Non-registered Users', color='red')
    ax.plot(monthly_rentals.index.date, monthly_rentals['registered'], label='Registered Users', color='orange')
    ax.set_title('Trend of Total Bike Rent by Users', size=15)
    ax.set_xlabel('Time', size=15)
    ax.set_ylabel('Total Rent', size=15)
    ax.legend()
    st.pyplot(fig)

# menambahkan subheader 
st.subheader('Total Bike Rent by Weather Condition')

# menampilkan bar chart total sewa berdasarkan kategori kondisi cuaca
fig, ax = plt.subplots(figsize=(7,3))
sns.barplot(data=weather_cond_df,
            x='weather_condt',
            y='total_count',
            palette=color_pal,
            ax=ax
)
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Total Rent")
ax.tick_params(axis='x')
ax.tick_params(axis='y')
st.pyplot(fig)

# menambahkan subheader
st.subheader('Total Bike Rent by Season')

# menampilkan bar chart total sewa berdasarkan kategori musim
fig, ax = plt.subplots(figsize=(7,3))
sns.barplot(data=season_df,
            x='season',
            y='total_count',
            palette=color_pal,
            ax=ax
)
ax.set_xlabel("Season")
ax.set_ylabel("Total Rent")
ax.tick_params(axis='x')
ax.tick_params(axis='y')
st.pyplot(fig)

#membuat kolom
col1, col2 = st.columns(2)

with col1:
    # menampilkan bar chart total sewa harian berdasarkan kategori musim
    fig, ax = plt.subplots()
    sns.barplot(data=season_daily_df,
                x='is_weekday',
                y='total_count',
                hue='season',
                palette=color_pal,
                ax=ax
    )
    ax.set_title("Total of Daily Bike Rent by Season", loc="center", fontsize=15)
    ax.set_xlabel("Day in a Week")
    ax.set_ylabel("Total Rent")
    ax.tick_params(axis='x')
    ax.tick_params(axis='y')
    st.pyplot(fig)

with col2:
    # menampilkan line chart total sewa per jam berdasarkan kategori musim
    fig, ax = plt.subplots()
    sns.pointplot(data=season_hour_df,
                  x='hour',
                  y='total_count',
                  hue='season',
                  palette=color_pal,
                  ax=ax
    )
    ax.set_title('Total Bike Rent per Hour by Season', size=15)
    ax.set_xlabel('Hour in a Day')
    ax.set_ylabel('Total Rent')
    st.pyplot(fig)

# membuat subheader
st.subheader('Correlation of Environments Condition vs Total Bike Rent')

# membuat kolom
col1, col2, col3 = st.columns(3)

with col1:
    # menampilkan scatterplot hubungan antara temperatur dengan total sewa
    fig,ax = plt.subplots() 
    plt.scatter(main_df['temp'], main_df['registered'], label='Registered Users', color='#F24C00')
    plt.scatter(main_df['temp'], main_df['casual'], label='Non-registered Users', color='#485696')
    plt.title('Temperature vs Total Rent', size=15)
    plt.xlabel('Temperature')
    plt.ylabel('Total Rent')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig)

with col2:
    # menampilkan scatterplot hubungan antara kelembapan udara dengan total sewa
    fig,ax = plt.subplots()
    plt.scatter(main_df['humid'], main_df['registered'], label='Registered Users', color='#F68E5F')
    plt.scatter(main_df['humid'], main_df['casual'], label='Non-registered Users', color='#485696')
    plt.title('Humidity vs Total Rent', size=15)
    plt.xlabel('Humidity')
    plt.ylabel('Total Rent')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig)

with col3:
    # menampilkan scatterplot hubungan antara kecepatan angin dengan total sewa
    fig,ax = plt.subplots()
    plt.scatter(main_df['wind_speed'], main_df['registered'], label='Registered Users', color='#F5DD90')
    plt.scatter(main_df['wind_speed'], main_df['casual'], label='Non-registered Users', color='#485696')
    plt.title('Wind Speed vs Total Rent', size=15)
    plt.xlabel('Wind Speed')
    plt.ylabel('Total Rent')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig)

# menampilkan heatmap korelasi antara semua variabel kondisi lingkungan terhadap total sewa
fig, ax = plt.subplots(figsize=(8,5))
corr = main_df[['temp', 'humid', 'wind_speed', 'total_count']].corr()
corr_renamed = corr.rename(columns={'temp': 'Temperature',
                                    'humid': 'Humidity',
                                    'wind_speed': 'Wind Speed',
                                    'total_count': 'Total Rent'}, 
                            index={'temp': 'Temperature',
                                   'humid': 'Humidity',
                                   'wind_speed': 'Wind Speed',
                                   'total_count': 'Total Rent'
})
sns.heatmap(data=corr_renamed, annot=True, cmap='RdYlBu', fmt=".2f", annot_kws={"size": 12})
ax.set_title('Environment Conditions vs Total Rent', size=15)
ax.set_xlabel('Environment Conditions')
ax.set_ylabel('Environment Conditions')
ax.tick_params(axis='x')
ax.tick_params(axis='y')
st.pyplot(fig)

# membuat caption copyright
st.caption('Copyright (c) Pinasthika Sekar Wintang 2024')