import streamlit as st
import  pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

import preprocesser, helper

df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')


df=preprocesser.preprocess(df, region_df)

usser_menu=st.sidebar.radio('Select an Option',
                 ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athelete wise Analysis')
                 )


st.dataframe(df)

if usser_menu=='Medal Tally':
    st.sidebar.header('Medall Tally')
    years, country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally=helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_country=='Overall' and selected_year=='Overall':
        st.title('Overall Tally')

    if selected_country!='Overall' and selected_year=='Overall':
        st.title('Medall Tall in'+str(selected_year))

    if selected_country=='Overall' and selected_year!='Overall':
        st.title(selected_country+ ' Overall Performance ')

    if selected_country != 'Overall' and selected_year != 'Overall':
        st.title(selected_country + ' Performance in '+str(selected_year)+' Olympics')
    st.table(medal_tally)

if usser_menu=='Overall Analysis':
    editions=df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athelete = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')
    col1, col2, col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)

    with col2:
        st.header('Cities')
        st.title(cities)

    with col3:
        st.header('Sport')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Atheletes')
        st.title(athelete)

    with col3:
        st.header('Nation')
        st.title(nations)

    nations_over_time=helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations over Time')
    st.plotly_chart(fig)

    evens_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(evens_over_time, x='Edition', y='Event')
    st.title('Events over Time')
    st.plotly_chart(fig)

    athelete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athelete_over_time, x='Edition', y='Name')
    st.title('Atheletes over Time')
    st.plotly_chart(fig)

    st.title('Number of Events over time(Every Sports)')
    fig, ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sx=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title('Most Successfull Athelets')
    sprot_list=df['Sport'].unique().tolist()
    sprot_list.sort()
    sprot_list.insert(0, 'Overall')

    select_sports=st.selectbox('Select Sport', sprot_list)
    x=helper.most_successful(df, select_sports)
    st.table(x)

if usser_menu=='Country Wise Analysis':

    st.sidebar.title('Country Wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('Select A Country', country_list)
    country_df=helper.year_wise_medal_tally(df,selected_country)
    fig=px.line(country_df, x='Year', y='Medal')
    st.title(selected_country, ' Medal Tally Over the Year')
    st.plotly_chart(fig)

    st.title(selected_country+ ' excels in the following Countries')
    pt=helper.country_events_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    top10df=helper.most_successful_countrywise(df,selected_country)
    st.title('Top ten atheletes of '+selected_country)
    st.table(top10df)

if usser_menu=='Athelete wise Analysis':
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medatlist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    # sprot_list = df['Sport'].unique().tolist()
    # sprot_list.sort()
    # sprot_list.insert(0, 'Overall')

    # select_sports=st.selectbox('Select a Sport', sprot_list)
    # temp_df=helper.weight_v_height(df, select_sports)
    # fig, ax=plt.subplots()
    # ax=sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=100)
    # st.title('Height vs Weight')
    # st.pyplot(fig)


    final=helper.man_v_women(df)

    fig=px.line(final, x='Year', y=['Male', 'Female'])
    st.title('Man vs Women Particiption over the Year')
    st.plotly_chart(fig)

