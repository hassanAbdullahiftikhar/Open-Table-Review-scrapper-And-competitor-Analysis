import streamlit as st
import pandas as pd
import json
from datetime import datetime,timedelta
from webscrapper import scrap
from matplotlib import pyplot as plt
def competitor_analysis():
    st.write("# Competitor Analysis")
    st.write("## Dante&CO Performance Analysis")
    r=pd.read_excel("Reviewdata.xlsx")
    d=pd.DataFrame(r.loc[:,"Overall Rating":],dtype=int)
    Or=pd.DataFrame(d["Overall Rating"],dtype=int)
    Or=Or["Overall Rating"].value_counts()
    Or
    st.write("### Overall Rating Bar Graph")
    st.bar_chart(Or)
    d=st.date_input("Enter date")
    comp=st.text_input("Enter Competitor restaurant URL")
    
    if  comp and d:
        dates=[]
        ratings=[]
        scrap(comp,dates,ratings,5,d)
        over=ratings[::4]
        food=ratings[1::4]
        serv=ratings[2::4]
        amb=ratings[3::4]
        food=[int(i.split()[1])for i in food]
        over=[int(i.split()[1])for i in over]
        serv=[int(i.split()[1])for i in serv]
        amb=[int(i.split()[1])for i in amb]
        dates=dates[:len(food)]
        c1,c2=st.columns(2)
        # Subplot 1: Overall Ratings
        plt.plot(dates, over[0:len(dates)], label="Competitor OR")
        plt.plot(dates, r["Overall Rating"][0:len(dates)], label="Donato&Co Or")
        plt.xlabel("Date")
        plt.ylabel("Ratings")
        plt.title("Competitor  Ratings Analysis")
        plt.xticks(rotation=90, ha='right')
        plt.legend()
        st.pyplot(plt)
        with c1:
            fo = pd.DataFrame(food, columns=["Food Ratings"])
            foc = fo["Food Ratings"].value_counts().sort_index()
            st.write("## Competitor Food Ratings Distribution")
            st.bar_chart(foc)
            st.write("## Competitor Service Ratings Distribution")
            se=pd.DataFrame(serv,columns=["Service"])
            sec=se["Service"].value_counts().sort_index()
            st.bar_chart(sec)
            st.write("## Competitor Ambiance Ratings Distribution")
            am=pd.DataFrame(amb,columns=["Ambiance"])
            amc=am["Ambiance"].value_counts().sort_index()
            st.bar_chart(amc)
        with c2:
            st.write("## Dante&CO Food Ratings Distribution")
            dcf=r["Food"][0:len(dates)]
            dcf=pd.DataFrame(dcf,columns=["Food"])
            dcf=dcf["Food"].value_counts().sort_index()
            st.bar_chart(dcf)
            st.write("## Dante&CO Service Ratings Distribution")
            dcs=r["Service"][0:len(dates)]
            dcs=pd.DataFrame(dcs,columns=["Service"])
            dcs=dcs["Service"].value_counts().sort_index()
            st.bar_chart(dcs)
            st.write("## Dante&CO Ambiance Ratings Distribution")
            dca=r["Ambiance"][0:len(dates)]
            dca=pd.DataFrame(dca,columns=["Ambiance"])
            dca=dca["Ambiance"].value_counts().sort_index()
            st.bar_chart(dca)

        
def food():
    r=pd.read_excel("Reviewdata.xlsx")
    with open("food_reviews.json") as file:
        f=json.load(file)
    st.write("# Food Reviews")
    page = st.slider("Select Page",min_value=1,max_value=(len(f)+(len(f)%10)) // 10,value=1,step=1)
    start = (page - 1) * 10
    end = start + 10
    for i, fo in enumerate(f[start:end],start=start+1):
        st.markdown(f":red[{i}. {fo}] :green[Rating: {r["Food"][i-1]} Dined:{r["Date"][i-1]}]")
def service():
    st.write("# Service Reviews")
    r=pd.read_excel("Reviewdata.xlsx")
    with open("service_reviews.json") as file:
        f=json.load(file)
    page=st.slider("Select page",min_value=1,max_value=(len(f)+(len(f)%10)) // 10,step=1)
    start = (page - 1) * 10
    end = start + 10-1
    for i,fo in enumerate(f[start:end],start=start+1):
        st.markdown(f":blue[{i} {fo}] :green[ \nRating: {r["Service"][i-1]} Dined:{r["Date"][i-1]}]")
def overall():
    st.write("# Reviews")
    rdata=pd.read_excel("Reviewdata.xlsx")
    with open("food_reviews.json") as file:
        f=json.load(file)
    with open("service_reviews.json") as file:
        s=json.load(file)
    r=list(zip(f,s))
    page=st.slider("Select page",min_value=1,max_value=(len(f)+(len(f)%10)) // 10,step=1)
    start = (page - 1) * 10
    end = start + 10-1
    for i,(fo,se) in enumerate(r[start:end-1],start=start+1):
        st.markdown(f":blue[{i} {fo}] :red[{se}]\n:green[ Food Rating: {rdata["Food"][i-1]} service Rating: {rdata["Service"][i-1]} Overall Rating: {rdata["Overall Rating"][i-1]} Dined:{rdata["Date"][i-1]}]")
hamburger=st.sidebar.radio("Dante&Co Dashboard",["Food","Service","Overall Review","Competitor Analysis"])
if(hamburger=="Food"):
    food()
elif(hamburger=="Service"):
    service()

elif(hamburger=="Overall Review"):
    overall()
elif(hamburger=="Competitor Analysis"):
    competitor_analysis()