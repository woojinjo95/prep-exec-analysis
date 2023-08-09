import pandas as pd
from process import process_dumpsys_meminfo

summary_column_names = ('timestamp', 'Total_RAM', 'Free_RAM', 'Used_RAM', 'Lost_RAM')
detail_column_names = ('timestamp', 'section', 'adj', 'adj_pss', 'category', 'process', 'pid', 'pss')


def create_dumpsys_meminfo_summary_df():
    df = pd.DataFrame({key: [] for key in summary_column_names})
    return df


def create_dumpsys_meminfo_detail_df():
    df = pd.DataFrame({key: [] for key in detail_column_names})
    return df


def convert_mem_value(key, value):
    if key in ['Total_RAM', 'Free_RAM', 'Used_RAM', 'Lost_RAM', 'adj_pss', 'pss'] and type(value) == str:
        return value.replace(',', '')
    else:
        return value


def dumpsys_meminfo_df_from_rawfile(raw_file_path):
    with open(raw_file_path, 'r', encoding='utf-8') as dumpsys_meminfo_log_file:
        summary_list, detail_list = process_dumpsys_meminfo(
            dumpsys_meminfo_log_file)
    # summary_list, detail_list 비어있지 않을 때!
    if summary_list and detail_list:
        return (
            pd.DataFrame([{key: convert_mem_value(key, value) for key, value in summary.items()}
                         for summary in summary_list]),
            pd.DataFrame([{key: convert_mem_value(key, value) for key, value in detail.items()}
                         for detail in detail_list]),
        )
    # summary_list, detail_list 비어있으면 빈 dataframe return
    else:
        return create_dumpsys_meminfo_summary_df(), create_dumpsys_meminfo_detail_df()
