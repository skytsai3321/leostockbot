from pymongo import MongoClient
import urllib.parse
import datetime

##### 資料庫設定 #####
# Authentication Database認證資料庫
Authdb = 'leostockdb'

##### 資料庫連結 #####


def constructor():
    client = MongoClient(
        "mongodb+srv://leotsai:5ram1o@cluster0.6b9yz.gcp.mongodb.net/leostockdb?retryWrites=true & w=majority")
    db = client[Authdb]
    return db

# ----------------------儲存使用者股票----------------------


def write_user_stock_fountion(stock, bs, price):
    db = constructor()
    collect = db['mystock']
    collect.insert({
        "stock": stock,
        "data": "care_stock",
        "bs": bs,
        "price": float(price),
        "date_info": datetime.datetime.utcnow()
    })

# ----------------------刪除使用者股票----------------------


def delete_user_stock_fountion(stock):
    db = constructor()
    collect = db['mystock']
    collect.delete({
        "stock": stock
    })

# ----------------------秀出使用者的股票----------------------


def show_user_stock_fountion():
    db = constructor()
    collect = db['mystock']
    cel = list(collect.find({
        "data": "care_stock"
    }))
    return cel
