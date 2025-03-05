import re
import pandas as pd


def save_to_excel(df, excel_path):
    df['КОЛ-ВО'] = df['КОЛ-ВО'].apply(lambda x: re.sub(r'[^0-9.,]', '', str(x)))
    df['КОЛ-ВО'] = df['КОЛ-ВО'].str.replace(',', '.', regex=False)
    df['КОЛ-ВО'] = pd.to_numeric(df['КОЛ-ВО'], errors='coerce').fillna(0)

    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        headers = ['ИДЕНТИФИКАТОР', 'ОПИСАНИЕ КОМПОНЕНТА', 'ИДЕНТ.КОД', 'КОЛ-ВО']
        df[headers].to_excel(writer, index=False, header=True)

        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            col_num = df.columns.get_loc('КОЛ-ВО')
            num_format = writer.book.add_format({'num_format': '#,##0.00'})
            worksheet.set_column(col_num, col_num, 15, num_format)

        for sheet in writer.sheets.values():
            for idx, col in enumerate(df.columns):
                series = df[col]
                max_width = max(series.astype(str).map(len).max(), len(col)) + 2
                sheet.set_column(idx, idx, max_width)

