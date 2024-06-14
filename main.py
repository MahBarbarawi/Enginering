#pip install tkinter

# GUI
import tkinter as tk
from tkinter import ttk

#math
import math


# convert from D,M,S to Decimal
def DeflectionAngle(degrees, minutes, seconds):
    decimal_deg = degrees + (minutes / 60) + (seconds / 3600)
    return decimal_deg


def TangetDestince(Radius, def_angel):
    return Radius * (math.tan(math.radians(def_angel) / 2))


def LongChord(Radius, def_angel):
    return Radius * 2 * math.sin(math.radians(def_angel) / 2)


def L(Radius, def_angel):
    return Radius * math.radians(def_angel)


def chainageT1(chI, Radius, def_angel):
    return chI - TangetDestince(Radius, def_angel)


def chainageT2(chI, Radius, def_angel):
    return chainageT1(chI, Radius, def_angel) + L(Radius, def_angel)


def thetaNote(Radius, def_angel):
    return (def_angel / 2) / L(Radius, def_angel)


def thetanote_to_dms(angle):
    degrees = int(angle)
    minutes = int((angle - degrees) * 60)
    seconds = float(((angle - degrees) * 60 - minutes) * 60)

    return str(degrees) + " degrees| " + str(minutes) + " min| " + str(seconds) + " sec"


def DeflictionAngleMethod(chI, Radius, def_angel):
    #Table
    table = {"point": list(), "Chainage": list(), "Subchord": list(), "Defliction Angle": list()}
    Alp = {}
    Thon = thetaNote(Radius, def_angel)
    # ----- T1
    table["point"].append("T1")
    Alp['T1'] = 0 # [] is the diffining the key value // T1 is the key // 0 is the value
    table["Subchord"].append("0")
    table["Defliction Angle"].append("0")
    val=chainageT1(chI, Radius, def_angel)
    table["Chainage"].append(val)
    # ------ 1
    table["point"].append("1")
    val = chainageT1(chI, Radius, def_angel)

    x = math.ceil(val / 5) * 5 # chainage point(1) 280
    table["Chainage"].append(x)
    c1 = x - chainageT1(chI, Radius, def_angel)
    table["Subchord"].append(c1)
    alpha1 = Thon * c1
    Alp['1'] = alpha1

    alpha1 = thetanote_to_dms(alpha1)
    table["Defliction Angle"].append(alpha1)

    # ---
    c = Radius / 20
    i = 0
    lis = list()
    ch = None
    while x + c * (i + 1) <= chainageT2(chI, Radius, def_angel):
        table['point'].append(i + 2)
        ch = x + c * (i + 1) # chainage point(i) 280 + C * ( i + 1 )
        table['Chainage'].append(ch)
        table['Subchord'].append(c)
        alpha1 = Thon * (c1 + c * (i + 1))
        lis.append(alpha1)
        alpha1 = thetanote_to_dms(alpha1)
        table["Defliction Angle"].append(alpha1)
        i += 1

    #     print(i,)
    leng = len(table["Defliction Angle"])

    if ch is None:
        ch = x
    else :
        # 10 || 0,1,2,3,....,9
        for num in range(i, leng + 1):
            Alp[str(num - 1)] = lis[num - 3] #alp["2"]..alp["3"]..alp["4"]..
    # point .. ..
    # t1..
    # 1
    # 2
    #

    #---- T2
    table['point'].append('T2')
    cht2 = chainageT2(chI, Radius, def_angel)
    table['Chainage'].append(cht2)
    #ch 295
    c2 = cht2 - ch
    table['Subchord'].append(c2)
    alpha1 = (c1 + i * c + c2) * Thon
    Alp['T2'] = alpha1

    alpha1 = thetanote_to_dms(alpha1)
    table["Defliction Angle"].append(alpha1)

    return table, Alp


