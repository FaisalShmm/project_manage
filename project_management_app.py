from st_aggrid import AgGrid
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
from PIL import Image
import io
import os
# Todo: creating sidebar
st.set_page_config(page_title="Project_management",layout='wide')  # Choose wide mode as the default setting

# Add a logo (optional) in the sidebar
logo=Image.open(r'logo.jpg')
st.image(logo,width=220)
st.sidebar.image(logo,width=230)
st.sidebar.markdown("[Linkedin Account](https://www.linkedin.com/in/faisal-shamim-a49332241)")
# Add the expander to provide some information about the app
with st.sidebar.expander("About the App"):
    st.write("""
 	        This interactive project management App was built by Faisal Shamim using Streamlit. You can use the app to easily and quickly generate a Gannt chart for any project plan and management purposes. \n  \nYou can edit the project plan within the app and instantly generate and update the Gantt chart. You can also export the Gantt chart to png file and share it with your team very easily.)
 	     """)

# Create a user feedback section to collect comments and ratings from users
# set clear_on_submit=True so that the form will be reset/cleared once it's submitted
with st.sidebar.form(key='columns_in_form', clear_on_submit=True):
    st.write('Please help us improve!')
    # Make horizontal radio buttons
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;} </style>', unsafe_allow_html=True)
    # Use radio buttons for ratings
    rating = st.radio("Please rate the app",
                      ('1', '2', '3', '4', '5'), index=4)
    # Collect user feedback
    text = st.text_input(label='Please leave your feedback here')
    submitted = st.form_submit_button('Submit')
    if submitted:
        st.write('Thanks for your feedback!')
        st.markdown('Your Rating:')
        st.markdown(rating)
        st.markdown('Your Feedback:')
        st.markdown(text)
#! Creating the Main interface-section 1
st.markdown(''' <style>.font{
    font-size:30px ;font_family:'cooper Black';color:#FF9633;}
    </style>''', unsafe_allow_html=True)
st.markdown('<p class="font">UPLOAD YOUR PROJECT PLAN AND GET GANTT CHART INSTANTLY</p>',
            unsafe_allow_html=True)
# ?Add a template screenshot
st.subheader('Step 1:Download the project plan template'.upper())
temp = Image.open(r'template.png')
st.image(temp, caption='Make sure you use the same column name as in the template'.upper())

# ? Allow the user to download the template


@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


df = pd.read_csv(r'/home/faisal/Python_Projects/project_manage/template.csv')
csv = convert_df(df)
st.download_button(
    label="Download Template".upper(),
    data=csv,
    file_name='template.csv',
    mime='text/csv'
)
#! Creating the Main Interface-section 2
# Adding file uploader
st.subheader('Step 2:Upload your project plan file'.upper())

uploaded_file = st.file_uploader(
    "Fill out the project plan template and upload your file here.After you upload the file, you can edit your project plan  within the app.".upper(), type=['csv'])
if uploaded_file is not None:
    Tasks = pd.read_csv(uploaded_file)
    Tasks['Start'] = Tasks['Start'].astype('datetime64')
    Tasks['Finish'] = Tasks['Finish'].astype('datetime64')

    grid_response = AgGrid(
        Tasks,
        editable=True,
        height=300,
        width='100%',
    )
    updated = grid_response['data']
    df = pd.DataFrame(updated)


# Todo: Main interface section 2
    st.subheader('Step 3:Generate the Gantt Chart'.upper())

    Options = st.selectbox("View Gantt chart by:", [
                           'Teams','Completion Pct'],index=0)
    if st.button("Generate Gantt Chart".upper()):
      fig = px.timeline(
            df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color=Options,
            hover_name="Task Description"
        )
      fig.update_yaxes(autorange="reversed")

      fig.update_layout(
            title='Project Plan Gantt Chart',
            hoverlabel_bgcolor='#DAEEED',
            bargap=0.2,
            height=600,
            xaxis_title="",
            yaxis_title="",
            title_x=0.5,
            xaxis=dict(
                tickfont_size=15,
                tickangle=270,
                rangeslider_visible=True,
                side="top",
                showgrid=True,
                zeroline=True,
                showline=True,
                showticklabels=True,
                tickformat="%x\n",

            )
        )
      fig.update_xaxes(tickangle=0, tickfont=dict(
        family='Rockwell', color='blue', size=15))

      st.plotly_chart(fig, use_container_width=True)

      st.subheader(
        'Bonus:Export the interactive Gantt chart to HTML and share with your team'.upper())
      buffer = io.StringIO()
      fig.write_html(buffer, include_plotlyjs='cdn')
      html_bytes = buffer.getvalue().encode()
      st.download_button(
        label='Export to HTML'.upper(),
        data=html_bytes,
        file_name='Gantt.html',
        mime='text/html'
      )
    st.success("Thanks for using this app:)".upper())
else:
    st.warning('You need to upload a csv file'.upper())


st.markdown("Made with ❤️ by Faisal Shamim".upper())