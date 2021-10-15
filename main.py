import streamlit as st
import boto3

#タイトル
st.subheader('串カツ田中料金シミュレーション')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TanakaMenuDB')
result = table.scan()
result = sorted(result["Items"], key=lambda x:x['Kind'])
order_list = {}
for item in result:
    order_list[item["Menu"]] = st.number_input(item["Menu"] + "   " + item["Price"] + "円",0,100,0)

with st.sidebar:
    total1 = 0
    total2 = 0
    calc_start = st.button("計算開始")
    if calc_start == True:
        for item in result:
            if order_list[item["Menu"]] != 0:
                total2 += int(item['Price']) * int(order_list[item["Menu"]])
                if item["Kind"] == "0":
                    total1 += 110 * int(order_list[item["Menu"]])
                else:
                    total1 += int(item['Price']) * int(order_list[item["Menu"]])
    st.write("240円以下の串を110円にした場合：")
    st.write(str(total1) + "円")
    st.write("会計の合計を10％オフにした場合：")
    st.write(str(int(total2 * 0.9)) + "円")