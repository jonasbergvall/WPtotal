import streamlit as st
import pandas as pd
import plotly.express as px

# Ladda datamängden
df = pd.read_csv('data.csv')

# Konvertera datum-kolumnen till datetime-objekt
df['Date'] = pd.to_datetime(df['Date'])

# Ta bort timmar, minuter och sekunder från tidstämpeln
df['Date'] = df['Date'].dt.date


# Add custom title with font size and no frame
st.markdown('<h1 style="text-align: center; font-size: 28px; margin: 0; padding: 0; color: gray;">Our well-being</h1>', unsafe_allow_html=True)

# Add logo to the upper right corner
logo = '''
<div style="text-align: right;">
<img src="https://bestofworlds.se/img/BoWlogo.png" width="150px">
</div>
'''
st.markdown(logo, unsafe_allow_html=True)



# Add sidebar with date range selection
# Set min_value and max_value to the minimum and maximum dates in the DataFrame
with st.sidebar:
    st.markdown("# WhistlePeep")
    start_date = st.date_input('Start date', min_value=pd.Timestamp(df['Date'].min()), max_value=pd.Timestamp(df['Date'].max()), value=pd.Timestamp(df['Date'].min()))
    end_date = st.date_input('End date', min_value=pd.Timestamp(df['Date'].min()), max_value=pd.Timestamp(df['Date'].max()), value=pd.Timestamp(df['Date'].max()))

# Convert start_date and end_date to pandas datetime64 objects
start_date = pd.Timestamp(start_date).date()
end_date = pd.Timestamp(end_date).date()

# Filter data based on selected date range
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Definiera färgerna för varje kategori med önskad opacitet
colors = {
    'Better than OK': 'rgba(70, 130, 180, 1.0)',      # steelblue med opacitet 100%
    'OK': 'rgba(70, 130, 180, 0.75)',               # steelblue med opacitet 75%
    'Worse than OK': 'rgba(205, 16, 118, 0.75)',      # HotPink2 med opacitet 75%
    'Much worse than OK': 'rgba(205, 16, 118, 1.0)' # HotPink2 med opacitet 100%
}

# Skapa ett stapeldiagram med animation
fig = px.bar(
    filtered_df.melt(id_vars=['Date'], var_name='Number of people', value_name='Well-being'),
    x='Number of people', 
    y='Well-being',
    color='Number of people',
    animation_frame='Date',
    range_y=[0, 100],  # Konstant skala för y-axeln från 0 till 100
    height=600,  # Ställ in höjden på diagrammet
    color_discrete_map=colors  # Anpassa färgerna för varje kategori
)

# Uppdatera layouten för att ändra axelnamn
fig.update_layout(
    xaxis_title="Well-being",
    yaxis_title="Number of people"
)

# Visa diagrammet i Streamlit-appen
st.plotly_chart(fig)
