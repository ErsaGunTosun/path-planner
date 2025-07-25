import folium
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import math
from shapely.geometry import Point, LineString

class PathPlanner:
    def __init__(self):
        self.obstacle_penalty = 10000
    
    def is_edge_near_obstacle(self, node1, node2, G, obstacle_points, obstacle_radius=100):
        if not obstacle_points:
            return False
            
        lat1, lon1 = G.nodes[node1]['y'], G.nodes[node1]['x']
        lat2, lon2 = G.nodes[node2]['y'], G.nodes[node2]['x']
        
        edge_line = LineString([(lon1, lat1), (lon2, lat2)])
        
        radius_deg = obstacle_radius / 111000

        for obs_lat, obs_lon in obstacle_points:
            obs_point = Point(obs_lon, obs_lat)
            obs_circle = obs_point.buffer(radius_deg)
            
            if edge_line.intersects(obs_circle):
                return True
                
        return False
    
    def modify_graph_with_obstacles(self, G, obstacle_points, obstacle_radius=100):
        if not obstacle_points:
            return G
            
        G_modified = G.copy()
        edges_to_modify = []
        
        for u, v, key in G_modified.edges(keys=True):
            if self.is_edge_near_obstacle(u, v, G_modified, obstacle_points, obstacle_radius):
                edges_to_modify.append((u, v, key))
        
        for u, v, key in edges_to_modify:
            if G_modified.has_edge(u, v, key):
                current_length = G_modified[u][v][key].get('length', 1000)
                G_modified[u][v][key]['length'] = current_length + self.obstacle_penalty
                
        return G_modified

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
        
    def CreateMapWithPolygon(self,points):
        from shapely.geometry import Polygon
        polygon = Polygon(points)
        G = ox.graph_from_polygon(polygon, network_type='drive')
        return G
    
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
    
    def CreateMapForAllMarkers(self, markers):
        lats = [marker[0] for marker in markers]
        lons = [marker[1] for marker in markers]
        
        min_lat, max_lat = min(lats), max(lats)
        min_lon, max_lon = min(lons), max(lons)
        
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        center_point = (center_lat, center_lon)
        
        diagonal_distance = haversine_distance((min_lat, min_lon), (max_lat, max_lon))
        
        radius = (diagonal_distance * 0.7) + 1000  
    
        if radius < 1000:
            radius = 1000
        elif radius > 20000:  
            radius = 20000

        try:
            G = ox.graph_from_point(center_point, dist=radius, network_type='drive')
            return G
        except Exception as e:
            return self.CreateMapWith2Point(markers[0], markers[1])
    
    def CreatePathWithAStar(self, markers, obstacle_points=None):
        if len(markers) < 2:
            return []
    
        G = self.CreateMapForAllMarkers(markers)
        
        if obstacle_points:
            G_modified = self.modify_graph_with_obstacles(G, obstacle_points)
        else:
            G_modified = G
        
        all_path_edges = []
        total_distance = 0
        
        for i in range(len(markers) - 1):
            point1 = markers[i]
            point2 = markers[i + 1]
            
            try:
                orig_node = ox.distance.nearest_nodes(G_modified, point1[1], point1[0])
                dest_node = ox.distance.nearest_nodes(G_modified, point2[1], point2[0])
                
                def heuristic(u, v):
                    u_coords = (G_modified.nodes[u]['y'], G_modified.nodes[u]['x'])
                    v_coords = (G_modified.nodes[v]['y'], G_modified.nodes[v]['x'])
                    return haversine_distance(u_coords, v_coords)
                
                route = astar_algorithm(G_modified, orig_node, dest_node, heuristic)

                if not route:
                    print(f"No path found between waypoints {i} and {i+1}, possibly due to obstacles")
                    continue
                
                G_route = nx.MultiDiGraph()
                G_route.graph = G_modified.graph.copy()
                
                for node_id in route:
                    if node_id in G_modified:
                        G_route.add_node(node_id, **G_modified.nodes[node_id])
                
                for j in range(len(route) - 1):
                    u = route[j]
                    v = route[j+1]
                    edge_data = G_modified.get_edge_data(u, v)
                    
                    if edge_data:
                        first_key = list(edge_data.keys())[0]
                        edge_attrs = edge_data[first_key]
                        G_route.add_edge(u, v, key=first_key, **edge_attrs)
                
                path_edges = self.GetEdges(G_route)
                all_path_edges.extend(path_edges)
                
                segment_distance = haversine_distance(point1, point2)
                total_distance += segment_distance
                
            except Exception as e:
                print(f" Custom A* Error: {str(e)}")
                continue
        
        return all_path_edges

    def CreatePathWithDijkstra(self, markers, obstacle_points=None):
        if len(markers) < 2:
            return []
    
        G = self.CreateMapForAllMarkers(markers)
        
        if obstacle_points:
            G_modified = self.modify_graph_with_obstacles(G, obstacle_points)
        else:
            G_modified = G
        
        all_path_edges = []
        
        for i in range(len(markers) - 1):
            point1 = markers[i]
            point2 = markers[i + 1]
            
            try:
                orig_node = ox.distance.nearest_nodes(G_modified, point1[1], point1[0])
                dest_node = ox.distance.nearest_nodes(G_modified, point2[1], point2[0])
                
                route = dijkstra_algorithm(G_modified, orig_node, dest_node)

                if not route:
                    print(f"No path found between waypoints {i} and {i+1}")
                    continue
                
                G_route = nx.MultiDiGraph()
                G_route.graph = G_modified.graph.copy()
                
                for node_id in route:
                    if node_id in G_modified:
                        G_route.add_node(node_id, **G_modified.nodes[node_id])
                
                for j in range(len(route) - 1):
                    u = route[j]
                    v = route[j+1]
                    edge_data = G_modified.get_edge_data(u, v)
                    
                    if edge_data:
                        first_key = list(edge_data.keys())[0]
                        edge_attrs = edge_data[first_key]
                        G_route.add_edge(u, v, key=first_key, **edge_attrs)
                
                path_edges = self.GetEdges(G_route)
                all_path_edges.extend(path_edges)
                
            except Exception as e:
                print(f"Dijkstra Error: {str(e)}")
                continue
        
        return all_path_edges

    def CreateAlternativeRoutes(self, markers, obstacle_points=None, main_route_edges=None):
        if len(markers) < 2:
            return []
        
        alternatives = []
        
        G = self.CreateMapForAllMarkers(markers)
        
        if obstacle_points:
            G = self.modify_graph_with_obstacles(G, obstacle_points)
        
        # Simple Dijkstra alternative without penalty system
        # Add slight random variation to edge weights to get different path
        G_variant = G.copy()
        
        # Add small random variation (1-5%) to edge weights for alternative route
        import random
        random.seed(42)  # Fixed seed for consistent results
        
        for u, v, key in G_variant.edges(keys=True):
            if 'length' in G_variant[u][v][key]:
                original_length = G_variant[u][v][key]['length']
                # Add 1-5% random variation
                variation = random.uniform(0.01, 0.05)
                G_variant[u][v][key]['length'] = original_length * (1 + variation)
        
        route1 = self._create_path_dijkstra_with_graph(markers, G_variant)
        if route1 and len(route1) > 0:
            alternatives.append({
                'algorithm': 'Dijkstra Alternative',
                'path': route1,
            })
              
        return alternatives
    
    def _create_path_dijkstra_with_graph(self, markers, G):
        all_path_edges = []
        
        for i in range(len(markers) - 1):
            point1 = markers[i]
            point2 = markers[i + 1]
            
            try:
                orig_node = ox.distance.nearest_nodes(G, point1[1], point1[0])
                dest_node = ox.distance.nearest_nodes(G, point2[1], point2[0])
                
                route = dijkstra_algorithm(G, orig_node, dest_node)

                if not route:
                    continue
                
                G_route = nx.MultiDiGraph()
                G_route.graph = G.graph.copy()
                
                for node_id in route:
                    if node_id in G:
                        G_route.add_node(node_id, **G.nodes[node_id])
                
                for j in range(len(route) - 1):
                    u = route[j]
                    v = route[j+1]
                    edge_data = G.get_edge_data(u, v)
                    
                    if edge_data:
                        first_key = list(edge_data.keys())[0]
                        edge_attrs = edge_data[first_key]
                        G_route.add_edge(u, v, key=first_key, **edge_attrs)
                
                path_edges = self.GetEdges(G_route)
                all_path_edges.extend(path_edges)
                
            except Exception as e:
                continue
        
        return all_path_edges
    
    def CreatePathWithCustomHeuristic(self, markers, obstacle_points=None, heuristic_type='haversine'):
        if len(markers) < 2:
            return []
    
        G = self.CreateMapForAllMarkers(markers)
        
        if obstacle_points:
            G_modified = self.modify_graph_with_obstacles(G, obstacle_points)
        else:
            G_modified = G
        
        all_path_edges = []
        
        for i in range(len(markers) - 1):
            point1 = markers[i]
            point2 = markers[i + 1]
            
            try:
                orig_node = ox.distance.nearest_nodes(G_modified, point1[1], point1[0])
                dest_node = ox.distance.nearest_nodes(G_modified, point2[1], point2[0])
                
                def custom_heuristic(u, v):
                    u_coords = (G_modified.nodes[u]['y'], G_modified.nodes[u]['x'])
                    v_coords = (G_modified.nodes[v]['y'], G_modified.nodes[v]['x'])
                    
                    if heuristic_type == 'manhattan':
                        return abs(u_coords[0] - v_coords[0]) + abs(u_coords[1] - v_coords[1])
                    elif heuristic_type == 'euclidean':
                        import math
                        return math.sqrt((u_coords[0] - v_coords[0])**2 + (u_coords[1] - v_coords[1])**2)
                    else:
                        return haversine_distance(u_coords, v_coords)
                
                route = astar_algorithm(G_modified, orig_node, dest_node, custom_heuristic)

                if not route:
                    continue
                
                G_route = nx.MultiDiGraph()
                G_route.graph = G_modified.graph.copy()
                
                for node_id in route:
                    if node_id in G_modified:
                        G_route.add_node(node_id, **G_modified.nodes[node_id])
                
                for j in range(len(route) - 1):
                    u = route[j]
                    v = route[j+1]
                    edge_data = G_modified.get_edge_data(u, v)
                    
                    if edge_data:
                        first_key = list(edge_data.keys())[0]
                        edge_attrs = edge_data[first_key]
                        G_route.add_edge(u, v, key=first_key, **edge_attrs)
                
                path_edges = self.GetEdges(G_route)
                all_path_edges.extend(path_edges)
                
            except Exception as e:
                continue
        
        return all_path_edges

    def PrintMapFig(self,G,name="Map",color="red"):
        fig, ax = ox.plot_graph(G, figsize=(10, 10), 
                            edge_color=color,node_size=10,show=False,)
        fig.canvas.manager.set_window_title(name)
        plt.show()

    def PrintMap(self,m,name="Map"):
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

