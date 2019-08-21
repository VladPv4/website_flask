from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    name='GOOG'
    start=datetime.datetime(2018,8,1)
    end=datetime.datetime(2019,8,30)
    df = data.DataReader(name=name,data_source='yahoo',start=start,end=end)

    def inc_dec(c,o):
        if c>o:
            value='Increase'
        elif c<o:
            value='Descrease'
        else:
            value='Equal'
        return value

    df['Status']=[inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df['Middle']=(df.Open+df.Close)/2
    df['Height']=abs(df.Close-df.Open)

    p=figure(x_axis_type='datetime',width=1000,height=300,sizing_mode='scale_width')
    p.title.text=str('Stock Prices. Ticker: '+str(name))
    p.grid.grid_line_alpha=0.5

    hours_12=12*60*60*1000

    p.segment(df.index,df.High,df.index,df.Low,color='black')

    p.rect(df.index[df.Status=='Increase'],df.Middle[df.Status=='Increase'], hours_12,
        df.Height[df.Status=='Increase'],fill_color='green',line_color='black')

    p.rect(df.index[df.Status=='Descrease'],df.Middle[df.Status=='Descrease'], hours_12,
        df.Height[df.Status=='Descrease'],fill_color='red',line_color='black')


    script1, div1 = components(p)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]
    return render_template('plot.html', script1=script1, div1=div1, cdn_css=cdn_css, cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

if __name__=="__main__":
    app.run(debug=True)





# <link rel="stylesheet" href={{cdn_css | safe}} type="text/css">
# <script type="text/javascript" src={{cdn_js | safe}}></script>

# <link rel="stylesheet" href="https://cdn.pydata.org/bokeh/release/bokeh-1.0.2.min.css" type="text/css">
# <script type="text/javascript" src="https://cdn.pydata.org/bokeh/release/bokeh-1.0.2.min.js"></script>