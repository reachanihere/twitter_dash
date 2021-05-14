import pandas as pd

"""
Loading the data from a repo created by Johns Hopkins University.
"""

def loading_data():

    total_confirmed = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data'
        '/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        encoding='utf-8', na_values=None)
    total_death = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data'
        '/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        encoding='utf-8', na_values=None)

    total_recovered = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data'
        '/csse_covid_19_time_series/time_series_covid19_recovered_global.csv',
        encoding='utf-8', na_values=None)

    total_confirmed.replace(
        to_replace='US', value='United States', regex=True, inplace=True)
    total_recovered.replace(
        to_replace='US', value='United States', regex=True, inplace=True)
    total_death.replace(
        to_replace='US', value='United States', regex=True, inplace=True)

    df_pop = pd.read_json(
        'https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-population.json')

    df_pop.columns = ['Country/Region', 'population']
    df_pop = df_pop.replace(to_replace='Russian Federation', value='Russia')

    return total_confirmed, total_death, total_recovered, df_pop


def cleaning_data(total_confirmed, total_death, total_recovered):
    # grouped total confirmed data
    grouped_total_confirmed = total_confirmed[["Country/Region", total_confirmed.columns[-1]]].groupby(
        "Country/Region").sum().sort_values(by=total_confirmed.columns[-1], ascending=False)
    grouped_total_confirmed.reset_index(inplace=True)
    grouped_total_confirmed.columns = ["Country/Region", 'confirmed']
    grouped_total_confirmed.replace(
        to_replace='US', value='United States', regex=True, inplace=True)

    barplot_confirmed_values = grouped_total_confirmed["confirmed"].values.tolist(
    )
    country_names = grouped_total_confirmed["Country/Region"].values.tolist()

    # global time series confirmed data frame
    global_confirmed_timeseries = pd.DataFrame(
        total_confirmed[total_confirmed.columns[4:]].sum())
    global_confirmed_timeseries.reset_index(inplace=True)
    global_confirmed_timeseries.columns = ['date', 'total confirmed']

    global_confirmed_timeseries["daily new cases"] = global_confirmed_timeseries['total confirmed'] - \
                                                     global_confirmed_timeseries['total confirmed'].shift()
    global_confirmed_timeseries = global_confirmed_timeseries.fillna(0)

    # grouped total recovered data
    grouped_total_recovered = total_recovered[["Country/Region", total_recovered.columns[-1]]].groupby(
        "Country/Region").sum().sort_values(by=total_recovered.columns[-1], ascending=False)
    grouped_total_recovered.reset_index(inplace=True)
    grouped_total_recovered.columns = ["Country/Region", 'recovered']
    grouped_total_recovered.replace(
        to_replace='US', value='United States', regex=True, inplace=True)

    barplot_recovered_values = grouped_total_recovered["recovered"].values.tolist(
    )
    country_names = grouped_total_confirmed["Country/Region"].values.tolist()

    global_recovered_timeseries = pd.DataFrame(
        total_recovered[total_recovered.columns[4:]].sum())
    global_recovered_timeseries.reset_index(inplace=True)
    global_recovered_timeseries.columns = ['date', 'total recovered']

    global_recovered_timeseries["daily new recovered"] = global_recovered_timeseries['total recovered'] - \
                                                         global_recovered_timeseries['total recovered'].shift()
    global_recovered_timeseries = global_recovered_timeseries.fillna(0)

    grouped_total_death = total_death[["Country/Region", total_death.columns[-1]]].groupby(
        "Country/Region").sum().sort_values(by=total_death.columns[-1], ascending=False)
    grouped_total_death.reset_index(inplace=True)
    grouped_total_death.columns = ["Country/Region", 'deaths']
    grouped_total_death.replace(
        to_replace='US', value='United States', regex=True, inplace=True)

    barplot_death_values = grouped_total_death["deaths"].values.tolist()
    global_death_timeseries = total_death[total_death.columns[4:]].sum()

    global_death_timeseries = pd.DataFrame(
        total_death[total_death.columns[4:]].sum())
    global_death_timeseries.reset_index(inplace=True)
    global_death_timeseries.columns = ['date', 'total deaths']

    global_death_timeseries["daily new deaths"] = global_death_timeseries['total deaths'] - \
                                                  global_death_timeseries['total deaths'].shift()
    global_death_timeseries = global_death_timeseries.fillna(0)
    global_death_timeseries

    timeseries_final = pd.merge(
        global_confirmed_timeseries, global_recovered_timeseries, how='inner', on='date')
    timeseries_final = pd.merge(
        timeseries_final, global_death_timeseries, how='inner', on='date')
    timeseries_final
    return grouped_total_confirmed, grouped_total_recovered, grouped_total_death, timeseries_final, country_names


def combining_data(grouped_total_confirmed, grouped_total_recovered, grouped_total_death, df_pop):

    url = "https://gist.githubusercontent.com/komasaru/9303029/raw/9ea6e5900715afec6ce4ff79a0c4102b09180ddd/iso_3166_1.csv"
    country_code = pd.read_csv(url)
    country_code = country_code[[
        "English short name", "Alpha-3 code", "Numeric"]]
    country_code.columns = ["Country/Region", "code3", "id"]


    country_code = country_code.replace(
        to_replace='Russian Federation (the)', value='Russia')
    country_code = country_code.replace(
        to_replace='United Kingdom (the)', value='United Kingdom')
    country_code = country_code.replace(
        to_replace='United States (the)', value='United States')
    country_code = country_code.replace(to_replace='Viet Nam', value='Vietnam')


    final_df = pd.merge(grouped_total_confirmed,
                        grouped_total_recovered, how='inner', on='Country/Region')
    final_df = pd.merge(final_df, grouped_total_death,
                        how='inner', on='Country/Region')
    final_df = pd.merge(final_df, df_pop, how='inner', on='Country/Region')
    final_df = pd.merge(country_code, final_df,
                        how='inner', on='Country/Region')
    final_df = final_df.sort_values(by="confirmed", ascending=False)
    final_df.reset_index(inplace=True, drop=True)

    final_df['cases/million'] = ((final_df['confirmed'] /
                                  final_df['population']) * 1000000).round(2)
    final_df['death rate(%)'] = (
            (final_df['deaths'] / final_df['confirmed']) * 100).round(2)

    return final_df
