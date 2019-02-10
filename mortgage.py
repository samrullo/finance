import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def generate_mortgage_schedule(mortgage=30000000, term=35, ir=2.5, start=datetime.date(2019, 4, 1)):
    """
    Monthly mortgage payments, discounted at the monthly compounded mortgage rate, equals the
    original amount borrowed.

    :param mortgage:
    :param term:
    :param ir:
    :return:
    """
    discount_rates = []
    periods = np.arange(1, term * 12 + 1)
    for p in periods:
        discount_rates.append(1 / (1 + ir * 0.01 / 12) ** p)

    discount_rates = np.array(discount_rates)

    monthly_mortgage_payment = mortgage / np.sum(discount_rates)
    df = pd.DataFrame(
        columns=['date', 'monthly_payment', 'monthly_interest', 'monthly_principal', 'paid_down_principal',
                 'remaining_principal', 'total_ir_paid'], index=periods)

    remaining_principal = mortgage
    paid_down_principal = 0
    total_ir_paid = 0
    df['monthly_payment'] = monthly_mortgage_payment
    for i, row in df.iterrows():
        monthly_ir = remaining_principal * ir * 0.01 / 12
        monthly_principal = monthly_mortgage_payment - monthly_ir
        paid_down_principal += monthly_principal
        total_ir_paid += monthly_ir
        remaining_principal -= monthly_principal
        df.loc[i, 'date'] = start + datetime.timedelta(30) * i
        df.loc[i, 'monthly_principal'] = monthly_principal
        df.loc[i, 'monthly_interest'] = monthly_ir
        df.loc[i, 'remaining_principal'] = remaining_principal
        df.loc[i, 'paid_down_principal'] = paid_down_principal
        df.loc[i, 'total_ir_paid'] = total_ir_paid
    df['monthly_principal'].plot(label='monthly_principal')
    df['monthly_interest'].plot(label='monthly_interest')
    plt.title("Monthly principal and monthly interest plotted")
    plt.xlabel('periods')
    plt.ylabel('JPY')
    plt.show()
    return df


df = generate_mortgage_schedule()
