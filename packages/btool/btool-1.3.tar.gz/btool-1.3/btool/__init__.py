import pandas as pd
import numpy as np
import multiprocessing as mp
import seaborn as sns
import matplotlib.pyplot as plt

def cal_bband_performance(df, direction, days, cost, output_csv):

    if direction == 'bnh':
        df[f'{direction}_pnl'] = df['change']    # need to adjust the range
    else:
        df[f'{direction}_trade'] = abs(df[f'{direction}'] - df[f'{direction}'].shift(1))
        df[f'{direction}_cost'] = df[f'{direction}_trade'] * cost / 100
        df[f'{direction}_pnl'] = df[f'{direction}'].shift(1) * df['change'] - df[f'{direction}_cost']

    if output_csv:
        df.to_csv(f'result/{direction}.csv')

    sharpe = df[f'{direction}_pnl'].mean() / df[f'{direction}_pnl'].std() * np.sqrt(days)
    sharpe = round(sharpe, 2)
    pnl = round(df[f'{direction}_pnl'].sum(), 2)
    annual_return = round(df[f'{direction}_pnl'].mean() * days, 2)

    df_dd = pd.DataFrame()
    df_dd['cumu'] = df[f'{direction}_pnl'].cumsum()
    df_dd['dd'] = df_dd['cumu'].cummax() - df_dd['cumu']
    mdd = round(df_dd['dd'].max(), 3)


    if mdd == 0:
        calmar = 0
    else:
        calmar = round(annual_return / mdd, 2)

    if direction == 'bnh':
        num_trades = 0
    else:
        df_dd['PriceDiff'] = df[f'{direction}'].diff()
        num_trades = len(df_dd[(df_dd['PriceDiff'] == 1) | (df_dd['PriceDiff'] == -1)])

    if output_csv:
        df_dd.to_csv(f'result/{direction}_dd.csv')

    return sharpe, pnl, annual_return, mdd, calmar, num_trades, df_dd

def mp_bband(tuple_data):
    parameters = tuple_data[0]
    df = tuple_data[1]
    result_list = tuple_data[2]

    # print(parameters)
    framework = parameters['framework']
    factor = parameters['factor']
    rolling = parameters['rolling']
    threshold = parameters['threshold']
    strategy = parameters['strategy']
    days = parameters['days']
    cost = parameters['cost']

    df['ma'] = df[factor].rolling(rolling).mean()


    if framework == 'bband':
        df['sd'] = df[factor].rolling(rolling).std()
        df['z'] = (df[factor] - df['ma']) / df['sd']
    elif framework == 'abs':
        df['z'] = df['ma']



    df['above_thres'] = df['z'] > threshold
    df['below_thres'] = df['z'] < -threshold

    ### Generate one backtest only
    if parameters['one_only']:
        long_short = parameters['long_short']
        if strategy == 'momentum':
            if long_short == 'long':
                df['ml'] = df['above_thres'].astype(int)
            elif long_short == 'short':
                df['ms'] = df['below_thres'].astype(int) * -1
        elif strategy == 'revision':
            if long_short == 'long':
                df['rl'] = df['below_thres'].astype(int)
            elif long_short == 'short':
                df['rs'] = df['above_thres'].astype(int) * -1

        return df
    ### Generate one backtest only


    if strategy == 'momentum':
        directions = ['ml', 'ms']
        df['ml'] = df['above_thres'].astype(int)
        df['ms'] = df['below_thres'].astype(int) * -1
    elif strategy == 'revision':
        directions = ['rl', 'rs']
        df['rl'] = df['below_thres'].astype(int)
        df['rs'] = df['above_thres'].astype(int) * -1

    for direction in directions:
        sharpe, pnl, annual_return, mdd, calmar, num_trades, df_dd = cal_bband_performance(df, direction, days, cost, False)
        result_list.append([direction, rolling, threshold, sharpe, pnl, annual_return, mdd, calmar, num_trades])


