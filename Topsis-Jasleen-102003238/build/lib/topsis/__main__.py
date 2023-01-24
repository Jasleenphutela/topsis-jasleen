# Name=jasleen phutela
# Roll_no=102003238
import pandas as pd
import sys
import os
import math

try:
    def main():
        if len(sys.argv) != 5:
            raise Exception('Wrong Format, Write: python <program.py> <InputDataFile.csv> <Weights> <Impacts> <output.csv>')


        datafile = sys.argv[1]
        weights = sys.argv[2].split(',')
        impacts = sys.argv[3].split(',')
        outputfile = sys.argv[4]

        if not os.path.exists(datafile):
            raise Exception('File not Found!')

        df = pd.read_csv(datafile)
        if len(df.columns) < 3:
            raise Exception('Input file must contain 3 or more columns')

        col_names = list(df.columns[1:])
        for i in col_names:
            for j in df[i]:
                if not isinstance(j, int) and not isinstance(j, float):
                    raise Exception('Value not numeric')

        if len(col_names) != len(weights) or len(col_names) != len(impacts):
            raise Exception('Lengths of weights and impacts must be same as that of columns!')

        for i in impacts:
            if not i == '+' and not i == '-':
                raise Exception('Impacts can only be + or -')

        col_sum = []
        for i in col_names:
            col_sum.append(math.sqrt(df[i].pow(2).sum()))
        # print(col_sum)
        iter = 0
        for i in col_names:
            df.loc[:, i] = df.loc[:, i] / col_sum[iter]
            df.loc[:, i] = df.loc[:, i] * float(weights[iter])
            iter = iter + 1

        #print(df)
        v_pos = []
        v_neg = []

        iter = 0
        for i in col_names:
            if impacts[iter] == '+':
                v_pos.append(df[i].max())
                v_neg.append(df[i].min())
            else:
                v_neg.append(df[i].max())
                v_pos.append(df[i].min())
            iter = iter + 1
        # print(v_pos)
        # print(v_neg)
        s_pos = []
        s_neg = []

        for i in range(len(df)):
            iter = 0
            temp_sum_pos = 0
            temp_sum_neg = 0
            for j in range(1, len(df.loc[i])):

                temp_sum_pos = temp_sum_pos + (df.iloc[i, j] - v_pos[iter])*(df.iloc[i, j] - v_pos[iter])

                temp_sum_neg = temp_sum_neg + (df.iloc[i, j] - v_neg[iter])*(df.iloc[i, j] - v_neg[iter])

                iter = iter + 1
            s_pos.append(math.sqrt(temp_sum_pos))
            s_neg.append(math.sqrt(temp_sum_neg))
        # print(s_pos)
        # print(s_neg)
        performance = []
        for i in range(len(s_pos)):
            performance.append((s_neg[i]) / (s_neg[i] + s_pos[i]))
        # print(performance)
        df['Topsis Score'] = performance

        df['Rank'] = df['Topsis Score'].rank(ascending=0)
        df['Rank'] = df['Rank'].astype(int)

        df.to_csv(outputfile, index=False)


    if __name__ == '__main__':
        main()

except Exception as e:
    print(e)
