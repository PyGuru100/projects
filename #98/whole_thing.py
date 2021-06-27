import pandas as pd
# import plotly.express as px
import iso3166
from datetime import datetime
import matplotlib.pyplot as plt


DATE_OF_SOVIET_DISSOLUTION = datetime(year=1991, month=12, day=25)


def extract_year(_date: datetime):
    return _date.year


def extract_month(_date: datetime):
    return _date.month


def string_to_float(number: str) -> float:
    return float(number.replace(',', ''))


def country_name_extractor(location: str) -> str:
    country_name = location.split(',')[-1].strip()
    if country_name in ['New Mexico', 'Pacific Missile Range Facility', 'Gran Canaria']:
        return 'USA'
    if country_name == 'Yellow Sea':
        return 'China'
    if country_name == 'Shahrud Missile Test Site':
        return 'Iran'
    if country_name == 'Barents Sea':
        return 'Russia'
    return country_name


iso_dict = {
    'USA': 'UNITED STATES OF AMERICA',
    'RUSSIA': 'RUSSIAN FEDERATION',
    'IRAN': 'IRAN, ISLAMIC REPUBLIC OF',
    'NORTH KOREA': "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",
    'SOUTH KOREA': 'KOREA, REPUBLIC OF',
}


def country_code_extractor(country_name: str) -> str:
    country_name = country_name.upper()
    if country_name in iso_dict:
        country_name = iso_dict[country_name]
    elif country_name == 'PACIFIC OCEAN':
        return ''
    # the index of the code we're looking for is 2.
    return iso3166.countries_by_apolitical_name[country_name][2]


def make_date_normal(_date: datetime):
    # Yes, I'm ignoring timezone data. I highly doubt a difference of a few hours matters here.
    # And I just checked the data: the earliest launch following the collapse of the USSR took place
    # on the 28th of December. So yes, I'm ignoring timezone data.
    return datetime(year=_date.year, month=_date.month, day=_date.day)


def ussr_convertor(country_name: str) -> str:
    necessary_dict = {
        'Russia': 'USSR',
        'Kazakhstan': 'USSR'
    }
    if country_name in necessary_dict:
        return necessary_dict[country_name]
    return country_name


def get_rid_of_others(country_name: str) -> str:
    if country_name not in ['USSR', 'USA']:
        return 'DOES NOT MATTER'
    return country_name


# data cleaning and pruning:
data = pd.read_csv('mission_launches.csv')
# removes junk columns:
data.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
# removes one duplicate:
data.drop_duplicates(inplace=True)
# dropna removes none. Without the subset it removes 3000 lmao, which is
# because the price column has NaN values a-plenty.
data.dropna(inplace=True, subset=['Date', 'Location', 'Organisation'])
# end of data cleaning


# launches per company chart:
# launches_by_company = data.groupby('Organisation').aggregate({'Date': pd.Series.count})
# launches_by_company = (launches_by_company.sort_values(by='Date', ascending=False))
# bar_company = px.bar(launches_by_company, x=launches_by_company.index,
#                      y=launches_by_company['Date'], labels={"Date": "Number of Launches"})
# bar_company.show()
# end of launches per company chart


# active vs. decommissioned:
# rockets_status = data.groupby('Rocket_Status').aggregate({'Date': pd.Series.count})
# print(rockets_status)
# end of active vs.


# percent successful, percent failure:
# success_data = data.groupby('Mission_Status').aggregate({'Date': pd.Series.count}).reset_index()
# success_data = success_data.rename(columns={'Date': 'Count'})
# print(success_data)
# for status in ['Failure', 'Success']:
#     print(f"{status=}")
#     print(f"col_index fraction | "
#           f"{success_data[success_data['Mission_Status'] == status]['Count']/success_data['Count'].sum()}")
# end of percent successful


# price data
# price_data_available = data.dropna(subset=['Price'])
# price_data_available['Price'] = price_data_available['Price'].apply(string_to_float)
# price_data_available = (price_data_available[['Price', 'Organisation']])
# print(price_data_available.sort_values(by='Price', ascending=False))
# hist = px.histogram(data_frame=price_data_available, x='Price', nbins=10)
# hist.show()
# end of price data


# map of launches by country
# maps, failures
# # uncommenting this line turns into failures by country:
# # data = data[data['Mission_Status'] != 'Success']
# data['Country'] = data['Location'].apply(country_name_extractor)
# data['Country_Code'] = data['Country'].apply(country_code_extractor)
# data = data.groupby('Country_Code').aggregate({'Date': pd.Series.count})
# data.reset_index(inplace=True)
# data.rename(columns={'Date': 'Count'}, inplace=True)
# fig = px.choropleth(data, locations='Country_Code', color=data['Count'])
# fig.show()
# end of maps


# sunburst
# data['Country'] = data['Location'].apply(country_name_extractor)
# sun = px.sunburst(data, path=['Mission_Status', 'Country', 'Organisation'])
# sun.show()
# end of sunburst