def coordinatesMethod(xi, yi, azIT1, Radius, Alpha, decimal_deg):
    table = {"points": list(), "cordinates": list()}
    azt1i = azIT1 + 180
    if azt1i > 360:
        azt1i -= 360
    azIT1 = math.radians(azIT1)
    table['points'].append('T1')
    xt1 = xi + TangetDestince(Radius, decimal_deg) * math.sin(azIT1)
    yt1 = yi + TangetDestince(Radius, decimal_deg) * math.cos(azIT1)
    table['cordinates'].append((xt1, yt1))
    for i in list(Alpha.keys())[1:]:
        a = Alpha[i]
        table['points'].append(i)
        AZt1pi = (azt1i + a) * (math.pi / 180)

        t1pi = 2 * Radius * math.sin(a * (math.pi / 180))

        xpi = xt1 + t1pi * math.sin(AZt1pi)
        ypi = yt1 + t1pi * math.cos(AZt1pi)

        table['cordinates'].append((xpi, ypi))
    return table


def DeflictionAngleSubmit():
    insertValues = {}
    for val in ['degree' ,'minutes','seconds','ChainagePI','Radius','seconds']:
        if entries[val].get() =='':
            label.config(text=val+" is not provided")
            label.config(fg="red")
            return
        insertValues[val] = float(entries[val].get())


    decimal_deg = DeflectionAngle(insertValues['degree'], insertValues['minutes'], insertValues['seconds'])

    DefTable, Alpha = DeflictionAngleMethod(insertValues['ChainagePI'], insertValues['Radius'], decimal_deg)
    Elimants(insertValues['Radius'],decimal_deg)

    # Update the table with sorted values
    table.delete(*table.get_children())
    for i in range(len(DefTable['point'])):
        table.insert("", "end", values=(DefTable['point'][i], DefTable['Chainage'][i], DefTable['Subchord'][i],
                                        DefTable['Defliction Angle'][i]))


def coordinatesMethodSubmition():
    insertValues = {}

    for val in ListOFVal :
        if entries[val].get() == '':
            label.config(text=val + " is not provided")
            label.config(fg="red")
            return
        insertValues[val] = float(entries[val].get())



    decimal_deg = DeflectionAngle(insertValues['degree'], insertValues['minutes'], insertValues['seconds'])
    DefTable, Alpha = DeflictionAngleMethod(insertValues['ChainagePI'], insertValues['Radius'], decimal_deg)
    Elimants(insertValues['Radius'],decimal_deg)
    # Update the table with sorted values
    table.delete(*table.get_children())
    for i in range(len(DefTable['point'])):
        table.insert("", "end", values=(DefTable['point'][i], DefTable['Chainage'][i], DefTable['Subchord'][i],
                                        DefTable['Defliction Angle'][i]))



    table2.delete(*table2.get_children())
    CorTable = coordinatesMethod(insertValues['xi'], insertValues['yi'], insertValues['azmouthIT1'],
                                 insertValues['Radius'], Alpha, decimal_deg)
    for i in range(len(CorTable['points'])):# to know which row
        table2.insert("", "end", values=(CorTable['points'][i], CorTable['cordinates'][i][0], CorTable['cordinates'][i][1]))

def Elimants(Radians,degre):
    #
    Tanget.config(text="Tangent distance:"+str(TangetDestince(Radians,degre)))
    LongCh.config(text="Long Chord:"+str(LongChord(Radians,degre)))
    deg=(degre / 2) * (math.pi / 180)
    mi = Radians*(1-(math.cos(deg)))
    MiddleOrdinate.config(text='Middle Ordinate:'+str(mi))
    E= Radians*(1/math.cos(deg)-1)
    ExtendDistance.config(text='External Distance:'+str(E))




root = tk.Tk()
root.geometry("1920x1080")  # Adjust the width and height of the GUI
root.title("caculate Simple Circular curve")

label = tk.Label(root, text="")
label.pack()

# Elimants = tk.Button(root, text="Defliction Angle Method", command=Elimants)
# Elimants.pack(side='left', padx=10, pady=5)
Tanget = tk.Label(root, text="")
Tanget.pack(side='top', padx=10, pady=5,anchor='nw')
LongCh = tk.Label(root, text="")
LongCh.pack(side='top', padx=10, pady=5,anchor='nw')
MiddleOrdinate = tk.Label(root, text="")
MiddleOrdinate.pack(side='top', padx=10, pady=5,anchor='nw')
ExtendDistance = tk.Label(root, text="")
ExtendDistance.pack(side='top', padx=10, pady=5,anchor='nw')

