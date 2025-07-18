import folium
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import math

class PathPlanner:
    def CreateMapWithName(self,name):
        self.G = ox.graph_from_place(name, network_type='drive')
        return G

    def CreateMapWith2Point(self,point1,point2):
        center_lat = (point1[0] + point2[0]) / 2
        center_lon = (point1[1] + point2[1]) / 2
        center_point = (center_lat, center_lon)
        
        distance_between_points = haversine_distance(point1, point2)
        radius = distance_between_points * 0.7  
        if radius < 500: 
            radius = 500
        elif radius > 5000:
            radius = 5000
        
        G = ox.graph_from_point(center_point, dist=radius, network_type='drive')
        
        return G
        
    def CreateMapWithPlygon(self,points):
        pass
    
    def CreatePathWithPoint(self,point1, point2):

        G = self.CreateMapWith2Point(point1,point2)

        orig_node, dist_to_orig = ox.distance.nearest_nodes(G, point1[1],point1[0], return_dist=True)
        dest_node, dist_to_dest = ox.distance.nearest_nodes(G, point2[1], point2[0], return_dist=True)

        route = nx.shortest_path(G, source=orig_node, target=dest_node, weight='length')
        G_route = nx.MultiDiGraph()
        G_route.graph = G.graph.copy()

        for node_id in route:
            if node_id in G:
                G_route.add_node(node_id, **G.nodes[node_id])

        for i in range(len(route) - 1):
            u = route[i]
            v = route[i+1]
            edge_data = G.get_edge_data(u, v)

            if edge_data:
                first_key = list(edge_data.keys())[0]
                edge_attrs = edge_data[first_key]
                G_route.add_edge(u, v, key=first_key, **edge_attrs)

        path_edges = self.GetEdges(G_route)
        
        return path_edges
        
    def DrawMap(self,G,m,color="blue",size=3):
        gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
        for idx, edge in gdf_edges.iterrows():
            folium.PolyLine(
                locations=[[point[1], point[0]] for point in edge.geometry.coords],
                color=color,
                weight=size
            ).add_to(m)
    
    def GetEdges(self,G):
        gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
        
        path_edges = []
        for idx, edge in gdf_edges.iterrows():
            coordinates = [[point[1], point[0]] for point in edge.geometry.coords]
            path_edges.append(coordinates)

        return path_edges

    def PrintMapFig(self,G,name="Map",color="red"):
        fig, ax = ox.plot_graph(G, figsize=(10, 10), 
                            edge_color=color,node_size=10,show=False,)
        fig.canvas.manager.set_window_title(name)
        plt.show()

    def PrintMap(sel,m,name="Map"):
        file_name = f"./templates/{name}.html"
        m.save(file_name)
    

def haversine_distance(point1, point2):
    R = 6371000 
    lat1_rad, lon1_rad = math.radians(point1[0]), math.radians(point1[1])
    lat2_rad, lon2_rad = math.radians(point2[0]), math.radians(point2[1])
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c