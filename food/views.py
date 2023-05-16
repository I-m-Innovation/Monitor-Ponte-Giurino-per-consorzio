# food/views.py
from django.shortcuts import render, redirect
# from ftplib import FTP
# from django.shortcuts import render
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from num2string_001 import convertNumber
from .FTPLogIn import FTPLogIn

# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64

def uploadData():

    ftp = FTPLogIn()
#
    # try:
    #     ftp = FTP("192.168.10.211", timeout=120)
    #     # ftp = FTP("93.33.192.68", timeout=120)
    # except:
    #     ftp = FTP("93.33.192.68", timeout=120)
    #
    # ftp.login('ftpdaticentzilio', 'Sd2PqAS.We8zBK')
    # ftp.cwd('/dati/ponte_giurino')

    ftp.cwd('/dati/ponte_giurino')

    gFile = open('PGDailyPlot.csv', "wb")
    ftp.retrbinary('RETR PGDailyPlot.csv', gFile.write)
    gFile.close()

    Data = pd.read_csv("PGDailyPlot.csv")
    # Data = 0
    return Data


def index2(request):
    stepcount = [
        {"y": 10560, "label": "Sunday"},
        {"y": 9060, "label": "Monday"},
        {"y": 6650, "label": "Tuesday"},
        {"y": 8305, "label": "Wednesday"},
        {"y": 8531, "label": "Thursday"},
        {"y": 10150, "label": "Friday"},
        {"y": 8921, "label": "Saturday"}
    ]

    return render(request, 'index2.html', {"stepcount": stepcount})

def index(request):

    Data = uploadData()

    P = Data["P"]
    PMax = max(P)
    PMin = min(P)
    lastP = P[len(P)-1]
    lastPString, dummy = convertNumber(lastP,"Power","HTML")

    Q = Data["Q"]
    QMax = max(Q)
    QMin = min(Q)
    lastQ = Q[len(Q)-1]
    lastQString, dummy = convertNumber(lastQ,"Charge","HTML")

    time = Data["t"]
    lastT = time[len(time)-1]
    if lastP>0:

        StatoTurbina = "In produzione!"

    elif lastP == 0:

        StatoTurbina = "Ferma!"


    fig = px.line(Data, x="t", y="P")
    fig.update_yaxes(range=[0, 235.39])

    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig2 = px.line(Data, x="t", y="Q")
    fig2.update_yaxes(range=[0, 70])
    fig2.update_traces(yaxis="y2")

    # subfig = fig.data + fig2.data
    subfig.add_traces(fig.data + fig2.data)
    # subfig.add_traces(fig.data + fig2.data)
    subfig.layout.xaxis.title = ""
    subfig.layout.yaxis.title = "Potenza [kW]"
    subfig.layout.yaxis.color = "red"
    subfig.layout.yaxis2.title = "Portata [l/s]"
    subfig.layout.yaxis2.color = "blue"
    subfig.update_layout({'yaxis':{'range': [min(0,PMin), max(235.39,PMax)]}})
    subfig.update_layout({'yaxis2':{'range': [min(0,QMin), max(80,QMax)]}})

    subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
    subfig.update_layout(height=600, width=800)
    # subfig.update_layout(showlegend=True)

    # t = pd.to_datetime(Data["t"])
    # Q = Data["Q"]
    # #
    #
    # Data.plot(kind='scatter', x='t', y='P')

    # fig, ax = plt.subplots()
    #
    # ax.plot(t, Q, lw=1.5, label="Potenza [kW]", color="red")

    # buffer = BytesIO()
    A=subfig.to_html('graph.html')
    # buffer.seek(0)
    # image_png = buffer.getvalue()
    # buffer.close()

    # graphic = base64.b64encode(image_png)
    # graphic = graphic.decode('utf-8')

    Data = {"Grafico": A, "StatoTurbina": StatoTurbina, "lastT": str(lastT), "lastQ": lastQString, "lastP": lastPString}

    # return render(request, 'index.html', {'graphic': graphic})
    return render(request, 'index3.html', context=Data)

# Create your views here.