Deflict = tk.Button(root, text="Defliction Angle Method", command=DeflictionAngleSubmit)
Deflict.pack(side='left', padx=10, pady=5,anchor='sw')

coordinates = tk.Button(root, text="coordinates Method", command=coordinatesMethodSubmition)
coordinates.pack(side='left', padx=10, pady=10,anchor='sw')


# input user
ListOFVal = ["degree", 'minutes', 'seconds', 'Radius', 'ChainagePI', 'azmouthIT1', 'xi', 'yi']
entries = dict()

frame = tk.Frame(root)
frame.pack(anchor='w', padx=10, pady=5)

label_degree = tk.Label(frame, text=ListOFVal[0])
label_degree.grid(row=0, column=0, sticky='w')

entry_degree = tk.Entry(frame)
entry_degree.grid(row=1, column=0, padx=5)
entries[ListOFVal[0]] = entry_degree

label_minutes = tk.Label(frame, text=ListOFVal[1])
label_minutes.grid(row=0, column=1, sticky='w')
entry_minutes = tk.Entry(frame)
entry_minutes.grid(row=1, column=1, padx=5)
entries[ListOFVal[1]] = entry_minutes

label_seconds = tk.Label(frame, text=ListOFVal[2])
label_seconds.grid(row=0, column=2, sticky='w')
entry_seconds = tk.Entry(frame)
entry_seconds.grid(row=1, column=2, padx=5)
entries[ListOFVal[2]] = entry_seconds

label_radius = tk.Label(frame, text=ListOFVal[3])
label_radius.grid(row=0, column=3, sticky='w')
entry_radius = tk.Entry(frame)
entry_radius.grid(row=1, column=3, padx=5)
entries[ListOFVal[3]] = entry_radius

label_chainage = tk.Label(frame, text=ListOFVal[4])
label_chainage.grid(row=0, column=4, sticky='w')
entry_chainage = tk.Entry(frame)
entry_chainage.grid(row=1, column=4, padx=5)
entries[ListOFVal[4]] = entry_chainage

label_azmouthIT1 = tk.Label(frame, text=ListOFVal[5])
label_azmouthIT1.grid(row=0, column=5, sticky='w')
entry_azmouthIT1 = tk.Entry(frame)
entry_azmouthIT1.grid(row=1, column=5, padx=5)
entries[ListOFVal[5]] = entry_azmouthIT1

label_xi = tk.Label(frame, text=ListOFVal[6])
label_xi.grid(row=0, column=6, sticky='w')
entry_xi = tk.Entry(frame)
entry_xi.grid(row=1, column=6, padx=5)
entries[ListOFVal[6]] = entry_xi

label_yi = tk.Label(frame, text=ListOFVal[7])
label_yi.grid(row=0, column=7, sticky='w')
entry_yi = tk.Entry(frame)
entry_yi.grid(row=1, column=7, padx=5)
entries[ListOFVal[7]] = entry_yi



# Create the table 1
table_frame = tk.Frame(root)
table_frame.pack(side='right', padx=10, pady=10, fill='both', expand=True)

table = ttk.Treeview(table_frame, show="headings", columns=("point", "ChainagePI","Subchord",'Defliction Angle'))
table.pack(side='right', fill='both', expand=True)

table.column("point", width=50, anchor='center')
table.column("ChainagePI", width=50, anchor='w')
table.column("Subchord", width=50, anchor='center')
table.column("Defliction Angle", width=50, anchor='w')

table.heading("point", text="point")
table.heading("ChainagePI", text="Chainage?")
table.heading("Subchord", text="Subchord")
table.heading("Defliction Angle", text="Defliction Angle")




# Create the table 2
table_frame = tk.Frame(root)
table_frame.pack(side='right', padx=10, pady=10, fill='both', expand=True)

table2 = ttk.Treeview(table_frame, show="headings", columns=("points", "cordinatesX", "cordinatesY"))
table2.pack(side='right', fill='both', expand=True)

table2.column("points", width=50, anchor='center')
table2.column("cordinatesX", width=100, anchor='w')
table2.column("cordinatesY", width=100, anchor='w')

table2.heading("points", text="points")
table2.heading("cordinatesX", text="cordinatesX")
table2.heading("cordinatesY", text="cordinatesY")


root.mainloop()
