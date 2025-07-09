import folium
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

class Path:
    def __init__(self):
        self.place =  "Kadıköy, İstanbul, Turkey"

        self.G = ox.graph_from_place(self.place, network_type='drive')

        self.m = self.loadMap()

    def createMap(self):
        self.G = ox.graph_from_place(self.place, network_type='drive')
        self.m = self.loadMap()

    def loadMap():
        gdf_nodes = ox.graph_to_gdfs(self.G, nodes=True, edges=False)

        center_lat = gdf_nodes['y'].mean()
        center_lon = gdf_nodes['x'].mean()

        m = folium.Map(location=[center_lat, center_lon], zoom_start=15)
        return m   
    
    def drawMap(self,color="blue",size=3):
        gdf_edges = ox.graph_to_gdfs(self.G, nodes=False, edges=True)
        for idx, edge in gdf_edges.iterrows():
            folium.PolyLine(
                locations=[[point[1], point[0]] for point in edge.geometry.coords],
                color=color,
                weight=size
            ).add_to(self.m)

    def addMarker(self,location,name):
        folium.Marker(
            location=location,
            popup=name,
        ).add_to(self.m)
        
    def printMap(self,name="Map"):
        file_name = f"./map/{name}.html"
        self.m.save(file_name)

    def printMapFig(self,name="Map",color="red"):
        fig, ax = ox.plot_graph(self.G, figsize=(10, 10), 
                            edge_color=color,node_size=10,show=False,)
        fig.canvas.manager.set_window_title(name)
        plt.show()
    
   

    