def bband(bband_parameters, data_freq='1D', show_pic=True, save_pic=True, pic_name='output',
          result_folder='result', output_csv=False):
    if data_freq == '1D':
        days = 252
    elif data_freq == '1H':
        days = 24 * 252
    elif data_freq == '1W':
        days = 52
    elif data_freq == '1m':
        days = 60 * 24 * 252



    framework = bband_parameters['framework']
    factor = bband_parameters['factor']
    try:
        cost = bband_parameters['cost']
    except:
        cost = 0.05
    mode = bband_parameters['mode']

    print('mode', mode)
    print('factor:', factor)
    print('data_freq:', data_freq)
    print('cost:', f'{cost}%')
    print()

    if (mode == 'heatmap') or (mode =='single_heatmap'):


        if mode == 'heatmap':
            df = bband_parameters['dataframe']

            momentum_rollings = bband_parameters['momentum_rollings']
            momentum_thresholds = bband_parameters['momentum_thresholds']

            revision_rollings = bband_parameters['revision_rollings']
            revision_thresholds = bband_parameters['revision_thresholds']

            mp_tuple = []
            count = 0
            result_list = mp.Manager().list()  # To save the result with index number

            ### Momentum
            for rolling in momentum_rollings:
                for threshold in momentum_thresholds:
                    # print(rolling, threshold)
                    count = count + 1
                    mp_tuple.append(({
                                         'framework': framework,
                                         'rolling': rolling,
                                         'threshold': threshold,
                                         'strategy': 'momentum',
                                         'factor': factor,
                                         'days': days,
                                         'cost': cost,
                                         'one_only': False},
                                     df,
                                     result_list))

            ### Revision
            for rolling in revision_rollings:
                for threshold in revision_thresholds:
                    # print(rolling, threshold)
                    count = count + 1
                    mp_tuple.append(({
                                         'framework': framework,
                                         'rolling': rolling,
                                         'threshold': threshold,
                                         'strategy': 'revision',
                                         'factor': factor,
                                         'days': days,
                                         'cost': cost,
                                         'one_only': False},
                                     df,
                                     result_list))

            pool = mp.Pool(processes=8)
            pool.map(mp_bband, mp_tuple)
            pool.close()

            colums = ['direction', 'ma', 'thres', 'sharpe', 'pnl', 'ann_return', 'mdd', 'calmar', 'num_trade']
            df = pd.DataFrame(list(result_list), columns=colums)

            data1 = df[df['direction'] == 'ml'][['ma', 'thres', 'sharpe']].copy().pivot(index='ma', columns='thres',
                                                                                        values='sharpe')
            data2 = df[df['direction'] == 'ms'][['ma', 'thres', 'sharpe']].copy().pivot(index='ma', columns='thres',
                                                                                        values='sharpe')
            data4 = df[df['direction'] == 'rl'][['ma', 'thres', 'sharpe']].copy().pivot(index='ma', columns='thres',
                                                                                        values='sharpe')
            data5 = df[df['direction'] == 'rs'][['ma', 'thres', 'sharpe']].copy().pivot(index='ma', columns='thres',
                                                                                        values='sharpe')

            fig, axes = plt.subplots(2, 2, figsize=(15, 10))

            sns.heatmap(data1, cmap='Greens', ax=axes[0, 0], annot=True, annot_kws={"fontsize": 8}, fmt="g")
            axes[0, 0].set_title('Momentum Long')
            axes[0, 0].tick_params(axis='both', labelsize=8)

            sns.heatmap(data2, cmap='Greens', ax=axes[0, 1], annot=True, annot_kws={"fontsize": 8}, fmt="g")
            axes[0, 1].set_title('Momentum Short')
            axes[0, 1].tick_params(axis='both', labelsize=8)

            sns.heatmap(data4, cmap='Greens', ax=axes[1, 0], annot=True, annot_kws={"fontsize": 8}, fmt="g")
            axes[1, 0].set_title('Revision Long')
            axes[1, 0].tick_params(axis='both', labelsize=8)

            sns.heatmap(data5, cmap='Greens', ax=axes[1, 1], annot=True, annot_kws={"fontsize": 8}, fmt="g")
            axes[1, 1].set_title('Revision Short')
            axes[1, 1].tick_params(axis='both', labelsize=8)

            plt.subplots_adjust(top=0.5)  # Adjust the top margin for the title
            plt.suptitle(f'{pic_name}', fontsize=16)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)

            plt.tight_layout()

            if save_pic:
                plt.savefig(f'{result_folder}/heatmap_{pic_name}.png')

        else:
            df = bband_parameters['dataframe']
            direction = bband_parameters['direction']

            mp_tuple = []
            count = 0
            result_list = mp.Manager().list()  # To save the result with index number

            if (direction == 'ml') or (direction == 'ms'):
                momentum_rollings = bband_parameters['momentum_rollings']
                momentum_thresholds = bband_parameters['momentum_thresholds']
                ### Momentum
                for rolling in momentum_rollings:
                    for threshold in momentum_thresholds:
                        # print(rolling, threshold)
                        count = count + 1
                        mp_tuple.append(({
                                             'framework': framework,
                                             'rolling': rolling,
                                             'threshold': threshold,
                                             'strategy': 'momentum',
                                             'factor': factor,
                                             'days': days,
                                             'cost': cost,
                                             'one_only': False},
                                         df,
                                         result_list))
            else:

                revision_rollings = bband_parameters['revision_rollings']
                revision_thresholds = bband_parameters['revision_thresholds']

                ### Revision
                for rolling in revision_rollings:
                    for threshold in revision_thresholds:
                        # print(rolling, threshold)
                        count = count + 1
                        mp_tuple.append(({
                                             'framework': framework,
                                             'rolling': rolling,
                                             'threshold': threshold,
                                             'strategy': 'revision',
                                             'factor': factor,
                                             'days': days,
                                             'cost': cost,
                                             'one_only': False},
                                         df,
                                         result_list))

            pool = mp.Pool(processes=8)
            pool.map(mp_bband, mp_tuple)
            pool.close()

            colums = ['direction', 'ma', 'thres', 'sharpe', 'pnl', 'ann_return', 'mdd', 'calmar', 'num_trade']
            df = pd.DataFrame(list(result_list), columns=colums)

            titles = {
                'ml' : 'Momentum Long',
                'ms': 'Momentum Short',
                'rl': 'Revision Long',
                'rs': 'Revision Short',
            }

            sharpe_data = df[df['direction'] == direction][['ma', 'thres', 'sharpe']].copy().pivot(index='ma', columns='thres',
                                                                                        values='sharpe')
            ann_return_data = df[df['direction'] == direction][['ma', 'thres', 'ann_return']].copy().pivot(index='ma', columns='thres',
                                                                                        values='ann_return')
            mdd_data = df[df['direction'] == direction][['ma', 'thres', 'mdd']].round(2).copy().pivot(index='ma',
                                                                                                           columns='thres',
                                                                                                           values='mdd')
            num_trade_data = df[df['direction'] == direction][['ma', 'thres', 'num_trade']].copy().pivot(index='ma',
                                                                                                      columns='thres',
                                                                                                      values='num_trade')

            fig, axes = plt.subplots(2, 2, figsize=(15, 10))

            sns.heatmap(sharpe_data, cmap='Greens', ax=axes[0, 0], annot=True, annot_kws={"fontsize": 8}, fmt="g")
            axes[0,0].set_title(f'{titles[direction]} Sharpe')
            axes[0,0].tick_params(axis='both', labelsize=8)

            sns.heatmap(ann_return_data, cmap='Blues', ax=axes[0, 1], annot=True, annot_kws={"fontsize": 8}, fmt="g")
            axes[0,1].set_title(f'{titles[direction]} Ann Return')
            axes[0,1].tick_params(axis='both', labelsize=8)

            sns.heatmap(mdd_data, cmap='OrRd', ax=axes[1, 0], annot=True, annot_kws={"fontsize": 8}, fmt="g")
            axes[1,0].set_title(f'{titles[direction]} MDD')
            axes[1,0].tick_params(axis='both', labelsize=8)

            sns.heatmap(num_trade_data, cmap='Purples', ax=axes[1, 1], annot=True, annot_kws={"fontsize": 8}, fmt="g")
            axes[1,1].set_title(f'{titles[direction]} Num of Trade')
            axes[1,1].tick_params(axis='both', labelsize=8)

            plt.subplots_adjust(top=0.5)  # Adjust the top margin for the title
            plt.suptitle(f'{pic_name}', fontsize=16)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)

            plt.tight_layout()

            if save_pic:
                plt.savefig(f'{result_folder}/single_headmap_{direction}_{pic_name}.png')



        if show_pic:
            plt.show()


    elif mode == 'equity_curve':
        df = bband_parameters['dataframe']

        s1 = bband_parameters['s1']
        s2 = bband_parameters['s2']

        result_list = mp.Manager().list()  # To save the result with index number

        df_csv = df.copy()
        df_combine = pd.DataFrame()
        df_combine['date'] = df_csv['date']
        df_combine['change'] = df_csv['change']
        text = ''

        plt.figure(figsize=(15, 10))

        ### bnh
        df = df_csv.copy()
        sharpe, pnl, annual_return, mdd, calmar, num_trades, df_dd = cal_bband_performance(df, 'bnh', days, cost, output_csv)
        bnh_text = f'BnH Sharpe:{sharpe} Pnl:{pnl} Annual Return:{annual_return} MDD:{round(mdd * 100)}% Calmar: {calmar} \n\n'
        df_bnh = df_dd.copy()

        ### Strategy 1
        direction, rolling, threshold = s1
        long_short = 'long' if direction[1] == 'l' else 'short'
        strategy = 'momentum' if direction[0] == 'm' else 'revision'

        df = df_csv.copy()
        df = mp_bband(({'framework': framework, 'rolling': rolling, 'threshold': threshold, 'strategy': strategy, 'long_short': long_short,
                     'factor': factor, 'days': days, 'cost':cost, 'one_only': True},
                    df, result_list))
        df_combine[direction] = df[direction].copy()

        sharpe, pnl, annual_return, mdd, calmar, num_trades, df_dd = cal_bband_performance(df, direction, days, cost, output_csv)
        text = text + f'S1  Sharpe:{sharpe} Pnl:{pnl} Annual Return:{annual_return} MDD:{round(mdd * 100)}% Calmar: {calmar} Trades: {num_trades} \n\n'

        plt.subplot(2, 2, 1)
        plt.xticks(rotation=90)
        plt.title(f'S1 {framework} {strategy} {long_short} {rolling} {threshold}')
        plt.plot(df_csv['date'], df_dd.copy()['cumu'], label='Strategy', linestyle='-', color='blue')
        plt.plot(df_csv['date'], df_bnh['cumu'], label='BnH', linestyle='-', color='red')

        ### Strategy 2
        direction, rolling, threshold = s2
        long_short = 'long' if direction[1] == 'l' else 'short'
        strategy = 'momentum' if direction[0] == 'm' else 'revision'

        df = df_csv.copy()
        df = mp_bband(({'framework': framework, 'rolling': rolling, 'threshold': threshold, 'strategy': strategy, 'long_short': long_short,
                     'factor': factor, 'days': days, 'cost':cost, 'one_only': True},
                    df, result_list))
        df_combine[direction] = df[direction].copy()

        sharpe, pnl, annual_return, mdd, calmar, num_trades, df_dd = cal_bband_performance(df, direction, days, cost, output_csv)
        text = text + f'S2  Sharpe:{sharpe} Pnl:{pnl} Annual Return:{annual_return} MDD:{round(mdd * 100)}% Calmar: {calmar} Trades: {num_trades} \n\n'

        plt.subplot(2, 2, 3)
        plt.xticks(rotation=90)
        plt.title(f'S2 {framework} {strategy} {long_short} {rolling} {threshold}')
        plt.plot(df_csv['date'], df_dd.copy()['cumu'], label='Strategy', linestyle='-', color='blue')
        plt.plot(df_csv['date'], df_bnh['cumu'], label='BnH', linestyle='-', color='red')

        ### Check Duplication
        #  = pd.concat(dfs, axis=1)
        result_df = df_combine[(df_combine[s1[0]] != 0) & (df_combine[s2[0]] != 0)].drop('change', axis=1).copy()
        result_df['date'] = result_df['date'].dt.strftime('%Y-%m-%d')
        result_df.reset_index(drop=True, inplace=True)
        text_duplicate = ''
        separator = " "
        if len(result_df) > 0:
            print('Duplication Action')
            print(result_df)
            print()
            text_duplicate = text_duplicate + separator.join(result_df.columns) + '\n'
            print(text_duplicate)
            for i in result_df.index:
                # df.iloc[i].astype(str)
                result = result_df.iloc[i].apply(lambda x: str(x)).str.cat(sep=' ')
                text_duplicate = text_duplicate + result + '\n'
                print()

        ### Combine
        df_combine['combine'] = df_combine[s1[0]] | df_combine[s2[0]]

        sharpe, pnl, annual_return, mdd, calmar, num_trades, df_dd = cal_bband_performance(df_combine, 'combine', days, cost, output_csv)
        text = text + f'S12  Sharpe:{sharpe} Pnl:{pnl} Annual Return:{annual_return} MDD:{round(mdd * 100)}% Calmar: {calmar} Trades: {num_trades} \n\n'

        plt.subplot(2, 2, 2)
        plt.xticks(rotation=90)
        plt.title(f'Combine')
        plt.plot(df_csv['date'], df_dd.copy()['cumu'], label='Strategy', linestyle='-', color='blue')
        plt.plot(df_csv['date'], df_bnh['cumu'], label='BnH', linestyle='-', color='red')

        ### Performance
        plt.subplot(2, 2, 4)
        plt.xticks([])
        plt.yticks([])

        # start_str = df_csv.reset_index().at[0,'date'].strftime('%Y%m%d')
        # end_str = df_csv.reset_index().at[len(df_csv)-1,'date'].strftime('%Y%m%d')

        text = f'{pic_name}_{factor}\n\n' + text + bnh_text + text_duplicate

        print(text)

        h = 0.5 - len(result_df) * 0.1
        plt.text(0.01, h, text, fontsize=11, bbox={'facecolor': 'none', 'edgecolor': 'none'})
        plt.tight_layout()
        if save_pic:
            plt.savefig(f'result/{pic_name}_{factor}_{s1[0]}_{s1[1]}_{s1[2]}_{s2[0]}_{s2[1]}_{s2[2]}.png')

        if show_pic:
            plt.show()




    elif mode == 'single_equity_curve':

        df = bband_parameters['dataframe']

        s1 = bband_parameters['s1']

        output_single_csv = output_csv

        output_csv = False

        result_list = mp.Manager().list()  # To save the result with index number

        df_csv = df.copy()
        df_combine = pd.DataFrame()
        df_combine['date'] = df_csv['date']
        df_combine['change'] = df_csv['change']
        text = ''

        plt.figure(figsize=(15, 6))

        ### bnh
        df = df_csv.copy()
        sharpe, pnl, annual_return, mdd, calmar, num_trades, df_dd = cal_bband_performance(df, 'bnh', days, cost, output_csv)
        try:
            bnh_text = f'BnH Sharpe:{sharpe} Pnl:{pnl} Annual Return:{annual_return} MDD:{round(mdd * 100)}% Calmar: {calmar} \n\n'
        except:
            bnh_text = ''
        df_bnh = df_dd.copy()

        ### Strategy 1
        direction, rolling, threshold = s1
        long_short = 'long' if direction[1] == 'l' else 'short'
        strategy = 'momentum' if direction[0] == 'm' else 'revision'

        df = df_csv.copy()
        df = mp_bband(({'framework': framework, 'rolling': rolling, 'threshold': threshold, 'strategy': strategy, 'long_short': long_short,
                     'factor': factor, 'days': days, 'cost':cost, 'one_only': True},
                    df, result_list))

        print(df)


        df_combine[direction] = df[direction].copy()


        sharpe, pnl, annual_return, mdd, calmar, num_trades, df_dd = cal_bband_performance(df, direction, days, cost, output_csv)
        text = text + f'S1   Sharpe:{sharpe} Pnl:{pnl} Annual Return:{annual_return} MDD:{round(mdd * 100)}% Calmar: {calmar} Trades: {num_trades} \n\n'

        plt.subplot(1, 2, 1)
        plt.xticks(rotation=90)
        plt.title(f'{framework} {strategy} {long_short} {rolling} {threshold}')
        plt.plot(df_csv['date'], df_dd.copy()['cumu'], label='Strategy', linestyle='-', color='blue')
        plt.plot(df_csv['date'], df_bnh['cumu'], label='BnH', linestyle='-', color='red')




        ### Calculate strategy details
        def pnl(row):
            # print(row['date'])
            if row[f'{pnl.direction}_trade'] == 1:
                if pnl.pos == 0:
                    pnl.current_trade = []
                    pnl.current_trade.append(row.date)
                    pnl.pnl = 0
                    pnl.pos = 1

                elif pnl.pos == 1:
                    pnl.current_trade.append(row.date)
                    pnl.pnl = pnl.pnl + row[f'{direction}_pnl']
                    pnl.current_trade.append(pnl.pnl)
                    pnl.trades.append(pnl.current_trade.copy())
                    pnl.pos = 0

            pnl.pnl = pnl.pnl + row[f'{direction}_pnl']

        pnl.pos = 0
        pnl.direction = direction
        pnl.trades = []
        pnl.pnl = 0

        df.apply(pnl, axis=1)

        colums = ['start_date', 'end_date', 'pnl']
        df_trade = pd.DataFrame(pnl.trades, columns=colums)
        df_trade['start_date'] = pd.to_datetime(df_trade['start_date'])
        df_trade['end_date'] = pd.to_datetime(df_trade['end_date'])
        df_trade['days'] = (df_trade['end_date'] - df_trade['start_date']).dt.days

        df_trade['year'] = df_trade['start_date'].dt.year

        df_years = df_trade['year'].value_counts().reset_index().sort_values(by='year', ascending=True)
        df_years.columns = ['year', 'count']
        # print(df_years)

        df_pnl = df_trade.groupby('year')['pnl'].sum().reset_index().sort_values(by='year', ascending=True)
        # print(df_pnl)

        df_positive_pnl_counts = df_trade[df_trade['pnl'] > 0].groupby('year')['pnl'].count().reset_index().sort_values(by='year', ascending=True)
        df_positive_pnl_counts.columns = ['year', 'positive_pnl_count']
        # print(df_positive_pnl_counts)

        p_dict = pd.concat([df_years.set_index('year', drop=True), df_pnl.set_index('year', drop=True), df_positive_pnl_counts.set_index('year', drop=True)], axis=1).reset_index().to_dict(orient='records')
        # print(df_by_year.to_dict(orient='records'))


        df['date'] = pd.to_datetime(df['date'])
        min_date = df['date'].min()
        max_date = df['date'].max()
        years_difference = (max_date - min_date).days / 365.25  # Divide by 365.25 for leap years

        trade_per_year = len(df_trade) / years_difference

        average_holding_day = df_trade['days'].mean()

        win_rate = (df_trade['pnl'] > 0).sum() / len(df_trade)

        details_text = ''
        details_text = details_text + 'Strategy Performance \n'
        details_text = details_text + f'Trade per year : {round(trade_per_year, 1)} \n'
        details_text = details_text + f'Average Holding Days: {round(average_holding_day, 1)} \n'
        details_text = details_text + f'Win Rate: {round(win_rate * 100, 1)}% \n\n'
        details_text = details_text + f'Year     Pnl   Count   Win Rate \n'
        for p in p_dict:
            details_text = details_text + f"{p['year']}    {round(p['pnl'], 2)}    {p['count']}    {round(p['positive_pnl_count']/p['count']*100,1)}% \n"






        ### Performance
        plt.subplot(1, 2, 2)
        plt.xticks([])
        plt.yticks([])

        # start_str = df_csv.reset_index().at[0,'date'].strftime('%Y%m%d')
        # end_str = df_csv.reset_index().at[len(df_csv)-1,'date'].strftime('%Y%m%d')

        text = f'{pic_name}\n\n' + text + bnh_text + details_text# + text_duplicate

        print(text)

        h = 0.6 - len(p_dict) * 0.05
        plt.text(0.01, h, text, fontsize=11, bbox={'facecolor': 'none', 'edgecolor': 'none'})
        plt.tight_layout()
        if save_pic:
            plt.savefig(f'result/equity_curve_{s1[0]}_{s1[1]}_{s1[2]}_{pic_name}.png')

        if output_single_csv:
            df.to_csv(f'result/df_equity_curve_{s1[0]}_{s1[1]}_{s1[2]}_{pic_name}.csv')
            df_trade.to_csv(f'result/trades_equity_curve_{s1[0]}_{s1[1]}_{s1[2]}_{pic_name}.csv')

        if show_pic:
            plt.show()

