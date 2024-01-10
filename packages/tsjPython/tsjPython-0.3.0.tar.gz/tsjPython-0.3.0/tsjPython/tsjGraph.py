import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# from matplotlib.font_manager import FontProperties
# import matplotlib
import gVal as glv
from tsjPython.tsjCommonFunc import *
import sys
import plotly.graph_objects as go
import plotly
import plotly.io as pio
from itertools import zip_longest
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Polygon, Patch
from matplotlib.lines import Line2D
from pylab import *  

class lineData:
    def __init__(self, x_list, y_list, label, marker, color) -> None:
        self.x_list=x_list
        self.y_list=y_list
        self.max_y = max(y_list)
        self.label=label
        # https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html#sphx-glr-gallery-lines-bars-and-markers-marker-reference-py
        # candidate_marker = ['o', '.', 's', '^', '<',\
        #                     '1', '+', 'x', 'X', '*',\
        #                     'p', 'h', 'H', 'P' , '2',\
        #                     "$A$", '$B$', '$C$' , '$D$', '$E$'\
        #                     ]
        self.marker=marker
        # https://matplotlib.org/stable/gallery/color/named_colors.html
        # candidate_color = ['orange','red','blue','g','c',
        #                    'y','k','purple','gray','brown', 
        #                    'pink','lime', 'slateblue', 'gold','darkred',
        #                    'tomato', 'tan', 'olive', 'teal', 'violet' ]
        self.color=color
        pass

DEFAULT = 0
SOFT = 1
STRONG = 2  
class GraphData:
    
    def __init__(self, type, title, xaxis_title, yaxis_title, \
                fontsize: int, hide_inside_text: bool, save_path, data_dict, \
                tail_avg_data=False, is_normalized = False, color_choice = DEFAULT):
        if type == "group_bar":
            # for stacked graphs
            self.x = [[],[]]
        elif type == "compare_bar":
            self.x = []
        elif type == "multi_line":
            pass
        else:
            assert False, "Invalid graph type: {type}"
        self.title = title
        self.type = type
        self.xaxis_title = xaxis_title
        self.yaxis_title = yaxis_title
        self.fontsize = fontsize
        self.hide_inside_text=hide_inside_text
        self.save_path = save_path
        
        self.data_dict = data_dict
        self.max_value = 1
        self.size_number = 0
        self.tail_avg_data = tail_avg_data
        self.is_normalized = is_normalized
        self.color_choice = color_choice
        
    # python function not support overloading
    def append4(self,x_first,x_second, data_list):
        if self.type == "group_bar":
            self.x[0].append(x_first)
            self.x[1].append(x_second)
            tmp_sum = 0
            for key, add in zip(self.data_dict, data_list):
                tmp_sum += add
                self.data_dict[key].append(add)
            self.max_value = max(tmp_sum, self.max_value)
        else:
            assert False, f"Not matched type: {self.type}"
          
    def append(self,x_input, data_list):
        if self.type == "compare_bar":
            self.x.append(x_input)
            for key, add in zip(self.data_dict, data_list):
                self.data_dict[key].append(add)
                self.max_value = max(add, self.max_value)
        else:
            assert False, f"Not matched type: {self.type}"
       
    def append_line(self, line_data: lineData):
        if self.type == "multi_line":
            self.data_dict[line_data.label]=line_data
            self.max_value = max(line_data.max_y, self.max_value)
            self.size_number = max(self.size_number , len(line_data.x_list))
        else:
            assert False, f"Not matched type: {self.type}"
        
    def size(self):
        if self.type == "compare_bar": 
            return len(self.x)
        elif self.type == "group_bar":
            return len(self.x[0])
        elif self.type == "multi_line":
            return self.size_number
        else:
            assert False, "Invalid graph type: {type} in graph size()"
            