# money spent: (please note that little data on the budget of RVSN USSR is available.
# data.dropna(subset=['Price'], inplace=True)
# data['Price'] = data['Price'].apply(string_to_float)
# total_per_org = data.groupby('Organisation').aggregate({'Price': pd.Series.sum,
#                                                         'Date': pd.Series.count}).reset_index()
# total_per_org.rename(columns={'Date': 'Count', 'Price': 'Total_Spent'}, inplace=True)
# total_per_org['Price_Per_Mission'] = total_per_org['Total_Spent']/total_per_org['Count']
# print(total_per_org)
# end of money spent


data['Date'] = pd.to_datetime(data['Date'])


# Total missions year by year:
# data['Year'] = data['Date'].apply(extract_year)
# by_year = data.groupby('Year').count().reset_index()[['Organisation',
#                                                       'Year']].rename(columns={'Organisation': 'Count'})
# line_chart = px.line(by_year, x='Year', y='Count')
# line_chart.show()
# end of total missions year by year.


# most popular months for launches:
# data['Month'] = data['Date'].apply(extract_month)
# by_month = data.groupby('Month').count().reset_index()[['Organisation', 'Month']]\
#     .rename(columns={'Organisation': 'Count'})
# # uncommenting the line below shows the rolling average graph.
# # by_month['Count'] = by_month['Count'].rolling(3).mean()
# line_chart = px.line(by_month, x='Month', y='Count')
# line_chart.show()
# end of popular months


# average price, year by year
# data.dropna(subset=['Price'], inplace=True)
# data['Price'] = data['Price'].apply(string_to_float)
# data['Year'] = data['Date'].apply(extract_year)
# print(data[data['Year'] == 1970][['Year', 'Price']])
# price_by_year = data.groupby('Year').aggregate({'Price': pd.Series.mean}).reset_index()
# print(price_by_year)
# line_chart = px.line(price_by_year, x='Year', y='Price')
# line_chart.show()
# end of average price


# USSR VS US SECTION. Here you must uncomment the section-specific code THEN the subsection-specific code.

# data['Date'] = data['Date'].apply(make_date_normal)
# data = data[data['Date'] <= DATE_OF_SOVIET_DISSOLUTION]
# data['Country'] = data['Location'].apply(country_name_extractor)
# data['Country'] = data['Country'].apply(ussr_convertor).apply(get_rid_of_others)
# data = data[data['Country'] != 'DOES NOT MATTER']
# #
# # data = data.groupby(by='Country').aggregate({'Date': pd.Series.count}).rename(
# #                                      columns={'Date': 'Count'}).reset_index()
# # # color shouldn't work here, but it does lmao
# # pie_chart = px.pie(data, names='Country', values='Count', color=['blue', 'red'])
# # pie_chart.show()
# #
# # # Year-on-Year --
# # # uncommenting the line below makes it failure year-on-year data
# # # data = data[data['Mission_Status'] != 'Success']
# # USA_DATA = data[data['Country'] == 'USA']
# # USSR_DATA = data[data['Country'] == 'USSR']
# # for superpower_data in [USSR_DATA, USA_DATA]:
# #     superpower_data['Year'] = superpower_data['Date'].apply(extract_year)
# #     superpower_data = superpower_data.groupby('Year').aggregate({'Date': pd.Series.count}).rename(
# #         columns={'Date': 'Count'}).reset_index()
# #     plt.plot(superpower_data['Year'], superpower_data['Count'])
# # plt.show()


def generate_missions_line_chart(what_for):
    """This is a very specific-purpose function written because I want to generate
    comparison graphs for both the Country column and the Organisation column."""
    if what_for == 'Country':
        data['Country'] = data['Location'].apply(country_name_extractor)
    data['Year'] = data['Date'].apply(extract_year)
    things = [thing for thing in data[what_for].unique()]
    legend = []
    for thing in things:
        thing_specific_data = data[data[what_for] == thing]
        thing_specific_data = thing_specific_data.groupby('Year').aggregate(
            {'Date': pd.Series.count}).reset_index()
        thing_specific_data.rename(columns={'Date': f'{thing}_Mission_Count'}, inplace=True)
        plt.plot(thing_specific_data['Year'], thing_specific_data[f'{thing}_Mission_Count'])
        legend.append(f'{thing} line')
    plt.legend(legend)
    plt.show()


# data['Year'] = data['Date'].apply(extract_year)
# success_data = data[data['Mission_Status'] == 'Success']
# failure_data = data[data['Mission_Status'] != 'Success']
# success_data = success_data.groupby('Year').aggregate({'Date': pd.Series.count}).rename(
#     columns={'Date': 'Count'}).reset_index()
# failure_data = failure_data.groupby('Year').aggregate({'Date': pd.Series.count}).rename(
#     columns={'Date': 'Count'}).reset_index()
# failure_data['Ratio'] = failure_data['Count'] / (failure_data['Count'] + success_data['Count'])
# line_chart = px.line(failure_data, 'Year', 'Ratio')
# line_chart.show()


# countries line chart:
# generate_missions_line_chart('Country')

# organisations line chart:
# generate_missions_line_chart('Organisation')
