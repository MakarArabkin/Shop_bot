
import json


class DBConnection():
    def __init__(self):
        self.error = False

        with open("Base.json", "r") as read_file:  
            self.data = json.load(read_file)
        
        self.picture_menu = 'https://sun9-east.userapi.com/sun9-17/s/v1/ig2/4qBrzGackWYVTaQV8cCxmaHgMUtY9zQ5fRBM00haoK5wVrEASitf4JgjMgCQiMjzD6MCUNVdVsD8cpsHc-dph-xV.jpg?size=1000x1000&quality=95&type=album'
        self.base_parsing = None
        self.base_find = {"Sneakers_find": []}
        self.orders = None
        with open('Order.json', 'r') as outfile:
            self.orders = json.load(outfile)
            
    def cls_find (self):
        self.base_find = {"Sneakers_find": []}
    def cls_order (self,m):
        self.orders['Change Orders'] = []

    def update_order(self):
        with open('Order.json', 'w') as outfile:
            json.dump(self.orders, outfile)
