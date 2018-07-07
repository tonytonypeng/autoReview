import json
import xlwt, xlrd,time
import requests
from xlrd import open_workbook
from xlutils.copy import copy
import math

entity_list = [
    {
        "entity": "logistics",
        "isOnline": 1,
        "value": [
            "wait_overday",
            "item_when",
            "info_status",
            "site_when",
            "delay",
            "customer_when",
            "still_processing",
            "missing",
            "where_check"
        ]
    },
    {
        "entity": "AfterSale",
        "isOnline": 1,
        "value": [
            "Not_like_expected_satisfied",
            "poor_quality_clothing",
            "PLACE_WRONG_ORDER",
            "not_as_described",
            "want_return",
            "poor_function_electronic",
            "wrong_item",
            "size_issue",
            "not_work",
            "damaged_item",
            "Smell_dirty"
        ]
    },
    {
        "entity": "other",
        "isOnline": 2,
        "value": [
            "other"
        ]
    },
    {
        "entity": "change_item",
        "isOnline": 2,
        "value": [
            "change_item",
            "change_quantity",
            "change_size_color_version"
        ]
    },
    {
        "entity": "change_shipping",
        "isOnline": 2,
        "value": [
            "change_shipping"
        ]
    },
    {
        "entity": "change_address",
        "isOnline": 2,
        "value": [
            "confirm_address",
            "correct_address",
            "ship_to_wrong_address",
            "put_wrong_address",
            "change_to_new_address",
            "move_address"
        ]
    },
    {
        "entity": "cancel_order",
        "isOnline": 2,
        "value": [
            "Order_get_canceled",
            "want_to_cancel"
        ]
    },
    {
        "entity": "Pre_shipping",
        "isOnline": 2,
        "value": [
            "free_shipping",
            "COD",
            "Where_store_located",
            "shipping_method",
            "shipping_destination",
            "shipping_time",
            "no_shipping_method",
            "Do_you_have_Branch",
            "shipping_cost",
            "expensive_sipping",
            "shipping_insurance"
        ]
    },
    {
        "entity": "pre_stock_inquiry",
        "isOnline": 2,
        "value": [
            "restock_inquiry",
            "stock_inquiry"
        ]
    },
    {
        "entity": "pre_points",
        "isOnline": 2,
        "value": [
            "forget_use_points",
            "how_to_use_points",
            "didnt_get_points",
            "cannot_use_points",
            "how_to_get_points",
            "points_benefit"
        ]
    },
    {
        "entity": "pre_coupon",
        "isOnline": 2,
        "value": [
            "how_to_get_coupon",
            "where_to_find_coupon",
            "ask_for_coupon",
            "cannot_use_coupon",
            "how_to_use_coupon",
            "didnt_get_coupon",
            "forget_use_coupon"
        ]
    },
    {
        "entity": "pre_wholesale_dropship",
        "isOnline": 2,
        "value": [
            "wholesale",
            "Facebook_cooperation",
            "blog_cooperation",
            "get_it_free",
            "supplier",
            "gift_card",
            "invite_new_customer",
            "dropship",
            "cooperation",
            "affiliate",
            "Instagram_cooperation",
            "youtube_cooperation"
        ]
    },
    {
        "entity": "Pre_payment_inquiry",
        "isOnline": 2,
        "value": [
            "cc_cannot_pay",
            "available_payment_method",
            "how_to_pay",
            "pp_cannot_pay",
            "no_payment_method",
            "Just_cannot_pay",
            "confirm_payment"
        ]
    },
    {
        "entity": "pre_wallet",
        "isOnline": 2,
        "value": [
            "wallet_benefit",
            "cannot_use_wallet",
            "change_wallet_password",
            "how_to_use_wallet"
        ]
    },
    {
        "entity": "pre_product_inquiry",
        "isOnline": 2,
        "value": [
            "bikini_top_bottom",
            "confuse_size",
            "fit_or_not",
            "size_accurate",
            "how_to_choose_size"
        ]
    },
    {
        "entity": "pre_tax_duty",
        "isOnline": 2,
        "value": [
            "declare_lower",
            "how_to_avoid_tax",
            "do_i_need_to_pay_tax"
        ]
    },
    {
        "entity": "pre_warranty_inquiry",
        "isOnline": 2,
        "value": [
            "warranty_return_policy",
            "return_bikini",
            "who_pay_return_shipping"
        ]
    },
    {
        "entity": "pre_account",
        "isOnline": 2,
        "value": [
            "cannot_login",
            "how_to_register",
            "Delete_account",
            "how_active_account",
            "cannot_find_order",
            "unsubscribe_remove_email",
            "change_account_info",
            "Can't_create_account"
        ]
    },
    {
        "entity": "Refund",
        "isOnline": 2,
        "value": [
            "How_long_refund_take",
            "Wrong_refund_amount",
            "Don't_get_refund"
        ]
    },
    {
        "entity": "Pre-contacts",
        "isOnline": 2,
        "value": [
            "What's_your_number",
            "phone_not_work",
            "Can't_submit_ticket",
            "livechat_not_work",
            "Do_you_speak_English"
        ]
    },
    {
        "entity": "AfterSale_Logistics",
        "isOnline": 2,
        "value": [
            "lost_told_by_shipping_company",
            "Package_stuck_in_Customs",
            "Package_get_returned",
            "Delivered_But_Not_Received",
            "Po_don't_have"
        ]
    },
    {
        "entity": "Aftersale_tax_duty_invoice",
        "isOnline": 2,
        "value": [
            "Told_need_to_pay_tax/duty",
            "Customer_need_invoice"
        ]
    },
    {
        "entity": "Pre_price_issues",
        "isOnline": 2,
        "value": [
            "price_difference_cart",
            "price_match"
        ]
    },
    {
        "entity": "Pre_place_order",
        "isOnline": 2,
        "value": [
            "how_to_order",
            "can't_not_order"
        ]
    },
    {
        "entity": "General",
        "isOnline": 2,
        "value": [
            "willing_to_wait"
        ]
    }

]

