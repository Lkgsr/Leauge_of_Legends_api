import pandas as pd
from Api import LeaugeOfLegendObjects as objects
from sqlalchemy import desc
import matplotlib.pyplot as plt

the_offset_val = 1000
df = pd.read_sql(objects.session.query(objects.Participants).order_by(desc(objects.Participants.game_id)).statement,objects.session.bind) #.limit(100000).offset(the_offset_val)
df_champions = pd.read_sql(objects.session.query(objects.Champions).statement, objects.session.bind)
teil_df = df['champion_id'].value_counts()
teil_df = pd.DataFrame(teil_df)
print(teil_df.head())
teil_df.columns = ['count']
teil_df.index.name = "id"
teil_df.reset_index(level=0, inplace=True)
print(teil_df.head())

teil_df.index.name = "ind"
print(teil_df.head())
teil_df.sort_values(by=['id'], inplace=True)
print(teil_df.head())
teil_df = teil_df.merge(df_champions, on='id')
print(teil_df.head())
teil_df.reset_index(level=0, inplace=True)
print(teil_df.head())
teil_df.index.name = "ind"
print(teil_df.head())
teil_df.drop(['index'], axis=1)
print(teil_df.head())
teil_df.reset_index(level=0, inplace=True)
print(teil_df.head())
teil_df.sort_values(by=['count'], inplace=True)
print(teil_df.head())
#teil_df['abstand'] = teil_df.apply(lambda row: (row['ind']*2), axis=1)


fig = plt.figure(dpi=140)
ax = teil_df.plot(kind='bar', x='ind',  y='count', colormap='Dark2_r', ax = plt.gca()) #plt.plot_date(df.index, df.count)# ,
ax.set_xticks(teil_df.ind)
ax.set_xticklabels(teil_df.name, rotation=90)
plt.show()