def line_chart(graph_data):       
    # Sample data
    # x_values = [1, 2, 3, 4, 5]
    # y_values1 = [3, 6, 2, 8, 5]
    # y_values2 = [5, 4, 7, 1, 3]
    # y_values3 = [2, 7, 3, 4, 6]

    # Create a new figure and axis
    plt.figure(figsize=(10, 6))
    plt.title(graph_data.title)
    plt.xlabel(graph_data.xaxis_title)
    plt.ylabel(graph_data.yaxis_title)

    # Plot the data
    # plt.plot(x_values, y_values1, label="Line 1", marker='o')
    # plt.plot(x_values, y_values2, label="Line 2", marker='s')
    # plt.plot(x_values, y_values3, label="Line 3", marker='^')
    for line_label, line_data in graph_data.data_dict.items():
        plt.plot(line_data.x_list, line_data.y_list, label=line_label, marker=line_data.marker)
        x_values = line_data.x_list
    
    
    # plt.xscale('log',base=10)
    
    # Set custom x-axis ticks
    # plt.xticks(x_values)

    # Add a legend
    plt.legend()

    # Show the plot
    plt.grid(True, which='major',axis='y', zorder=-1.0)
    
    plt.savefig(graph_data.save_path, dpi=300)
    filename = f"{graph_data.save_path}.svg"
    plt.savefig(filename, format='svg')
    filename = f"{graph_data.save_path}.pdf"
    plt.savefig(filename, format='pdf')

def barlike_linechart(graph_data):
    import matplotlib.pyplot as plt

    # Sample data
    # categories = ['A', 'B', 'C', 'D', 'E']
    # values = [15, 23, 10, 30, 18]

    if graph_data.max_value > 1:
        max_y = graph_data.max_value + 10
    else:
        max_y = graph_data.max_value
        
    # Create a new figure and axis
    plt.figure(figsize=(12, 3*graph_data.size()))
    plt.title(graph_data.title)
    plt.xlabel(graph_data.xaxis_title)
    plt.ylabel(graph_data.yaxis_title)


    for line_label, line_data in graph_data.data_dict.items():
        categories = line_data.x_list
        values = line_data.y_list
        ic(categories,values)
        # Create scatter plot for highlighted points
        plt.scatter(categories, values, color=line_data.color,
                    label=line_label, marker=line_data.marker,
                    edgecolors='black', linewidth=1, zorder=5)

        # Draw broken lines connecting each bar's top sequentially
        for i in range(len(categories) - 1):
            plt.plot([i, i + 1], [values[i], values[i + 1]], linestyle='dashed', color=line_data.color)
            
        # Add value numbers above the scatter points
        for i, value in enumerate(values):
            plt.text(i, value + max_y/100, str(round(value,3)), ha='center', fontsize=6)
            


    # Set x-axis ticks and labels
    plt.xticks(range(len(categories)), categories)

    if graph_data.max_value > 1:
        plt.yticks(np.arange(0, max_y ,10), fontsize=graph_data.fontsize)
    else:
        plt.yticks(np.arange(0, max_y ,0.1), fontsize=graph_data.fontsize)
    
    # Add a legend
    plt.legend( loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)
    
    # Adjust the left margin to make room for the legend, left & right chart vertical line position from [0,1]
    plt.subplots_adjust(left=0.1, right=0.8)
    
    # Show the plot
    plt.grid(True, which='major',axis='y', zorder=-1.0)
    
    
    plt.savefig(graph_data.save_path, dpi=300)
    filename = f"{graph_data.save_path}.svg"
    plt.savefig(filename, format='svg')
    filename = f"{graph_data.save_path}.pdf"
    plt.savefig(filename, format='pdf')




