#!/usr/bin/python3
# pricebook.py by daveyblade
# Grabs and displays the pricebook bids from quadrigacx
# Also saves last GET in a txt file
#
# This was written by an amateur coder and should in no way be considered
# a tool for sound financial advice.

import requests, json, os
from datetime import datetime
from tkinter import *
from tkinter import ttk


class Feedback:

    def __init__(self, master):

        master.title('Pricebook v1.0 Alpha')

        #variables
        path = "./pricebook.txt"

        lastReport = []
        #Gotta default to something dont we
        exchangeType = 'bch_btc'
        exchangeMaj = 'bch'
        exchangeMin = 'btc'

        self.main_frame = ttk.Frame(master)
        self.main_frame.pack()

        #combobox
        exchangevar = StringVar()
        self.exchangebox = ttk.Combobox(self.main_frame, textvariable = exchangevar)
        self.exchangebox.config(values = ('btc_cad', 'btc_usd', 'eth_cad', 'eth_btc', 'ltc_cad', 'ltc_btc', 'bch_cad', 'bch_btc', 'btg_cad', 'btg_btc'))
        self.exchangebox.grid(row = 3, column = 1)
        self.exchangebox.bind('<<ComboboxSelected>>', lambda e: setExchange(exchangevar.get()))


        #labels
        self.labelMain = ttk.Label(self.main_frame, text = "Pricebook Quad Alpha v 0.1").grid(row = 0, column = 0, columnspan = 2)
        self.labelMaj = ttk.Label(self.main_frame)
        self.labelMin = ttk.Label(self.main_frame)
        self.labelMaj.config(text = exchangeMaj)
        self.labelMin.config(text = exchangeMin)
        self.labelMaj.grid(row = 1, column = 0)
        self.labelMin.grid(row = 1, column = 1)
        self.displaypricemajor = Text(self.main_frame, width = 12, height = 10)
        self.displaypricemajor.grid(row = 2, column = 0)
        self.displaypriceminor = Text(self.main_frame, width = 12, height = 10)
        self.displaypriceminor.grid(row = 2, column = 1)

        self.button = ttk.Button(self.main_frame, text = "Get Pricebook", command = lambda: quadData())
        self.button.grid(row = 3, column = 0)






        def setExchange(exstr):
            exchangeType = exstr
            exchangeMaj, exchangeMin = exstr.split('_')
            self.labelMaj.config(text = exchangeMaj)
            self.labelMin.config(text = exchangeMin)
            quadData()



        #Grab data from quadrigacx
        def quadData():

            response = json.loads(requests.get("https://api.quadrigacx.com/v2/order_book?book="+exchangeType).text)
            lastReport = response['bids']
            thefile = open(path, 'w')
            for i in range(len(lastReport)):
                #Debug: print(lastReport[i])
                self.displaypricemajor.replace(str(i)+'.0', str(i)+'.0 lineend', str(lastReport[i][0]) + "\n")
                self.displaypriceminor.replace(str(i)+'.0', str(i)+'.0 lineend', str(lastReport[i][1]) + "\n")

            with thefile as out:
                out.write(str(lastReport))
            thefile.close()




def main():
    root = Tk()
    root.option_add('*tearoff', False)




    feedback = Feedback(root)
    root.mainloop()


if __name__ == "__main__": main()
