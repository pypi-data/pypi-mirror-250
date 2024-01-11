import random
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import is_color_like


def Color():
    c = "#"+str(hex(random.randint(0, 16777215)))[2:]
    if is_color_like(c):
        return c
    else:
        Color()

class Graphs:
    def __init__(self) -> None:
        pass
    
    def __initialization(self, *args, **kwargs):
        plt.figure(figsize=(kwargs.get("height", 12), kwargs.get("width", 8)), dpi=kwargs.get("dpi", 777))
        plt.style.use("seaborn-v0_8-muted")
        plt.rcParams["font.family"] = "DejaVu Serif"
        plt.rcParams["font.serif"] = ["Times New Roman"]
        plt.rcParams["font.size"] = 15.0
    
    def LineGraph(self,
                  data:list,
                  title:str="Line",
                  x_axis:str="X axis",
                  y_axis:str="Y axis",
                  marker:str="o",
                  line_label:str="Data",
                  save_image_path:str="",
                  line_color:str=None,
                  *args, **kwargs):
        
        self.__initialization(**kwargs)
        
        plt.plot(range(1, len(data)+1), data,
                 marker=marker,
                 color=line_color if line_color is not None else Color(),
                 label=line_label)
        plt.grid(kwargs.get("grid", True))
        plt.legend()
        plt.xlabel(xlabel=x_axis), plt.ylabel(ylabel=y_axis), plt.title(label=title)
        plt.xticks(range(1, len(data)+1))
        plt.tight_layout()
        plt.savefig("Line_Graph.png" if save_image_path=="" else save_image_path,
                    dpi=kwargs.get("dpi", 777))
        plt.close()
    
    def ScatterGraph(self,
                     data:list,
                     cluster_labels:list=[],
                     title:str="Scatter",
                     x_axis:str="X axis",
                     y_axis:str="Y axis",
                     save_image_path:str="",
                     *args, **kwargs):
        
        self.__initialization(**kwargs)
        
        markers = list(Line2D.markers.keys())[:len(data)]
        colors = [Color() for _ in range(len(data))]
        if len(cluster_labels) == 0:
            cluster_labels = [f"Data_{i}" for i in range(1, len(data)+1)]
        
        
        for i in range(len(data)):
            plt.scatter(range(len(data[i])), data[i],
                        color=colors[i],
                        marker=markers[i],
                        label=cluster_labels[i])
    
        plt.xlabel(xlabel=x_axis), plt.ylabel(ylabel=y_axis), plt.title(label=title)
        plt.grid(kwargs.get("grid", True))
        plt.legend()
        plt.tight_layout()
        plt.savefig("Scatter_Graph.png" if save_image_path=="" else save_image_path,
                    dpi=kwargs.get("dpi", 777))
        plt.close()