from tkinter import *
from tkinter import ttk
import requests as req
import matplotlib.pyplot as plt

pen = Tk()
pen.title("Covid-19 Statistics")
pen.resizable(False, False)

countrydata = req.get('https://api.covid19api.com/countries')
list1 = countrydata.json()
countries = []
for i in list1:
    countries.append(i["Country"])
countries.sort()
slugs = {}
for i in list1:
    slugs[i["Country"]] = i["Slug"]

totalgraphics = ["Active","Confirmed", "Death", "Recovered"]
dailygraphics = ["Daily Confirmed", "Daily Death", "Daily Recovered"]
grafslug = {"Confirmed":"confirmed", "Death":"deaths", "Recovered":"recovered",
            "Daily Confirmed":"confirmed", "Daily Death":"deaths", "Daily Recovered":"recovered"}

topfrm = Frame(pen)
topfrm.grid(row=0, column=0)

frm1 = LabelFrame(topfrm, text="By Country Total")
frm1.grid(row=0, column=0)
v = StringVar()
cmbbox1 = ttk.Combobox(frm1, textvariable=v)
cmbbox1["values"] = countries
cmbbox1.set("Select")
cmbbox1.grid(row=0, column=1)
lbl1 = Label(frm1, text="Country :")
lbl1.grid(row=0, column=0)
c = StringVar()
cmbbox2 = ttk.Combobox(frm1, textvariable=c)
cmbbox2["values"] = totalgraphics
cmbbox2.set("Select")
cmbbox2.grid(row=1, column=1)
lbl2 = Label(frm1, text="Graphic :")
lbl2.grid(row=1, column=0)

frm2 = LabelFrame(topfrm, text="By Country Daily")
frm2.grid(row=0, column=1)
z = StringVar()
cmbbox3 = ttk.Combobox(frm2, textvariable=z)
cmbbox3["values"] = countries
cmbbox3.set("Select")
cmbbox3.grid(row=0, column=1)
lbl3 = Label(frm2, text="Country :")
lbl3.grid(row=0, column=0)
d = StringVar()
cmbbox4 = ttk.Combobox(frm2, textvariable=d)
cmbbox4["values"] = dailygraphics
cmbbox4.set("Select")
cmbbox4.grid(row=1, column=1)
lbl4 = Label(frm2, text="Graphic :")
lbl4.grid(row=1, column=0)

frm3 = LabelFrame(pen, text="Global Top 15")
frm3.grid(row=1, column=0)
tableheadings = ["Country,Other", "Total Cases", "Total Deaths", "Total Recovered"]
globaltotal = []
sumdata = req.get('https://api.covid19api.com/summary')
sumlist = sumdata.json()
globaltotal.append("Global")
globaltotal.append(sumlist['Global']['TotalConfirmed'])
globaltotal.append(sumlist['Global']['TotalDeaths'])
globaltotal.append(sumlist['Global']['TotalRecovered'])

country_case = {}
for i in range(0,len(sumlist["Countries"])):
    country_case[sumlist["Countries"][i]["TotalConfirmed"]] = sumlist["Countries"][i]["Country"]
casekeylist = []
for i in country_case.keys():
    casekeylist.append(i)
for i in range(len(casekeylist)):
    max_idx = i
    for j in range(i + 1, len(casekeylist)):
        if casekeylist[max_idx] < casekeylist[j]:
            max_idx = j
    casekeylist[i], casekeylist[max_idx] = casekeylist[max_idx], casekeylist[i]

country_death = {}
for i in range(0,len(sumlist["Countries"])):
    country_death[sumlist["Countries"][i]["Country"]] = sumlist["Countries"][i]["TotalDeaths"]

country_rec = {}
for i in range(0,len(sumlist["Countries"])):
    country_rec[sumlist["Countries"][i]["Country"]] = sumlist["Countries"][i]["TotalRecovered"]

