import pandas as pd

def onClickSave(df, date, syumoku, weight, rep, set, rm):
    s_no_name = pd.Series([date, syumoku, weight, rep, set, rm], index=['date', 'syumoku', 'weight', 'rep', 'set', 'rm'])

    df = df.append(s_no_name, ignore_index=True)

    # df.loc[date] = 0
    print(df)
    df.to_csv("weight_list.csv")
    return df
