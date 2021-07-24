from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange
from pythonping import ping
import pandas as pd
import io

MAX_TIME_FOR_PING_TIMEOUT_IN_SECONDS = 1
GRAPH_WINDOW_IN_DATAPOINT = 60
GRAPH_UPDATE_INTERVAL_IN_MILLISECONDS = 1000

pyplot.style.use('dark_background')
figure = pyplot.figure()
ax = figure.add_subplot(1,1,1)
ax.ylabel = "Latency (ms)"

# Replace Keys with your address
# RUN ipconfig/AP configurations to check your interface addresses
#Example
# host_names = {"192.168.0.101":"Self", "192.168.0.1":"Wi-Fi router", "x.x.x.x":"ISP Gateway", "google.com":"Google"}
host_names = {"192.168.0.1":"Wi-Fi router", "google.com":"Google"}
hosts=list(host for host in host_names)
listdata=[]

def get_data():
    data={host:"" for host in hosts}
    for host_key in data:
        out=""
        with io.StringIO() as f:
            try:
                ping(f"{host_key}", verbose=True, count=1, timeout=MAX_TIME_FOR_PING_TIMEOUT_IN_SECONDS, out=f)
                f.seek(0)
                out=f.read().split(' ')[-1].strip().replace('ms','')
                if(out.replace('.','',1).isdigit() is not True):
                    out=1000
            except Exception as e:
                out=1000
        data[host_key]=out
    return data

def update(frame):
    ax.clear()

    listdata.append(get_data())
    df=pd.DataFrame(listdata).astype(float).tail(GRAPH_WINDOW_IN_DATAPOINT)
    for host in hosts:
        print(host)
        print(df)
        ax.plot(df[f'{host}'].index, df[f'{host}'], f'C{hosts.index(f"{host}")}', label=str(host_names[f'{host}']))
    ax.legend()

pyplot.legend()
animation = FuncAnimation(figure, update, interval=GRAPH_UPDATE_INTERVAL_IN_MILLISECONDS)
pyplot.show()