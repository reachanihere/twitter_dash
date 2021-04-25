import pandas as pd
from wordcloud import WordCloud
import application

# general_data, restriction_data, vaccination_data

df_general_word_cloud = pd.read_csv('https://raw.githubusercontent.com/FabioPalliparambil98/cleaned-covid-dataset/main/general_covid.csv')
df_restriction_word_cloud = pd.read_csv('https://raw.githubusercontent.com/FabioPalliparambil98/cleaned-covid-dataset/main/covid_restriction.csv')
df_vaccination_word_cloud = pd.read_csv('https://raw.githubusercontent.com/FabioPalliparambil98/cleaned-covid-dataset/main/covid_vaccination.csv')


# general_data, restriction_data, vaccination_data = model.dataset_and_model(model.df_general,
#                                                                            model.df_restriction,
#                                                                            model.df_vaccination)
#
# df_general_word_cloud = general_data.copy()
# df_restriction_word_cloud = restriction_data.copy()
# df_vaccination_word_cloud = vaccination_data.copy()


def create_wordcloud(df_general, df_vaccination, df_restriction):
    wc_general = WordCloud(background_color="black", max_words=2000, width=1600, height=1300).generate(
        " ".join(df_general.text))
    wc_general.to_file("static\generalwordcloud.png")

    wc_vaccination = WordCloud(background_color="black", max_words=2000, width=1600, height=1300).generate(
        " ".join(df_vaccination.text))
    wc_vaccination.to_file("static\wordcloudvaccination.png")

    wc_restriction = WordCloud(background_color="black", max_words=2000, width=1600, height=1300).generate(
        " ".join(df_restriction.text))
    wc_restriction.to_file("static\wordcloudrestriciton.png")

create_wordcloud(df_general_word_cloud, df_vaccination_word_cloud, df_restriction_word_cloud )


"""
import mysql.connector
from mysql.connector import errorcode

cnx = mysql.connector.connect(
        host = '127.0.0.1',
        user = 's5107880',
        password = 'b1b299f98e7ad039fb6dd73281e148ac')
print(cnx)

"""