def run():
    ###

    file_name = input('File name? \n')
    print()
    date_column = input('Date Column? \n')
    print()
    close_column = input('Price Close Column? \n')
    print()
    factor = input('Factor Column? \n')
    print()

    # file_name = 'data.csv'
    # date_column = 'date'vhsi
    # close_column = 'close'
    # factor = 'close'

    file_path = file_name
    df_csv = pd.read_csv(file_path)
    df_csv['date'] = pd.to_datetime(df_csv[date_column])
    df_csv['close'] = df_csv[close_column]
    df_csv['factor'] = df_csv[factor]
    df_csv = df_csv[['date', 'close', 'factor']]

    # Clean Data
    df_csv = df_csv.sort_values(by='date')
    df_csv = df_csv.fillna(method='ffill')
    df_csv['close'] = df_csv['close'].replace(0, method='ffill')
    df_csv['factor'] = df_csv['factor'].replace(0, method='ffill')

    # print('Last 5 rows')
    # print(df_csv.tail(5))
    # print()


    ### Ask Mode
    mode = input('Mode? heatmap / single_heatmap / single_equity_curve \n')
    if not ((mode == 'heatmap') or (mode == 'single_heatmap') or (mode == 'single_equity_curve')):
        print('Error')
        exit()
    print('Mode:',mode)
    print()


    ### Ask Date
    date_mode = input('Single or Moving Date? single / moving \n')
    if date_mode == 'single':
        print()
        start_date = input('Start Date? (yyyymmdd) \n')
        print()
        end_date = input('End Date? (yyyymmdd) \n')
        dates = [[start_date, end_date]]
        print(start_date, end_date)
    elif date_mode == 'moving':
        print()
        length = input('5 or 10 years moving window? 5 / 10 \n')
        if length == '10':
            dates = [['20140101', '20231231'],
                     ['20130101', '20221231'],
                     ['20120101', '20211231'],
                     ['20110101', '20201231'],
                     ['20100101', '20191231'],
                     ['20090101', '20181231'],
                     ['20080101', '20171231'],
                     ['20070101', '20161231'],
                     ['20060101', '20151231']]
        elif length == '5':
            dates = [['20060101', '20101231'],
                     ['20070101', '20111231'],
                     ['20080101', '20121231'],
                     ['20080101', '20131231'],
                     ['20100101', '20141231'],
                     ['20110101', '20151231'],
                     ['20120101', '20161231'],
                     ['20130101', '20171231'],
                     ['20140101', '20181231'],
                     ['20150101', '20191231'],
                     ['20160101', '20201231'],
                     ['20170101', '20211231'],
                     ['20180101', '20221231'],
                     ['20190101', '20231231']]
        else:
            print('Error')
            exit()
    else:
        print('Error')
        exit()
    print('Date:', dates)
    print()



    ### Ask Framework
    # framework = input('Framework? bband / abs \n')
    # if not (framework == 'bband' or (framework == 'abs')):
    #     print('Error')
    #     exit()
    # print('Framework:', framework)
    # print()

    framework = 'bband'


    # mode = 'heatmap'
    # framework = 'bband'
    # dates = [['20140101', '20231231']]


    ### Ask Range
    if (mode == 'heatmap') or (mode == 'single_heatmap'):
        default_value = input('Default Parameters? yes / no \n')
        if default_value == 'yes':
            rolling_start = 0
            rolling_end = 200
            rolling_step = 10
            threshold_start = 0
            threshold_end = 4
            threshold_step = 0.2
        else:
            rolling_start = input('rolling start? (0)\n')
            rolling_end = input('rolling end? (200)\n')
            rolling_step = input('rolling step? (10)\n')
            threshold_start = input('threshold start? (0)\n')
            threshold_end = input('threshold end? (4)\n')
            threshold_step = input('threshold step? (0.2)\n')


            rolling_start = int(rolling_start)
            rolling_end = int(rolling_end)
            rolling_step = int(rolling_step)
            threshold_start = float(threshold_start)
            threshold_end = float(threshold_end)
            threshold_step = float(threshold_step)

        if (mode == 'single_heatmap'):
            direction = input('Direction? ml / ms / rl / rs \n')
        else:
            direction = ''



        for date in dates:
            print(date)
            start_str = date[0]
            end_str = date[1]

            df = df_csv.copy()
            df['change'] = (df['close'] / df['close'].shift(1)) - 1
            start_date = pd.to_datetime(start_str, format='%Y%m%d')
            end_date = pd.to_datetime(end_str, format='%Y%m%d')
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

            bband_parameters = {
                'mode': mode,
                'framework': framework,
                'factor': 'factor',
                'direction': direction,
                'cost': 0,
                'momentum_rollings': np.arange(rolling_start, rolling_end, rolling_step),  # ma, np.arange(10, 100, 10)
                'momentum_thresholds': np.round(np.arange(threshold_start, threshold_end, threshold_step), 1),  # thres, np.arange(0, 3, 0.25)

                'revision_rollings': np.arange(rolling_start, rolling_end, rolling_step),  # ma, np.arange(10, 100, 10)
                'revision_thresholds': np.round(np.arange(threshold_start, threshold_end, threshold_step), 1),  # thres, np.arange(0, 3, 0.25)
                'dataframe': df
            }

            bband(bband_parameters=bband_parameters,
                                data_freq='1D',  # Default 1D
                                show_pic=False,  # Default True
                                save_pic=True,  # Default True
                                pic_name=f'{start_str}_{end_str}',  # Default 'output'
                                result_folder='result',  # Default 'result'
                                output_csv=False,  # Default False
                                )

    else:
        direction = input('Direction? ml / ms / rl / rs \n')
        r = input('Rolling? \n')
        r = int(r)
        t = input('Threshold? \n')
        t = float(t)
        print()

        output = False
        output_choice = input('Output csv? yes / no \n')
        if output_choice == 'yes':
            output = True


        for date in dates:

            print(date)
            start_str = date[0]
            end_str = date[1]

            df = df_csv.copy()
            df['change'] = (df['close'] / df['close'].shift(1)) - 1
            start_date = pd.to_datetime(start_str, format='%Y%m%d')
            end_date = pd.to_datetime(end_str, format='%Y%m%d')
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

            bband_parameters = {
                'mode': mode,
                'framework': framework,
                'factor': 'factor',
                'cost': 0,
                's1': [direction, r, t],
                'dataframe': df
            }

            bband(bband_parameters=bband_parameters,
                                data_freq='1D',  # Default 1D
                                show_pic=False,  # Default True
                                save_pic=True,  # Default True
                                pic_name=f'{start_str}_{end_str}',  # Default 'output'
                                result_folder='result',  # Default 'result'
                                output_csv=output,  # Default False
                                )


if __name__ == '__main__':
    run()

    print()
    print('Done')