# plotly implementation:
# but many flaw make me crazy: the add_annotation of overflow value will disappeared nowhere which mathplotlib will not.
# so maybe use matplotlib to achieve figure like in CoNDA:
# https://stackoverflow.com/questions/65293432/creating-multiple-rows-of-matplotlib-x-labels
def group_stacked_bar_chart(graph_data: GraphData):
    x = graph_data.x
    barDict = graph_data.data_dict
    maxY = graph_data.max_value
    fig = go.Figure()
    # color from https://stackoverflow.com/questions/68596628/change-colors-in-100-stacked-barchart-plotly-python
    if graph_data.color_choice == DEFAULT:
        color_list = [
                'rgb(29, 105, 150)', \
                'rgb(56, 166, 165)', \
                'rgb(15, 133, 84)',\
                'rgb(95, 70, 144)']
    else:
        color_list = [
                'rgb(148, 170, 217)',\
                'rgb(56, 166, 165)', \
                'rgb(15, 133, 84)',\
                'rgb(95, 70, 144)']
    sumList = [0 for i in range(len(x[0]))]
    # Create an array of custom hatch patterns (wavy lines)
    if graph_data.hide_inside_text:
        for i, entry in enumerate( barDict.items()):
            barName=entry[0]
            yList = entry[1]
            ic(sumList,yList)
            sumList = [x + y for x, y in zip(yList, sumList)]
            yList = [min(maxY, y) for y in entry[1]]
            # find the overflow
            overflow_pattern = ["/" if y > maxY  else "" for y in entry[1]]
            fig.add_bar(x=x,y=yList, 
                name=barName, 
                marker=dict(
                    color=color_list[i],
                    pattern_shape = overflow_pattern,
                    line=dict(color='black', width=0.5)
                    ),
                textfont=dict(size=graph_data.fontsize),
       
            )
    else:
        for i, entry in enumerate( barDict.items()):
            barName=entry[0]
            yList = entry[1]
            ic(sumList,yList)
            sumList = [x + y for x, y in zip(yList, sumList)]
            yList = [min(maxY, y) for y in entry[1]]
            fig.add_bar(x=x,y=yList, 
                name=barName, 
                text =[f'{val:.2f}' for val in yList], 
                textposition='inside',
                marker=dict(
                    color=color_list[i],
                    pattern_shape="/"),
                textfont=dict(size=graph_data.fontsize),
                
            )
    for i, entry in enumerate(sumList):
        ic(x[0][i],x[1][i])
        
        # ref: https://plotly.com/python/reference/layout/annotations/
        fig.add_annotation(
            x=[x[0][i],x[1][i]],  # 注释的 x 坐标为 "bc"
            y=min(maxY,entry),  # 注释的 y 坐标为该列的最大值
            text=f"{entry:.2f}",  # 注释的文本内容
            # valign = "bottom", # text position in text box(default invisible)
            yanchor = "bottom", # text box position relative to anchor
            showarrow=False,  # 显示箭头
            # bgcolor="rgba(255, 255, 255, 0.8)",  # 注释框背景颜色
            font=dict(size=graph_data.fontsize+2)  # 注释文本字体大小
        )
        # Create scatter trace of text labels. ref:https://plotly.com/python/text-and-annotations/
        # fig.add_trace(go.Scatter(
        # but plotly can not correctly recognize the x
        #     x=[x[1][i]],  # 注释的 x 坐标为 "bc"
        #     y=[min(maxY,entry)+maxY/25],  # 注释的 y 坐标为该列的最大值
        #     text=[f'{entry:.2f}'],  # 注释的文本内容
        #     mode="text",
        # ))
        
    if graph_data.tail_avg_data:
        v_x = len(sumList)-1.5
        fig.add_vline(x=v_x, line_width=1.1, line_dash="dot", line_color="black")
    
    ic(maxY)
    
    # Add a rectangle shape to cover the entire subplot area
    fig.add_shape(type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0,
                x1=1, y1=1,
                line=dict(color="black", width=0.7))

    # Increase the distance between y-axis label and the axis ticks
    label_standoff = 40  # Adjust this value to your preference
    fig.update_yaxes(title_standoff=0,
                     ticksuffix=" "
                     )
    
    # Set the y-axis range to limit the max y-value


    fig.update_layout(barmode="relative", 
                    title={
                        "text": graph_data.title,
                        "x": 0.5,  # Set the title's x position to 0.5 for center alignment
                        "pad": {"t": 30}  # Adjust the padding of the title
                    },
                    xaxis_title=graph_data.xaxis_title,
                    yaxis_title=graph_data.yaxis_title,
                    yaxis_range=[0,maxY],                   
                    yaxis=dict(
                        # autorange=True, 
                        # showgrid=True,
                        # zeroline=True,
                        rangemode='tozero',  # Set the y-axis rangemode to 'tozero'
                        dtick=maxY/10,
                        gridcolor='rgb(196, 196, 196)',
                        gridwidth=1,
                        # zerolinecolor='rgb(196, 196, 196)',
                        # zerolinewidth=2,
                    ),
                    legend_title="",
                    font=dict(
                        family="Times New Roman",
                        size=graph_data.fontsize,
                        color="Black"
                    ),
                    height=350, width=50 * graph_data.size(), # 图片的长宽
                    template = "plotly_white", # https://plotly.com/python/templates/
                    margin=dict(b=1, t=20, l=20, r=5),
                    bargap=0.2
     )
    
    formats = ['svg', 'png', 'pdf', 'eps']
    for fmt in formats:
        filename = f"{graph_data.save_path}.{fmt}"
        pio.write_image(fig, filename , format=fmt, scale=3)



