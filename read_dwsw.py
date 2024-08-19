#dwswのgrdファイルを読み込んでデータをあフィルに出力するプログラム（2023/10/28）作成者：阿部研 佐久間

import numpy as np
import pygmt
import pandas as pd
from tkinter import filedialog
import os
import h5py


def read_data():
    ################################ パラメータ設定 #####################################

    #保存名 保存先は現在のディレクトリ
    save_title = "test.h5"

    #緯度経度

    #経度
    start_lon = 162.8125    #経度の観測開始地点
    lon_step = 0.3125       #経度のステップ間隔
    step_count = 200        #経度のデータ数

    lon = [i*lon_step+start_lon for i in range(step_count)]     #経度のデータ配列

    #緯度
    #.CTLからlatデータを[]内にコピペしてください
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

    lon_size = len(lon)
    lat_size = len(lat)

    ################################ ファイル選択 #####################################
    print("select dwsw .grd file")

    dir = os.getcwd()
    typ = [('grdファイル','*.grd')]
    #print(typ)
    path = filedialog.askopenfilename(filetypes = typ, initialdir = dir)

    ################################ データ読み込み #####################################

    with open(path,"rb") as fin:
        #データ読み込み
        dbuf = np.fromfile(fin,dtype='float32').byteswap() #データは4バイト形式なのでfloat32で読み込み
        data_size = len(dbuf)
        print("データサイズ : ", data_size)
        

    #dataサイズ = lon × lat × 日数
    day = int(data_size / lon_size / lat_size )
    print("データ日数 : ", day)

    #読み込んだ時点ではデータは1次元形式のため、3次元形式に整える
    #x=lon, y=lat, z= day
    dwsw = dbuf.reshape(day,lat_size,lon_size)
    print("データ形式 : ", dwsw)


    ################################ データ書き込み #####################################

    #データの保存形式はHDF5を採用
    #参考サイト：https://qiita.com/simonritchie/items/23db8b4cb5c590924d95

    #保存先パスを設定
    save_path = dir+"/"+save_title
    #ファイル作成
    #読み込む際の各アクセスキーは"dwsw","lat","lon"
    with h5py.File(save_path, mode='w') as h5:
        
        h5.create_dataset(name='dwsw', shape=dwsw.shape, dtype=np.float32, data=dwsw)
        h5.create_dataset(name='lat', shape=lat_size, data=lat)
        h5.create_dataset(name='lon', shape=lon_size, data=lon)

    print("All comlete.")

#おまけ
#作成したデータの読み込み処理及びグラフ作成、エクセル保存
def read_h5():
    #パスの設定
    dir = os.getcwd()
    typ = [('h5ファイル','*.h5')]
    
    #データ読み込み
    path = filedialog.askopenfilename(filetypes = typ, initialdir = dir)
    with h5py.File(path, "r") as h5:
        print(h5.keys())
        #" "の中身がアクセスキー、[:]←これで中身のデータを取得する
        data = h5["dwsw"][:]
        lat = h5["lat"][:]
        lon = h5["lon"][:]

    #1日分のデータ取得 [日付、lat,lon]の順
    data_oneday = data[0,:,:]

    #データのメッシュ化 メインのデータは2次元だけどlat, lonは1次元→数を合わせるためにメッシュ化する
    lon, lat = np.meshgrid(lon, lat)

    #1次元に返還する
    data_oneday, lat, lon = data_oneday.ravel(), lat.ravel(), lon.ravel()

    #dataframe化
    df = pd.DataFrame()
    df["dwsw"] = data_oneday
    df["lon"]  = lon
    df["lat"]  = lat
    #エクセルに保存 お好きにファイル名は変更してください
    df.to_excel(dir+"/test.xlsx")

    #pygmtで描写
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
    fig.grdimage(grid = grddata, region=region)
    fig.coast(shorelines=True,land="lightgray")
    fig.colorbar(frame=["x+ltest", "y+ltest"], scale=1)
    #保存する場合下の処理を有効化してください ファイル名はお好きにどうぞ
    #fig.save(dir+"/test.tif")
    fig.show()
    


if __name__ == "__main__":
    #read_data()
    read_h5()