def astar_algorithm(G, start_node, goal_node, heuristic_func=None):
    import heapq
    
    open_list = []  
    closed_list = set()
    
    g_scores = {start_node: 0}      
    f_scores = {start_node: 0}
    parent = {}
    

    if heuristic_func is None:
        def heuristic_func(node1, node2):
            coords1 = (G.nodes[node1]['y'], G.nodes[node1]['x'])
            coords2 = (G.nodes[node2]['y'], G.nodes[node2]['x'])
            return haversine_distance(coords1, coords2)

    h_start = heuristic_func(start_node, goal_node)
    f_scores[start_node] = h_start
    heapq.heappush(open_list, (h_start, start_node))
    
    while open_list:
        current_f, current_node = heapq.heappop(open_list)
        
        if current_node == goal_node:
            return reconstruct_path(parent, current_node)
        
        closed_list.add(current_node)
        
        for neighbor in G.neighbors(current_node):
            if neighbor in closed_list:
                continue
            
            edge_data = G.get_edge_data(current_node, neighbor)
            if edge_data:
                first_key = list(edge_data.keys())[0]
                edge_weight = edge_data[first_key].get('length', 1)
            else:
                edge_weight = 1
            
            tentative_g = g_scores[current_node] + edge_weight
            
            if neighbor not in g_scores:
                g_scores[neighbor] = float('inf')
            
            if tentative_g < g_scores[neighbor]:
                parent[neighbor] = current_node
                g_scores[neighbor] = tentative_g
                
                h_score = heuristic_func(neighbor, goal_node)
                f_score = tentative_g + h_score
                f_scores[neighbor] = f_score
                
                heapq.heappush(open_list, (f_score, neighbor))
    
    return []

def reconstruct_path(parent, current_node):
    path = []
    while current_node is not None:
        path.append(current_node)
        current_node = parent.get(current_node)
    
    path.reverse()
    return path

def dijkstra_algorithm(G, start_node, goal_node):
    import heapq
    
    distances = {node: float('inf') for node in G.nodes()}
    distances[start_node] = 0
    
    priority_queue = [(0, start_node)]
    parent = {}
    visited = set()
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
            
        visited.add(current_node)
        
        if current_node == goal_node:
            return reconstruct_path(parent, current_node)
        
        for neighbor in G.neighbors(current_node):
            if neighbor in visited:
                continue
            
            edge_data = G.get_edge_data(current_node, neighbor)
            if edge_data:
                first_key = list(edge_data.keys())[0]
                edge_weight = edge_data[first_key].get('length', 1)
            else:
                edge_weight = 1
            
            distance = current_distance + edge_weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return []