def compareBar(graph_data:GraphData):
    # matplotlib.use("pgf")
 
    # # 创建FontProperties对象，并设置字体搜索路径
    # custom_font_prop = FontProperties()
    # custom_font_prop.set_file(glv._get("custom_font_dir"))  # 设置自定义字体搜索路径

    # # 修改Matplotlib的字体设置
    # plt.rcParams.update({
    # 	'font.family': custom_font_prop.get_name()  # 设置自定义字体
    # })
 
    group_count = len(graph_data.data_dict)    
    x_count = len(graph_data.x)
    matplotlib.rcParams.update({
        "pgf.texsystem": "pdflatex",
        'font.family': 'serif',
        # 'text.usetex': True,
        # 'pgf.rcfonts': False,
    })
    plt.rcParams['hatch.linewidth'] = graph_data.fontsize/2
    # plt.rcParams['hatch.color'] = 'white' 
    plt.rcParams.update({'hatch.color': 'white'})
    matplotlib.use('Agg') # 禁止交互式窗口
    
    # data from https://allisonhorst.github.io/palmerpenguins/
    fig, ax = plt.subplots()

    # Adjust the margins to cut down extra space
    plt.subplots_adjust(left=0.04, right=0.99, bottom=0.1)

    if group_count*x_count > 22:
        gap_count = 0.5
    else:
        gap_count = 1.5
    fig.set_size_inches(w= 0.5 * x_count * (group_count + gap_count), h=5.75 * 0.8) #(8, 6.5)
    x = np.arange(len(graph_data.x))  # the label locations
    ic(x)
    width = 1/(group_count + gap_count) # the width of the bars
    multiplier = 0
    if(graph_data.max_value > 15):
        max_value =  graph_data.max_value+100
    else:
        max_value = graph_data.max_value+2
  
    # if you want grid
    ax.grid(True, which='major',axis='y', zorder=-1.0)
    

    
    # manually set colors
    if graph_data.color_choice == DEFAULT:
        # Define colors for each group (e.g., 'Paired')
        # more colormap choose in https://matplotlib.org/stable/tutorials/colors/colormaps.html#qualitative
        color_palette = plt.cm.get_cmap('tab10', 5) # use color=color_palette(idx)) in the following code
        pattern_list = ["" for i in range(group_count)]
    elif graph_data.color_choice == SOFT:
        color_palette = ['#f1cdb0',  '#cadfb9', '#b8c6e4', '#fbe7a3', '#aeabaa']
        pattern_list = ["" for i in range(group_count)]
    else:
        color_palette = ['black',  'w', (193/255, 1/255, 1/255), 'w', 'w']
        pattern_list = ["", "*", "/", "xx",  "\\"]
    
    edgecolor_list = ['w', (127/255, 126/255, 127/255), 'w', (0/255, 176/255, 80/255), (85/255, 133/255, 191/255)]
    
    for idx, (species_name, measurement) in enumerate(graph_data.data_dict.items()):
        ic(measurement)
        offset = width * multiplier
        ic(range(len(graph_data.data_dict)))
        
        # white doubel ref: https://stackoverflow.com/questions/38168948/how-to-decouple-hatch-and-edge-color-in-matplotlib
        # ref2: https://stackoverflow.com/questions/71424924/how-to-change-the-edge-color-of-markers-patches-in-matplotlib-legend
        if graph_data.color_choice == DEFAULT:
            rects0 = ax.bar(x + offset, measurement, width, label=species_name,
                       color=color_palette(idx),
                        hatch = pattern_list[idx],
                        edgecolor=edgecolor_list[idx],
                        linewidth=1,
                     )
        else:
            rects0 = ax.bar(x + offset, measurement, width, label=species_name,
                       color=color_palette[idx],
                        hatch = pattern_list[idx],
                        edgecolor=edgecolor_list[idx],
                        linewidth=1,
                     )
        # set zorder to hide grid
        for bar in rects0:
            bar.set_zorder(10)
        # rects = ax.bar(x + offset,  measurement, width, label=species_name,
        #             #  color=color_palette(idx),
        #              color=color_palette[idx],
        #              edgecolor='white', linewidth=1,
        #              hatch = pattern_list[idx]
        #              )
        rects = ax.bar(x + offset, measurement, width, label=species_name,
                    color = "none",
                    edgecolor='black', linewidth=1,
                    #  color=color_palette[idx],
                    #  hatch = pattern_list[idx]
                     )
        
        # set zorder to hide grid
        for bar in rects:
            bar.set_zorder(10)
        ax.bar_label(rects0, padding=2, 
                     fontsize=graph_data.fontsize+2) # Distance of label from the end of the bar, in points.
        multiplier += 1
        ic(measurement,rects)
        # 判断柱子是否超出最大范围
        for rect, value in zip(rects, measurement):
            if value > max_value:
                # 添加波浪线和标注
                ax.annotate(f'{value}', xy=(rect.get_x() + rect.get_width() / 2, max_value), xytext=(0, -20),
                            textcoords='offset points', ha='center', va='bottom',
                            arrowprops=dict(arrowstyle='fancy'))

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(graph_data.yaxis_title, fontsize=graph_data.fontsize,
                fontweight='bold')
    ax.set_xlabel("",fontsize=graph_data.fontsize)
    ax.set_title(graph_data.title, fontsize=graph_data.fontsize)
    

    
    # Calculate the legend width based on the figure width
    fig_size = plt.gcf().get_size_inches()
    fig_width = fig_size[0]
    legend_width = fig_width * 3 / (group_count - 1) # Adjust the percentage as needed    
    ic(legend_width)
    legend_fontsize = graph_data.fontsize+6
    handles1, labels1 = ax.get_legend_handles_labels()
    plt.legend([handles1[2*idx]+handles1[2*idx+1] for idx in range(group_count)], 
               [labels1[2*idx] for idx in range(group_count)],  
                loc='upper center', bbox_to_anchor=(0.5, 1 + legend_fontsize/100), 
                ncol=group_count,  # have labels in one line
                frameon=False,
                # bbox_transform=plt.gcf().transFigure,
                columnspacing=legend_width-legend_fontsize/2, 
                # handlelength=1.0, 
                handleheight=1.2, 
                prop={'size': legend_fontsize,
                    'weight': 'heavy'},
    ) 
    # set the bar move in x direction
    ax.set_xticks(x + (group_count-1)*0.5*width, graph_data.x)
    
    # if x tail avg, highlight the tail x label
    if graph_data.tail_avg_data:
        for idx,lab in enumerate(ax.get_xticklabels()):
            if idx == x_count-1:
                lab.set_fontweight('bold')
    
    # and add cut line 
    if graph_data.tail_avg_data:
        over_line = 1/16
        cut_x = (2 * x_count - 3 + (group_count-1)*width)/2
        plot([cut_x, cut_x], [- max_value * over_line, max_value * (1+over_line)], color='k', linestyle='--', lw=4)
        # clip_on=False)

    if graph_data.is_normalized:
        ax.axhline(y=1, color='k', linestyle='-', lw=3, zorder = 20)

    # set y axis
    if(graph_data.max_value > 500):
        plt.yscale('log',base=10)
        ax.set_ylim(0.1, graph_data.max_value+100) # 2
    elif(graph_data.max_value > 50):
        plt.yscale('linear')
        ax.set_ylim(0, graph_data.max_value+10) # 2
    elif(graph_data.max_value > 1.1):
        plt.yscale('linear')
        ax.set_ylim(0, graph_data.max_value+0.5) # 2
    else:
        plt.yscale('linear')
        ax.set_ylim(0.5, graph_data.max_value+0.1) # 2
    ic(graph_data.max_value)
    #set y-axis ticks (step size=5)
    ic(np.arange(0,105, 5))
    
    if graph_data.max_value > 10:
        plt.yticks(np.arange(0,graph_data.max_value + 10 ,10), fontsize=graph_data.fontsize)
    elif graph_data.max_value > 1.1:
        plt.yticks(np.arange(0,graph_data.max_value ,1), fontsize=graph_data.fontsize)
    else:
        plt.yticks(np.arange(0.5,graph_data.max_value+0.1 ,0.1), fontsize=graph_data.fontsize)
        
    plt.xticks(fontsize=graph_data.fontsize+8)
    # Adjust x-axis limits to narrow the gap
    plt.xlim(-(0.5+gap_count)*width, x_count - 1 + (group_count-1)*width + (0.5+gap_count)*width)
    
    # set custom labels of y, ref:https://stackoverflow.com/questions/40566413/matplotlib-pyplot-auto-adjust-unit-of-y-axis
    # ax.yaxis.set_major_formatter(FuncFormatter(y_fmt))
    
    plt.savefig(graph_data.save_path, dpi=300)
    filename = f"{graph_data.save_path}.svg"
    plt.savefig(filename, format='svg')
    filename = f"{graph_data.save_path}.pdf"
    plt.savefig(filename, format='pdf')
    
 
