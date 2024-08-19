import numpy as np
import pygmt
import pandas as pd




path = "/Users/sakumasouya/Desktop/arakisan/dwsw.2010.ctl"
path = "/Users/sakumasouya/Desktop/arakisan/dwsw.2010.grd"

fin = open(path,"rb")
dbuf = np.fromfile(fin,dtype='float32').byteswap()

print(dbuf.shape)

print(len(dbuf))

#lonは200、latは100＝200×100×366

reshape = dbuf.reshape(366,100,200)

print(reshape)
print(reshape.shape)

lon = [i*0.3125+162.8125 for i in range(200)]

print(len(lon))

lat =  [50.7372,   51.0494,   51.3616,   51.6739,   51.9861,
        52.2983,   52.6106,   52.9228,   53.2350,   53.5472,
        53.8595,   54.1717,   54.4839,   54.7962,   55.1084,
        55.4206,   55.7328,   56.0451,   56.3573,   56.6695,
        56.9818,   57.2940,   57.6062,   57.9184,   58.2307,
        58.5429,   58.8551,   59.1674,   59.4796,   59.7918,
        60.1040,   60.4163,   60.7285,   61.0407,   61.3530,
        61.6652,   61.9774,   62.2896,   62.6019,   62.9141,
        63.2263,   63.5386,   63.8508,   64.1630,   64.4752,
        64.7875,   65.0997,   65.4119,   65.7242,   66.0364,
        66.3486,   66.6608,   66.9731,   67.2853,   67.5975,
        67.9097,   68.2220,   68.5342,   68.8464,   69.1587,
        69.4709,   69.7831,   70.0953,   70.4076,   70.7198,
        71.0320,   71.3443,   71.6565,   71.9687,   72.2809,
        72.5932,   72.9054,   73.2176,   73.5298,   73.8421,
        74.1543,   74.4665,   74.7788,   75.0910,   75.4032,
        75.7154,   76.0277,   76.3399,   76.6521,   76.9643,
        77.2766,   77.5888,   77.9010,   78.2133,   78.5255,
        78.8377,   79.1499,   79.4622,   79.7744,   80.0866,
        80.3988,   80.7111,   81.0233,   81.3355,   81.6477,
]

print(len(lat))

data_oneday = reshape[0,:,:]


lon, lat = np.float32(np.meshgrid(lon, lat))
data_oneday, lat, lon = data_oneday.ravel(), lat.ravel(), lon.ravel()


#dataframe化処理（可視化用）
df = pd.DataFrame()
df["imerg rain"] = data_oneday
df["lon"]        = lon
df["lat"]        = lat

df.to_excel("/Users/sakumasouya/Desktop/arakisan/test.xlsx")

print("data one day ;",data_oneday, data_oneday.shape)
print("lat : ", lat, lat.shape)
print("lon : ", lon, lon.shape)


area = [162, 200, 50, 80]
grddata = pygmt.xyz2grd(
    region = area,
    spacing = '0.5/0.5', 
    x = lon,
    y = lat, 
    z = data_oneday,)

fig = pygmt.Figure()
projection = "M15c"
region = area
fig.basemap(region=region, projection=projection, frame=True)
#KEO用
#pygmt.makecpt(series = [0, 30, 0.1], continuous = True)
fig.grdimage(grid = grddata, region=region)
 
fig.coast(shorelines=True,land="lightgray")
fig.colorbar(frame=["x+ltest", "y+ltest"], scale=1)
fig.show()

