import streamlit as st
import boto3

#タイトル
st.subheader('串カツ田中')
st.subheader('料金シミュレーション')

dynamodb = boto3.resource('dynamodb',
                        region_name='us-east-1',
                        aws_access_key_id=st.secrets["ACCESS_KEY"],
                        aws_secret_access_key= st.secrets["SECRET_KEY"])
table = dynamodb.Table('TanakaMenuDB')
result = table.scan()
result = sorted(result["Items"], key=lambda x:x['Kind'])
order_list = {}

lcol, rcol = st.columns(2)
lcon = lcol.container()
rcon = rcol.container()

for i, item in enumerate(result, start=1):
    if i % 2 == 1:
        order_list[item["Menu"]] = lcon.number_input(item["Menu"] + "   " + item["Price"] + "円",0,100,0)
    else:
        order_list[item["Menu"]] = rcon.number_input(item["Menu"] + "   " + item["Price"] + "円",0,100,0)

with st.sidebar:
    total1 = 0
    total2 = 0
    total3 = 0
    total4 = 0
    calc_start = st.button("計算開始")
    if calc_start == True:
        for item in result:
            if order_list[item["Menu"]] != 0:
                total2 += int(item['Price']) * int(order_list[item["Menu"]])
                if item["Kind"] == "0":
                    total1 += 110 * int(order_list[item["Menu"]])
                    total3 += 110 * int(order_list[item["Menu"]])
                    total4 += int(item['Price']) * int(order_list[item["Menu"]])
                elif item["Kind"] == "2":
                    total1 += int(item['Price']) * int(order_list[item["Menu"]])
                    total3 += 250 * int(order_list[item["Menu"]])
                    total4 += 250 * int(order_list[item["Menu"]])
                else:
                    total1 += int(item['Price']) * int(order_list[item["Menu"]])
                    total3 += int(item['Price']) * int(order_list[item["Menu"]])
                    total4 += int(item['Price']) * int(order_list[item["Menu"]])
    st.write("元料金 ： " + str(total2) + "円")          
    st.write("① : 240円以下の串を110円にした場合")
    st.write(str(total1) + "円    (　" + str(total2 - total1) + "円得 )")
    st.write("② : 会計の合計を10％オフにした場合")
    st.write(str(int(total2 * 0.9)) + "円    (　" + str(int(total2 - total2 * 0.9)) + "円得 )")
    st.write("③ : ①と飲みpassと併用した場合")
    st.write(str(550 + total3) + "円    (　" + str(total2 - (550 +total3)) + "円得 )")
    st.write("④ : ②と飲みpassと併用した場合")
    st.write(str(int(550 + total4 * 0.9)) + "円    (　" + str(int(total2 - (550 + total4 * 0.9))) + "円得 )")