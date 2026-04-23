import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide', page_title='Startup Funding Analysis', page_icon=':bar_chart:')
df=pd.read_csv('cleaned_data.csv')
df['date']=pd.to_datetime(df['date'])
st.sidebar.title('Startup Funding Analysis')

def abtinvestor(investor):
    st.title(investor)
    #loading last 5 investments of the investors
    last_5=df[df['investors'].str.contains(investor)][['date','Startup Name','vertical','type','amount']]
    st.subheader('Most recent investments')
    st.dataframe(last_5)
    #top major investments of the investor
    col1,col2=st.columns(2)
    with col1:
        topinvest=df[df['investors'].str.contains(investor)].groupby('Startup Name')['amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Top investments')

        fig, ax = plt.subplots()
        ax.bar(topinvest.index, topinvest.values)
        ax.set_title("top investments")
        ax.set_xlabel("Startups")
        ax.set_ylabel("Investments") 
        st.pyplot(fig)
    with col2:
        ver=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Intrested in')
        fig1,ax1=plt.subplots()
        ax1.pie(ver,labels=ver.index,autopct='%0.01f%%')
        st.pyplot(fig1)    
    df['year']=df['date'].dt.year    
    dat=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    fig2,ax2=plt.subplots()
    ax2.plot(dat.index,dat.values)
    ax2.set_title('Investment over the years')
    ax2.set_xlabel('Years')
    ax2.set_ylabel('Investment')
    st.pyplot(fig2)

    
    #st.bar_chart(topinvest)
option=st.sidebar.selectbox('Select one',['Overall anaylsis','Startup','Investor'])
if option=='Overall anaylsis':
    st.title('Overall Analysis')
elif option=='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['Startup Name'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup')
    st.title('Startup Analysis')
else:
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor')
    if btn2:
        abtinvestor(selected_investor)

    