def getEntity(value):
    entity = ""
    for dict in entity_list:
        value_list = dict["value"]
        value_list = [item for item in value_list]
        if value in value_list:
            entity = dict["entity"]
            break
    return entity

def train(data):
    """训练会话"""
    response = requests.post('http://127.0.0.1:5000/api/v1_0/messenger/add',
                             headers={
                                 'content-type': "application/json",
                                 'cache-control': "no-cache",
                                 'postman-token': "1ccdff83-7e6d-89ec-f4d2-773f7e530e6e"
                             },
                             data=json.dumps({
	                            "message": data,
                             }))

    if response.status_code == 200:
        res = json.loads(response.content)['data']
        return res

def xaiDelete(ids):
    response = requests.post('http://127.0.0.1:8080//api/v1_0/messenger/add',
                             data=json.dumps({
                                 "ids": ids,
                             }))

    if response.status_code == 200:
        res = json.loads(response.content)['data']
        return res

# 写入excel初始化
def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

# class ParseExcel(object):
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#
#             f = xlwt.Workbook()  # 创建工作簿
#             test2 = f.add_sheet('result', cell_overwrite_ok=True)
#             row = ["id",'语料','entity','value']
#             for i in range(0, len(row)):
#                 test2.write(0, i, row[i], set_style('Times New Roman', 220, True))
#             f.save('data/关键字正式训练结果0627-1.xls')
#             cls._instance = super(ParseExcel, cls).__new__(cls)
#         return cls._instance
#
#     def write_excel(self, values, filename):
#         r_xls = open_workbook(filename)
#         r_sheet = r_xls.sheet_by_index(0)
#         rows = r_sheet.nrows
#         wb = copy(r_xls)
#         ws = wb.get_sheet(0)
#         for i in range(0, len(values)):
#             ws.write(rows, i, values[i])
#         wb.save(filename)
#
data = xlrd.open_workbook('data/0703语料后台数据.xlsx')
table = data.sheets()[0]
nrows = table.nrows
# parseExcel = ParseExcel()

if __name__ == "__main__":
    bigList = []
    for i in range(nrows):
        dict = {}
        if i == 0:
            continue
        data = table.row_values(i)[1:2][0]
        # entity = table.row_values(i)[2:3][0]
        value = table.row_values(i)[3:4][0]
        dict["message"] = data
        dict["target"] = value
        bigList.append(dict)
        # print(bigList)
    try:
        resData = train(bigList)
    except:
        pass
    else:
        print(resData)