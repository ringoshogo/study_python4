import pandas as pd
from datetime import datetime as dt

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master
        self.order_total_price=0
        self.order_total_amount=0
        self.receipt = ""
    
    def add_item_order(self,item_code, item_count):
        # 課題4 オーダー時に個数も登録する
        self.item_order_list.append((item_code,item_count))
        
    def view_item_list(self):
        result = 0
        total_amount = 0
        index = 0

        # 返却用の文字列
        text = ""
        for item_code, item_count in self.item_order_list:
            index += 1
            try:
                item = list(filter(lambda item: item.item_code == item_code, self.item_master))[0]

                # 返却用の文字列に格納する
                text += f"===============================\n"
                text += f"商品コード:{item_code}\n"
                # 課題1 商品の一覧を表示する
                text += f"商品名:{item.item_name}\n"
                text += f"価格:{item.price}\n"
                text += f"数量:{item_count}\n"
                text += f"===============================\n"
                # 課題5 合計金額、個数を表示する    
                result += int(item.price) * int(item_count)
                total_amount += int(item_count)

                # レシートの作成

            except:
                print(f"アイテムコード:{item_code} が存在しません")
        
        text += f"合計{total_amount}個、金額は{result}円です。\n"
        self.order_total_price = result
        self.order_total_amount = total_amount

        return text



   
def __get_master() -> list:
    """マスタをオーダーに登録する"""
    item_master = []
    try:

        # 課題3 商品マスタをcsvファイルから読み込む
        # header = 0: 1行目をヘッダとして認識する
        # dtype = str: データタイプを文字列と認識してくれる：0埋めなど
        item_master_csv = pd.read_csv("item_master.csv", header=0, dtype=str).values.tolist()
        print(item_master_csv)

        # csvマスタをアイテムに登録する
        for item in item_master_csv:
            item_master.append(Item(item[0], item[1], item[2]))

    except pd.errors.EmptyDataError:
        print("No columns to parse from file")
        return []

    return item_master

### メイン処理
def main():
    # マスタ登録
    # item_master=[]
    # item_master.append(Item("001","りんご",100))
    # item_master.append(Item("002","なし",120))
    # item_master.append(Item("003","みかん",150))

    # オーダーにアイテムマスタを登録する    
    order=Order(__get_master())

    # オーダー登録
    while True:
        
        # 課題2 オーダーをコンソールから登録する
        item_order = input("登録する商品コードを入力してください。>>")
        # 課題4 オーダー時に個数も登録する
        item_order_count = input("登録する個数を入力してください。>>")

        # アイテムマスタに存在しない場合はオーダーに登録しない
        if item_order in list(map(lambda x: x.item_code, order.item_master)):
            order.add_item_order(item_order, item_order_count)

        else:
            print("アイテムマスタに存在しません。")
    
        hasNext = input("追加で入力しますか？>> y/n :")

        if hasNext != "y" and hasNext != "Y":
            break

    # オーダー表示
    text = order.view_item_list()

    # お客様から金額を貰い、おつりを計算する
    text += __calculate_customer_payment(order)

    __output_receipt(text)

def __output_receipt(text: str):
    """レシートをテキストファイルに出力する"""
    filename = dt.now().strftime('%Y%m%d%H%M%S')
    with open(f"../receipt/{filename}.txt", encoding="utf-8_sig", mode="w") as f:
        f.write(text)
         


def __calculate_customer_payment(order: Order):
    """お客様からのお預かり金額を計算する"""
    # お客様からお預かりを貰う
    pay_amount = input("お預かり金額を入力してください(円)>>")

    # 返却用の文字列
    text = ""

    # 課題6 お客様からお預かり金額を入力しおつりを計算
    if pay_amount.isdigit():

        # 不足している場合
        if int(pay_amount) < order.order_total_price:
            text += "お預かり金額が不足しております。\n"
        elif int(pay_amount) == order.order_total_price:
            text += "ちょうどお預かり致します。\n"

        else:
            rest_amount =int(pay_amount) - order.order_total_price
            text += f"おつりは{rest_amount}円です。\n"

        return text
    else:
        print("数字を入力してください。")
        return ""

    
if __name__ == "__main__":
    main()