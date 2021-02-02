import numpy as np
from bokeh.plotting import figure, save
from bokeh.io import export_png

### Function to save figure as HTML or PNG ###

def saveFigure(fig, outputPath, tool, typeSave, name):
    if tool == 'bokeh':
        if typeSave == 'png':
            export_png(fig, filename = outputPath + name + '.png')
        elif typeSave == 'html':
            save(fig, outputPath + name + '.html')
    elif tool == 'plotly':
        if typeSave == 'png':
            fig.write_image(outputPath + name + '.png') # can specify image size, add following argument: width=1920, height=1080
        elif typeSave == 'html':
            fig.write_html(outputPath + name + '.html',include_plotlyjs='cdn') # Compact version without all plotly libraries, need internet connection to properly display the graph
            #plot(fig, filename = outputPath + figExportName + '.html', auto_open=False) # Bigger version with all plotly libraries

### Functions to create linear color gradient for map plot ###
	
def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def color_dict(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}

def linear_gradient(start_hex, finish_hex, n):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") 
    '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
      # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)
    return color_dict(RGB_list)


### Functions used to build Bokeh distribution plot with log scale ###

def calculateMinMaxLogScale(value,minOrMax):
    i = value
    k = 0
    while i > 1:
        k = k + 1
        i = i/10
    if minOrMax == 'Min':
        valueBorder = 10**(k-1)
    elif minOrMax == 'Max': 
        valueBorder = 10**k
    return valueBorder

def createLogBin(start,stop):
    # Initialisation
    stopTemp  = stop
    z         = start
    increment = 0
    flag      = 0
    bins      = list()

    # While loop to calculate the number of for loop to run next
    while flag == 0:
        increment = increment + 1
        stopTemp = stopTemp/10
        # If loop to check whether stopTemp = start
        if stopTemp == start:
            flag = 1
    # For loop to create the log bin
    for y in range(0,increment):
        for x in range(1,10):
            bins.append(x*z)
        z = z*10
    # Add the last value
    bins.append(int((x+1)*z/10))
    return bins
    
def removeLastFirstValuesWhenZero(hist,bin_edges):
    #Get index until last value not 0
    for lastNotZero in range(0,len(hist)):
        if hist[len(hist)-1-lastNotZero] > 0:
            break
    #Get index of first not 0 value
    for firstNotZero in range(0,len(hist)):
        if hist[firstNotZero] > 0:
            break
    #Update hist and bin_edges
    hist = hist[firstNotZero:-lastNotZero]
    bin_edges = bin_edges[firstNotZero:-lastNotZero]
    return hist,bin_edges

# Function to plot histogram with Bokeh

def histogramBokeh(data, bins, title, xAxisLabel, yAxisLabel, dataColor, textFontFamily, textColor, textFontSize):
    fig = figure(plot_height=300,
                 title=title,
                 x_axis_label=xAxisLabel,
                 y_axis_label=yAxisLabel)
    fig.quad(top=list(data),
             bottom=0,
             left=list(range(0,len(bins)))[:-1],
             right=list(range(0,len(bins)))[1:],
             fill_color = dataColor,
             line_color = "#5F5B5B",
             alpha=1)

    fig.xaxis.ticker = list(range(0,len(bins)))
    fig.xaxis.major_label_orientation = 3.14/4
    fig.xaxis.major_label_overrides = {el:"{:,}".format((round(bins[el],1))) if (bins[el]) < 1 else "{:,}".format(int(bins[el])) for el in range(0,len(bins))}

    fig.title.text_font_size = textFontSize
    fig.title.text_color = textColor
    fig.title.text_font = textFontFamily
    fig.yaxis.axis_label_text_font = textFontFamily
    fig.yaxis.axis_label_text_font_style = "normal"
    fig.xaxis.axis_label_text_font = textFontFamily
    fig.xaxis.axis_label_text_font_style = "normal"
    fig.xaxis.major_label_text_font = textFontFamily
    fig.yaxis.major_label_text_font = textFontFamily
    return fig
    
# Function to plot cumulative distribution with Bokeh

def cumulativeDistributionBokeh(data, bins, title, xAxisLabel, yAxisLabel, dataColor, textFontFamily, textColor, textFontSize):
    fig = figure(plot_height=300,
                 title=title,
                 x_axis_label=xAxisLabel,
                 y_axis_label=yAxisLabel)
    fig.step(list(range(0,len(bins))),
             [0]+[list(np.cumsum(data))[x]/data.sum()*100 for x in range(0,len(data))],
             line_color=dataColor,
             line_width=2)

    fig.xaxis.ticker = list(range(0,len(bins)))
    fig.xaxis.major_label_orientation = 3.14/4
    fig.xaxis.major_label_overrides = {el:"{:,}".format((round(bins[el],1))) if (bins[el]) < 1 else "{:,}".format(int(bins[el])) for el in range(0,len(bins))}

    fig.title.text_font_size = textFontSize
    fig.title.text_color = textColor
    fig.title.text_font = textFontFamily
    fig.yaxis.axis_label_text_font = textFontFamily
    fig.yaxis.axis_label_text_font_style = "normal"
    fig.xaxis.axis_label_text_font = textFontFamily
    fig.xaxis.axis_label_text_font_style = "normal"
    fig.xaxis.major_label_text_font = textFontFamily
    fig.yaxis.major_label_text_font = textFontFamily
    return fig
