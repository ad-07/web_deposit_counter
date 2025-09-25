import streamlit as st
import plotly.graph_objects as go





def simulate(depo, salary, perc, promotion, investment, months, check):
    balance = []
    current_salary = salary
    current = depo
    for m in range(1, months + 1):
        current += current_salary * perc
        current *= 1 + investment / 12
        if check and m % 12 == 0:  # 13-я зарплата
            current += current_salary
        if m % 12 == 0:
            current_salary *= 1 + promotion
        balance.append(current)
    return balance
# Заголовок

st.title("Сколько ты накопишь?(или не накопишь))")
# Текст
st.write("Привет! Войди в средний класс")

st.write("40 квадратов на члена семьи и две машины, одна из которых иномарка")
st.header("Ввод данных")
# Ввод текста
depo = st.number_input("Сколько у тебя денег есть(не ноль же?)", min_value=0.0, value=0.0, step=10000.0)
st.write("Вы ввели:", f"{depo:,.0f}".replace(",", " "))
salary = st.number_input("Сколько ты зарабатываешь(янезарабат...)", min_value=0.0, value=0.0, step=1000.0)
st.write("Вы ввели:", f"{salary:,.0f}".replace(",", " "))
perc = st.number_input("сколько процентов хочешь откладывать?", min_value=0.0, value=0.0, step=1.0)/100
promotion = st.number_input("раз в год доход же повышаешь или нет? на сколько в среднем? (%)", min_value=0.0, value=0.0, step=0.1)/100
investment = st.number_input("если че деньги надо вкладывать, сколько процентов имеешь в год? (%)", min_value=0.0, value=0.0, step=0.1) /100
months = st.slider("Сколько месяцев копить будем?", 0, 500, 12)


goal = st.number_input("Желаемая сумма накоплений", min_value=0.0, value=1_000_000.0, step=1000.0)





check = st.toggle("13 зарпалту считаем?")


# Бинарный поиск необходимого процента откладывания
low, high = 0.0, 1.0
for _ in range(40):
    mid = (low + high) / 2
    b = simulate(depo, salary, mid, promotion, investment, months, check)
    if b[-1] >= goal:
        high = mid
    else:
        low = mid
needed_perc = high * 100  # в процентах
st.info(f"Чтобы достичь цели: нужно откладывать {needed_perc:.2f}% от зарплаты каждый месяц")

balance = []
current = depo
current_salary = salary
for m in range(1, months + 1):
    current += current_salary * perc
    current *= 1 + investment / 12
    if check and m % 12 == 0:  # 13-я зарплата
        current += current_salary
    if m % 12 == 0:  # повышение
        current_salary *= 1 + promotion
    balance.append(current)

final = balance[-1]  # итог совпадает с последним значением графика
formatted = f"{final:,.2f}".replace(",", " ").replace(".", ",")

st.header("Результаты")
if st.button("Ну сколько деняг?"):
    st.success(f"{formatted} ₽!, нормально по идее")


balance = simulate(depo, salary, perc, promotion, investment, months, check)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=list(range(1, months + 1)),
    y=balance,
    mode='lines+markers',
    name='Накопления'
))
fig.add_trace(go.Scatter(
    x=[1, months],
    y=[goal, goal],
    mode='lines',
    name='Цель',
    line=dict(dash='dash', color='red')
))
fig.update_layout(title="Рост накоплений и цель",
                  xaxis_title="Месяц",
                  yaxis_title="Сумма",
                  yaxis=dict(tickformat=','))
st.plotly_chart(fig)



# Слайдер

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
