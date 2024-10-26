import datetime
import yfinance as yf
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource

# Descarga los datos
start = datetime.datetime(2024, 10, 2)
end = datetime.datetime(2024, 10, 25)
df = yf.download("TEF", start=start, end=end) #En el primer parametros se pone el nombre de la accion, su simbolo en bola, y el segundo parametro es el rango de tiempo
print(df)

# configuración del grafico
p = figure(x_axis_type="datetime", width=1000, height=300)
p.title.text = "Candlestick Chart"

hours_12 = 12 * 60 * 60 * 1000  # en milisegundos

# aqui filtramos los datos de subida y bajada
inc = df['Close'] > df['Open']
dec = df['Close'] < df['Open']

# datos para dias de subida en verde
source_inc = ColumnDataSource(data=dict(
    x=df.index[inc],
    y=(df['Open'][inc] + df['Close'][inc]) / 2,
    height=abs(df['Open'][inc] - df['Close'][inc])
))

# datos para dias de bajada en rojo
source_dec = ColumnDataSource(data=dict(
    x=df.index[dec],
    y=(df['Open'][dec] + df['Close'][dec]) / 2,
    height=abs(df['Open'][dec] - df['Close'][dec])
))

p.segment(df.index, df.High, df.index, df.Low, color="black") #dibuja los segmentos con los precios de apertura y cierre

# dibuja los rectangulos  subida en verde y bajada rojo
p.rect(x='x', y='y', width=hours_12, height='height', source=source_inc, fill_color="green", line_color="green")
p.rect(x='x', y='y', width=hours_12, height='height', source=source_dec, fill_color="red", line_color="red")



output_file("telefonica.html") #nombre del archivo que se va a generar
show(p) #muestra el grafico
