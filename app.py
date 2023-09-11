import pandas as pd
import re
import streamlit as st

st.write("""
<style>
    html, body, [class*="css"]  {
    }
    h3 {
        color: #4267B2;
        margin-bottom: 24px;
    }
    h5 {
        margin-bottom: 12px;
    }
    .date_selected {
        color: #4267B2;
    }
    
</style>
""", unsafe_allow_html=True)

SAMPLE_NAME = 'Sample Name'
GENE_NAME = 'Gene Name'
POSITION = 'Position'
CQ = 'Cq'
TM = 'TM1 (°C)'
GROUP = 'Group'
TEST_NAME = "Test Name"
SAMPLE_TUBE_ID = "SampleTubeID"
SAMPLE_TUBE_POSITION_ID = "SampleTubePositionID"
COMMENTS = 'Comments'

def sortDataFrameBy(df, col):
    df['sorted'] = [ord(i[0])*100+int(re.search(r'(\d+)(?!.*\d)',i).group(0)) for i in df[col]]
    df.sort_values(by='sorted',ascending=True, inplace=True)
    df.drop('sorted', axis=1, inplace=True)

    return df

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

files_path = None
mask = []

with st.sidebar:
    st.header('EntoExplorer')
    files = st.file_uploader("Choose your Files", type=["xls","xlsx","txt"], accept_multiple_files=True)

st.markdown("<h3>Ento Explorer App 🐜</h3>", unsafe_allow_html=True)


if files is not None:
    txt_files = []
    excel_files = []
    txt_names = []
    df_combined = pd.DataFrame()
    df_txt = pd.DataFrame()
    df_excel = pd.DataFrame()
    is_empty = True

    for file in files:
        if '.txt' in file.name: 
            txt_files.append(file)
            txt_names.append(file.name)
    

    unique_txt = set(txt_names)
    count_unique_txt = len(unique_txt)
    df = pd.DataFrame()

    if (len(txt_files) == 3) & (len(txt_files) == count_unique_txt):
        df1 = pd.read_csv(txt_files[0], delimiter = '\t')
        df2 = pd.read_csv(txt_files[1], delimiter = '\t')
        df3 = pd.read_csv(txt_files[2], delimiter = '\t')
       
        
        df = df1.merge((df2.merge(df3, on = POSITION)), on = POSITION)
  
        is_empty = False

       
      
       
 

    else:
        st.info(f"""
            Hi, dear user !\n
            You need to upload these 3 files in 'txt' format:
              - High Resolution Melting.txt
              - Quality_detection.txt
              - TM_calling.txt
        """, icon='🤖')

        st.markdown(f"""
            <p><i>Valid upload ({count_unique_txt}/3)<br> 
                {"" if count_unique_txt == 0 else unique_txt}</i></p>
            """, unsafe_allow_html=True)

       
    if is_empty is False:
        df.rename(columns={
            GENE_NAME: TEST_NAME,
            SAMPLE_NAME: SAMPLE_TUBE_ID,
            POSITION: SAMPLE_TUBE_POSITION_ID}, inplace=True)

        mask = [TEST_NAME, SAMPLE_TUBE_POSITION_ID, SAMPLE_TUBE_ID, GROUP, CQ, TM]

        df = df[mask].fillna('')
        
        df_final = sortDataFrameBy(df, SAMPLE_TUBE_POSITION_ID)

        st.markdown("<h5>&#128196; Data</h5>", unsafe_allow_html=True)
        st.dataframe(df_final.reset_index(drop=True))

        csv = convert_df(df)

        st.download_button(
            label="📥 Download Table",
            data=csv,
            file_name='data_combined.csv',
            mime='text/csv',
        )
