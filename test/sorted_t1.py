aa = {"stockNumberMap": {
    "sp_french_blue_#42*xs": 12,
    "sp_french_blue_#42*s": 19,
    "sp_french_blue_#42*m": 12,
    "sp_french_blue_#42*l": 34,
    "sp_french_blue_#42*2x": 27,
    "sp_french_blue_#42*1x": 13,
    "sp_french_blue_#42*xl/0x": 16,
    "sp_dark_green_#25*1x": 25,
    "sp_dark_green_#25*xl/0x": 48,
    "sp_dark_green_#25*xs": 31,
    "sp_dark_green_#25*l": 101,
    "sp_dark_green_#25*m": 93,
    "sp_dark_green_#25*s": 101,
    "sp_dark_green_#25*2x": 31,
    "sp_navy_blue_#20*m": 22,
    "sp_navy_blue_#20*l": 30,
    "sp_navy_blue_#20*xs": 15,
    "sp_navy_blue_#20*2x": 16,
    "sp_navy_blue_#20*xl/0x": 3,
    "sp_navy_blue_#20*1x": 9,
    "sp_navy_blue_#20*s": 34,
    "sp_cabernet_#86010d*xs": 32,
    "sp_cabernet_#86010d*s": 27,
    "sp_cabernet_#86010d*m": 18,
    "sp_cabernet_#86010d*l": 17,
    "sp_cabernet_#86010d*1x": 20,
    "sp_cabernet_#86010d*xl/0x": 16,
    "sp_cabernet_#86010d*2x": 15,
    "sp_purple_#86125d*s": 6,
    "sp_purple_#86125d*m": 12,
    "sp_purple_#86125d*l": 4,
    "sp_purple_#86125d*xl/0x": 14,
    "sp_purple_#86125d*1x": 26,
    "sp_purple_#86125d*2x": 16
}}

cc = [{"map":key,"value":value}for key,value in aa['stockNumberMap'].items()]
# print(cc)
a = sorted(cc, key=lambda i: i['value'], reverse=True)[0]
print(a)
print(list(a.keys())[0])
