
import pandas as pd
import matplotlib.pyplot as plt
import utm
from mpl_toolkits.mplot3d import Axes3D
import airport_coord
# function to convert lat/lon to UTM
lat_long_airp = airport_coord.lat_long_airp
code ='SCL'
def uuttmm(fila):
    [Easting, Northing, zone_number, zone_letter] = utm.from_latlon(fila['lat'], fila['lng'])
    return (Easting, Northing, zone_number, zone_letter)
# Function to create a plotting area in xN meters from center point (Easting, Northing)
def plotting_area(Easting, Northing, xN):
    east_left = Easting - xN
    east_right = Easting + xN
    north_up = Northing + xN
    north_down = Northing - xN
    return (east_left, east_right, north_up, north_down)

def iter_df(func):
    def wrapper(df, index): #Parameters from the function plot_trail()
        for i in index:
            a=df.loc[i] # a is a row of the main dataframe
            try:
                trail_df=pd.DataFrame(a['trail'])   
            except ValueError:
                print('No data for flight ' + i)
                continue

            if trail_df.empty:
                print("Empty trail: "+ i)
                continue
            else:
                plot_params = func(trail_df, ax)

        plt.xlim(plot_params['east_left'], plot_params['east_right'])
        plt.ylim(plot_params['north_down'], plot_params['north_up'])
        plt.show()
    return wrapper



ax = plt.figure().add_subplot(projection='3d')  
@iter_df
def plot_trail(trail_df, ax):
    # Append columns with the UTM coordinates
    coord_list = trail_df.apply(uuttmm, axis=1).to_list()
    utm_coord=pd.DataFrame(coord_list, columns=['Easting', 'Northing', 'Zone_N', 'Zone_L'])
    utm_trail_coord=pd.concat([trail_df, utm_coord], axis=1)
    # Add data to plot
    (Easting, Northing, zone_number, zone_letter) = utm.from_latlon(lat_long_airp[code]['Latitude'], 
                                                                    lat_long_airp[code]['Longitude'])
    (east_left, east_right, north_up, north_down)=plotting_area(Easting, Northing, 40000)
    result_df=utm_trail_coord[(utm_trail_coord['Easting']>east_left) & (utm_trail_coord['Easting']<east_right) 
            & (utm_trail_coord['Northing']>north_down) & (utm_trail_coord['Northing']<north_up)]
    sc= ax.plot(result_df.Easting, result_df.Northing, result_df.alt*0.3048)
    plot_params = {'sc':sc, 'east_left':east_left, 'east_right':east_right, 'north_up':north_up, 'north_down':north_down}
    return plot_params

class TrackAnalysis:
    def __init__(self, file_in):
        self.file_in = file_in

    def read_file(self):
        # Creating a main dataframe from the json file
        df = pd.read_json(self.file_in, orient='index')
        index=list(df.index.values) # list of flight ids
        return df, index

def main():
    filename = 'SCL_2022-01-04_data.json' #  <= Filename
    track = TrackAnalysis(filename)
    df, index = track.read_file()
    plot_trail(df, index)

if __name__ == '__main__':
    main()