for row in range(17):
    for column in range(4):
        if row == 0:
            lbl5 = Label(frm3, text=tableheadings[column], bg="grey", fg="white", padx=3, pady=3)
            lbl5.grid(row=row, column=column, sticky="nsew" , padx=1, pady=1)
            frm3.grid_columnconfigure(column, weight=1)
        elif row == 1:
            lbl5 = Label(frm3,text=globaltotal[column], bg="darkgrey", fg="white", padx=3, pady=3)
            lbl5.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            frm3.grid_columnconfigure(column, weight=1)
        elif column == 0:
            lbl5 = Label(frm3, text="#{} ".format(row-1) + country_case[casekeylist[row-2]], bg="white", fg="blue", padx=3, pady=3)
            lbl5.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            frm3.grid_columnconfigure(column, weight=1)
        elif column == 1:
            lbl5 = Label(frm3, text=casekeylist[row-2], bg="white", fg="black", padx=3, pady=3)
            lbl5.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            frm3.grid_columnconfigure(column, weight=1)
        elif column == 2:
            lbl5 = Label(frm3, text=country_death[country_case[casekeylist[row-2]]], bg="white", fg="red", padx=3, pady=3)
            lbl5.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            frm3.grid_columnconfigure(column, weight=1)
        elif column == 3:
            lbl5 = Label(frm3, text=country_rec[country_case[casekeylist[row-2]]], bg="white", fg="green", padx=3, pady=3)
            lbl5.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            frm3.grid_columnconfigure(column, weight=1)

def GraphTotal():
    if cmbbox2.get() == totalgraphics[0]:
        day = []
        activecase = []
        recovery = []
        cfrmcase = []
        cfrmdata = req.get('https://api.covid19api.com/total/country/{}/status/confirmed'.format(slugs[cmbbox1.get()]))
        cfrmlist = cfrmdata.json()
        recvdata = req.get('https://api.covid19api.com/total/country/{}/status/recovered'.format(slugs[cmbbox1.get()]))
        recvlist = recvdata.json()
        for i in range(1, len(cfrmlist) + 1):
            day.append(i)
        for i in cfrmlist:
            cfrmcase.append(i["Cases"])
        for i in recvlist:
            recovery.append(i["Cases"])
        for i in range(0,len(recovery)):
            activecase.append(cfrmcase[i] - recovery[i])
        plt.title("{} {}".format(cmbbox1.get(), cmbbox2.get()))
        plt.plot(day, activecase)
        plt.xlabel("Day(22 Jan - Today)")
        plt.ylabel("Case")
        plt.show()

    else:
        countrydata = req.get('https://api.covid19api.com/total/country/{}/status/{}'.format(slugs[cmbbox1.get()],grafslug[cmbbox2.get()]))
        list2 = countrydata.json()
        day = []
        case = []
        for i in range(1, len(list2) + 1):
            day.append(i)
        for i in list2:
            case.append(i["Cases"])
        plt.title("{} {}".format(cmbbox1.get(), cmbbox2.get()))
        plt.plot(day, case)
        plt.xlabel("Day(22 Jan - Today)")
        plt.ylabel("Case")
        plt.show()

def GraphDaily():
    countrydata = req.get('https://api.covid19api.com/total/country/{}/status/{}'.format(slugs[cmbbox3.get()], grafslug[cmbbox4.get()]))
    list2 = countrydata.json()
    day = []
    case = []
    dailycase = []
    for i in range(1, len(list2)):
        day.append(i)
    for i in list2:
        case.append(i["Cases"])
    for i in range(0, len(case) - 1):
        dailycase.append(case[i + 1] - case[i])
    plt.title("{} {}".format(cmbbox3.get(), cmbbox4.get()))
    plt.bar(day,dailycase)
    plt.xlabel("Day(22 Jan - Today)")
    plt.ylabel("Case")
    plt.show()

btn1 = Button(frm1, text="Show", command=GraphTotal)
btn1.grid(row=2, column=1)
btn2 = Button(frm2, text="Show", command=GraphDaily)
btn2.grid(row=2, column=1)

pen.mainloop()
