import pandas as pd
from wordcloud import WordCloud

df_general = pd.read_csv(r"static\dataset\general_covid.csv")
df_restriction = pd.read_csv(r"static\dataset\covid_restriction.csv")
df_vaccination = pd.read_csv(r"static\dataset\covid_vaccination.csv")

def create_wordcloud(df_general, df_vaccination, df_restriction):
    wc_general = WordCloud(background_color="black", max_words=2000, width=1600, height=800).generate(" ".join(df_general.text))
    wc_general.to_file("static\generalwordcloud.png")

    wc_vaccination = WordCloud(background_color="black", max_words=2000, width=1600, height=800).generate(" ".join(df_vaccination.text))
    wc_vaccination.to_file("static\wordcloudvaccination.png")

    wc_restriction = WordCloud(background_color="black", max_words=2000, width=1600, height=800).generate(" ".join(df_restriction.text))
    wc_restriction.to_file("static\wordcloudrestriciton.png")

