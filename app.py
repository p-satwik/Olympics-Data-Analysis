import streamlit as st
import pandas as pd
import helper
import preprocessing
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff


df=pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessing.doprocess(df,region_df)
st.sidebar.image("https://logowik.com/content/uploads/images/1196-the-paris-2024summer-olympics-and-paralympics.jpg")
st.sidebar.header("Olympics Analysis")
user_menu = st.sidebar.radio('Select an Option',('Olympics in Numbers','Medal Tally','Countries','Athletes') )

if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in "+str(selected_year)+" Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performace over the years")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performace in the "+str(selected_year)+" Olympics")
    st.table(medal_tally)

if user_menu=='Olympics in Numbers':
    st.title("Top Statistics")
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)


    nationsovertime = helper.data_over_time(df,'region')
    fig = px.line(nationsovertime, x="Edition", y="Count")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    eventsovertime = helper.data_over_time(df,'Event')
    fig = px.line(eventsovertime, x="Edition", y="Count")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletesovertime = helper.data_over_time(df, 'Name')
    fig = px.line(athletesovertime, x="Edition", y="Count")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of events over time(All Sports)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    st.title("Most successful athletes")
    sports = df['Sport'].unique().tolist()
    sports.sort()
    sports.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sports)
    most_succ_table = helper.most_successful(df,selected_sport)
    st.table(most_succ_table)

if user_menu=='Countries':
    st.sidebar.title("Country-wise Analysis")
    years, country = helper.country_year_list(df)
    country.pop(0)

    selected_country = st.sidebar.selectbox('Select a Country', country)

    country_table = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_table, x="Year", y="Medal")
    st.title(selected_country + " - Performance over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu=='Athletes':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    st.title("Athletes distribution by Age")
    fig = sns.displot(data=athlete_df, x="Age", hue="Medal", kind="kde")
    st.pyplot(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']


    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x = temp_df['Weight'], y = temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
