import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid,GridOptionsBuilder


st.title("The Payoff")
st.markdown("Himanshu & Team - Group 6")
####################### Calls #######################
stock = st.number_input('Price of stock (Long):')


#############################################
calls= st.selectbox("Number of Calls: ", [1,2,3],key='1')
data=[]
df = pd.DataFrame(data,columns=['Call No.','Long/Short', "Call price", "Strike Price"])
df['Call No.']=[(i+1) for i in range(calls)]
df['Call price']=[0 for i in range(calls)]
df['Strike Price']=[0 for i in range(calls)]
grid_return=AgGrid(df,editable=True)
df = grid_return['data']
######################## Puts ######################
puts= st.selectbox("Number of Puts: ", [1,2,3],key='2')
data1=[]
df1 = pd.DataFrame(data1,columns=['Put No.','Long/Short', "Put price", "Strike Price"])
df1['Put No.']=[(i+1) for i in range(puts)]
df1['Put price']=[0 for i in range(puts)]
df1['Strike Price']=[0 for i in range(puts)]
grid_return1=AgGrid(df1,editable=True)
df1 = grid_return1['data']

###################### Computation ########################

def called(new_df,calls,number):
    val=[]
    for i in range(calls):
        if new_df['Long/Short'][i] == 'Long':
            val.append((max((number - float(new_df['Strike Price'][i])),0) - float(new_df['Call price'][i])))
        elif new_df['Long/Short'][i] == 'Short':
            val.append((min((float(new_df['Strike Price'][i]) - number),0) + float(new_df['Call price'][i])))            
    return sum(val) 

def putted(new_df1,puts,number):
        val1=[]
        for i in range(puts):
            if new_df1['Long/Short'][i] == 'Long':
                val1.append((max((float(new_df1['Strike Price'][i])-number),0) - float(new_df1['Put price'][i])))
            elif new_df1['Long/Short'][i] == 'Short':
                val1.append((min(number-float(new_df1['Strike Price'][i]),0) + float(new_df1['Put price'][i])))        
        return sum(val1)
                          
def payoff(new_df,new_df1,calls,puts,number):
    try:
        return called(new_df,calls,number) + putted(new_df1,puts,number) + (number - stock)
    except ValueError:
        return None
    
st.markdown("""
<style>
div[data-testid="metric-container"] {
   border: 1px solid rgba(28, 131, 225, 0.1);
   margin-top:10px;
   padding: 5% 5% 0% 15%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   margin-top:-10px;
   white-space: break-spaces;
   color: rgb(49, 51, 63);
   font-size:25px;
   font-weight: 600;
   line-height: 250%;
}
</style>
"""
, unsafe_allow_html=True)

###################################### output display
col1, col2 = st.columns([2,2],gap='large')
with col1:
    st.markdown("### Current Price")
    number = st.number_input('')
with col2:
    st.metric(label="Payoff", value=payoff(df,df1,calls,puts,number), delta="")


st.markdown("""
<style>
div[data-testid="stMarkdownContainer"]> label[class="css-1offfwp e16nr0p33"] {
   font-weight:bold;
   position:relative;
   top:-160px;
   left:-200px;
   color: grey;
   overflow-wrap: break-word;
}
</style>
"""
, unsafe_allow_html=True)

st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.write('\n')
st.header("Payoff of the strategy")

n=int((max(max(list(map(int, df1['Strike Price']))), max(list(map(int, df['Strike Price']))))+100)/0.5)
x=[(0+i*0.5) for i in range(n)]
y=[]
for i in range(n):   
    y.append(payoff(df,df1,calls,puts,x[i]))
 
output = pd.DataFrame(list(zip(x,y)), columns=["Current Price", "Payoff"])
fig = px.scatter(output,x="Current Price", y="Payoff")
st.plotly_chart(fig, use_container_width=True)
