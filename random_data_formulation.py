import pandas as pd
from decimal import *
getcontext().prec = 15



# Constants
Phi = Decimal('1')
Q = Decimal('500')
M = Decimal('1')
R = Decimal('10000')


# Calculates X_bat, C_cat, X_cat
def rate_and_others(B_t= Decimal('8945.7') , X_bat= Decimal('1000'), X_cat = Decimal('10735'), K=Decimal('0.802')):
    X_bat = X_cat * Phi
    C_cat = X_bat * M
    X_cat = X_bat + K * (B_t - C_cat)

    if B_t == 0:
        rate = 'inf'
    else:
        rate = (B_t - X_cat) / B_t
    return X_bat, C_cat, X_cat, rate


# Calculates P, P_bat, K
def middle(P):
    P_bat = P * (Phi ** 2) + Q
    K = M * P_bat * (P_bat * (1 ** 2) + R) ** -1
    P = P_bat * (1 - K * M) ** 2 + (R * K ** 2)
    return P, P_bat, K


def random_data_formulation(bt_df, P=Decimal('40000')):
    X_bat = Decimal('1000')
    X_cat = Decimal('10735')
    bts = [Decimal(bt) for bt in bt_df['Bt']]

    for b_t in bts:
       P, P_bat, K = middle(P)
       X_bat, C_cat, X_cat, rate =  rate_and_others(b_t, X_bat, X_cat, K )

       P_col.append(float(P,))
       P_bat_col.append(float(P_bat))
       K_col.append(float(K))
   
       C_cat_col.append(float(C_cat,))
       X_bat_col.append(float(X_bat))
       X_cat_col.append(float(X_cat))
       rate_col.append(round(float(rate), 4))


if __name__ == '__main__':
    # Reading csv file containing Bt data
    # Creating empty lists to store the generated data
    bt_df = pd.read_csv('Bt_Data.csv')
    print(bt_df.columns)
    P_col = []
    P_bat_col = []
    K_col = []
    X_bat_col = []
    C_cat_col = []
    X_cat_col = []
    rate_col = []
    
    # Calling the function to generate all data
    random_data_formulation(bt_df=bt_df)

    # Appending data to new columns
    bt_df['P'] = P_col
    bt_df['P_bat'] = P_bat_col
    bt_df['K'] = K_col
    bt_df['C_cat'] = C_cat_col
    bt_df['X_bat'] = X_bat_col
    bt_df['X_cat'] = X_cat_col
    bt_df['rate'] = rate_col

    # Writing a new csv with new data
    bt_df.to_csv('sevenhundred.csv')
    print("Successful!")
    