def group_stacked_bar_chart_with_error_bar(x, barDict, up_error, down_error, maxY, title_name,saved_path):
    # maxY = max(1.2, maxY)
    maxY = 1.2 * maxY
    # [x, barDict] = detailNormalizedGraphAppDict()
    # ic(x)
    # x = [
    # 	["bc", "bc", "bc", "sssp", "sssp", "sssp"],
    # 	["CPU-ONLY", "PIM_ONLY", "PIMProf", "CPU-ONLY", "PIM_ONLY", "PIMProf",]
    # ]
    fig = go.Figure()

    # color from https://stackoverflow.com/questions/68596628/change-colors-in-100-stacked-barchart-plotly-python
    color_list = ['rgb(29, 105, 150)', \
                'rgb(56, 166, 165)', \
                'rgb(15, 133, 84)',\
                'rgb(95, 70, 144)']
    sumList = [0 for i in range(len(x[0]))]
    for i, entry in enumerate( barDict.items()):
        barName=entry[0]
        yList = entry[1]
        ic(sumList,yList)
        sumList = [x + y for x, y in zip(yList, sumList)]
        # add error bar
        fig.add_bar(x=x,y=yList, 
              name=barName, 
              text =[f'{val:.2f}' for val in yList], 
              textposition='inside',
              marker=dict(color=color_list[i]),
              error_y=dict(
                type='data',
                symmetric=False,
                color='rgb(95, 70, 144)',
                array=[i-j for i,j in zip(up_error,sumList)],
                arrayminus=[i-j for i,j in zip(sumList,down_error)],
                thickness=1, width=3),
              textfont=dict(size=8)
        )

    maxY = max(maxY, 1.2*max(up_error))
    for i, entry in enumerate(sumList):
        # add error bars
        # ic(x[0][i],x[1][i],entry,up_error[i]-entry,entry-down_error[i])
        # fig.add_trace(go.Scatter(
        # 	name='ceil_floor',
        # 	x=[[x[0][i],x[1][i]]], y=[entry],
        # 	mode='markers',
        # 	error_y=dict(
        # 		type='data',
        # 		symmetric=False,
        # 		array=[0.1],
        # 		arrayminus=[0.15]),
        # 	marker=dict(color='purple', size=8)
        # ))
        if entry > maxY+0.01:
            ic(x[0][i],x[1][i])
            # 添加 "bc" 列的注释
            fig.add_annotation(
                x=[x[0][i],x[1][i]],  # 注释的 x 坐标为 "bc"
                y=maxY,  # 注释的 y 坐标为该列的最大值
                text=f'{entry:.2f}',  # 注释的文本内容
                showarrow=True,  # 显示箭头
                arrowhead=1,  # 箭头样式
                ax=0,  # 箭头 x 偏移量
                ay=-10,  # 箭头 y 偏移量，负值表示向下偏移
                # bgcolor="rgba(255, 255, 255, 0.8)",  # 注释框背景颜色
                # font=dict(size=4)  # 注释文本字体大小
                font=dict(size=8)  # 注释文本字体大小
            )
        else:
            fig.add_annotation(
                x=[x[0][i],x[1][i]],  # 注释的 x 坐标为 "bc"
                y=entry+maxY/25,  # 注释的 y 坐标为该列的最大值
                text=f'{entry:.2f}',  # 注释的文本内容
                showarrow=False,  # 显示箭头
                # bgcolor="rgba(255, 255, 255, 0.8)",  # 注释框背景颜色
                font=dict(size=6)  # 注释文本字体大小
            )
 

    # fig.add_bar(x=x,y=[10,2,3,4,5,6], name="CPU")
    # fig.add_bar(x=x,y=[6,5,4,3,2,1], name="DataMove")
    # fig.add_bar(x=x,y=[6,5,4,3,2,1], name="PIM")
    ic(maxY)
    width=1200
    height=400
    fig.update_layout(barmode="relative", 
                    title={
                        "text": title_name,
                        "x": 0.5,  # Set the title's x position to 0.5 for center alignment
                        "pad": {"t": 30}  # Adjust the padding of the title
                    },
                     xaxis_title="GAP and PrIM workloads",
                    yaxis_title="Percentage (%)",
                    yaxis_range=[0,maxY],
                    legend_title="Legend Title",
                    font=dict(
                        family="serif",
                        size=12,
                        color="Black"
                    ),
                    height=height, width=width, # 图片的长宽
                    template = "plotly_white", # https://plotly.com/python/templates/
                    margin=dict(b=60, t=40, l=20, r=20),
                    bargap=0.2
     )
    pio.write_image(fig, saved_path, format="png", scale=3)
  
def y_fmt(y, pos):
    decades = [1e9, 1e6, 1e3, 1e0, 1e-3, 1e-6, 1e-9 ]
    suffix  = ["G", "M", "k", "" , "m" , "u", "n"  ]
    if y == 0:
        return str(0)
    
    return f"{y}%"
    
    for i, d in enumerate(decades):
        if np.abs(y) >=d:
            val = y/float(d)
            signf = len(str(val).split(".")[1])
            if signf == 0:
                return '{val:d} {suffix}'.format(val=int(val), suffix=suffix[i])
            else:
                if signf == 1:
                    # print val, signf
                    if str(val).split(".")[1] == "0":
                       return '{val:d} {suffix}'.format(val=int(round(val)), suffix=suffix[i]) 
                tx = "{"+"val:.{signf}f".format(signf = signf) +"} {suffix}"
                return tx.format(val=val, suffix=suffix[i])

                #return y
    return y