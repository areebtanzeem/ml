import gspread
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.graph_objects as go
import time
import tkinter as tk
import os
import plotly.io as pio
from PIL import ImageTk
from PIL import Image


#pio.kaleido.scope.default_height = 800
pio.kaleido.scope.default_width = 2000
pio.kaleido.scope.default_scale = 2

if not os.path.exists("images"):
    os.mkdir("images")

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('1024x800')
        self.title('Data')
        first_label = tk.Label(self, text="Please Enter your input here", font=10)
        first_label.pack(pady=2, padx=2)
               
        Application.first_entry = tk.Entry(self, width=50)
        Application.first_entry.pack(padx=15, pady=15)
        first_button = tk.Button(
            self, text="Submit", command=get_data)
        first_button.pack(pady=10, padx=10) 


#LithiumFoil


def get_data():
    filename = Application.first_entry.get()
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", scope)
    client = gspread.authorize(creds)

    lithium_sheet = client.open("StorTera").worksheet("LithiumSheet")
    df_lithium_sheet = pd.DataFrame(lithium_sheet.get_all_records())
    vendor_sheet = client.open("StorTera").worksheet("Vendor")
    df_vendor_sheet = pd.DataFrame(vendor_sheet.get_all_records())

    df_all_materials = df_lithium_sheet[df_lithium_sheet["Type"] == filename]
    # df_all_materials.to_csv("file.csv",index=False)

    #####################################################
    # Removing white spaces
    #####################################################
    df_all_materials = df_all_materials.rename(
        columns={'Quantity ': 'Quantity'})
    df_all_materials = df_all_materials.rename(
        columns={'Chemical Purity': 'Chemical_Purity'})
    df_all_materials = df_all_materials.rename(
        columns={'Chemical Price (G/L/m2) £': 'Chemical_Price_G_L_m2_euro'})
    df_all_materials = df_all_materials.rename(
        columns={'Total Chemical Price': 'Total_Chemical_Price'})
    df_all_materials = df_all_materials.rename(
        columns={'Price per Unit (£/mm2)': 'Price_per_Unit_euro_divided_by_mm2'})
    df_all_materials = df_all_materials.rename(
        columns={'Delivery Cost £': 'Delivery_Cost_euro'})
    df_all_materials = df_all_materials.rename(columns={'VAT £': 'VAT_euro'})
    df_all_materials = df_all_materials.rename(
        columns={'Extra Cost': 'Extra_Cost'})
    print(df_all_materials.columns)

    df_vendor_company = df_vendor_sheet[df_vendor_sheet["company"].isin(
        df_all_materials["company"])]
    layout = go.Layout( autosize=True, margin={'l': 0, 'r': 0, 't': 20, 'b': 0})
    print(df_vendor_company.columns)
    fig = go.Figure(layout=layout, data=[go.Table(
        columnorder = [1,2,3,4,5,6,7,8,9,10,11,12,13,14],
        columnwidth = [80,80,80,80,80,120,240,160,280,80,160,80,80,80],
        header=dict(values=list(df_all_materials.columns),
                    fill_color='green',
                    font=dict(color='white', size=15),
                    align='left'),
        cells=dict(values=[df_all_materials.Quantity, df_all_materials.SIZE, df_all_materials.Thickness, df_all_materials.Units, df_all_materials.Pieces, df_all_materials.Chemical_Purity, df_all_materials.Chemical_Price_G_L_m2_euro, df_all_materials.Total_Chemical_Price, df_all_materials.Price_per_Unit_euro_divided_by_mm2, df_all_materials.company, df_all_materials.Delivery_Cost_euro, df_all_materials.VAT_euro, df_all_materials.Extra_Cost, df_all_materials.Type], fill_color='lightgrey',font=dict(color='black', size=12), align='left'))])

    fig2 = go.Figure(layout=layout, data=[go.Table(
        columnorder = [1,2],
        columnwidth = [80,1200],
        header=dict(values=list(df_vendor_company.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_vendor_company.company, df_vendor_company.website],
                   fill_color='lavender',
                   align='left'))
    ])
    
    if os.path.exists(f"images/{filename}.svg"):
        os.remove(f"images/{filename}.svg")
    
    
    if os.path.exists(f"images/{filename}_company.svg"):
        os.remove(f"images/{filename}_company.svg")


    fig2.write_image(f"images/{filename}.svg")
    fig.write_image(f"images/{filename}_company.svg")
    open_img(f"images/{filename}_company.svg")
    open_img(f"images/{filename}.svg")

def open_img(filename):
    #x = openfn()
    img = Image.open(filename)
    #img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(app, image=img)
    panel.image = img
    panel.pack()


app = Application()
app.mainloop()