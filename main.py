from planner.Path import Path

def main():
    path = Path()

    path.drawMap()

    path.addMarker([40.98765,29.05748],"Start Point")
    path.addMarker([40.97314,29.08090],"End Point")
    
    path.printMap()

if __name__ == "__main__":
    main()