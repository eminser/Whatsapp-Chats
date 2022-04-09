# 1. importing libraries
import re
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from nltk.corpus import stopwords
from nltk import download

# 2. settings for dataframe outlook
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.3f}')
pd.set_option('display.width', 500)
pd.set_option('display.max_rows', None)

regex = r'"(.*:\d\d) - (.*): (.*)"'

with open(r'E:\12. EĞİTİM\bootcamp\0. REGEX\doktora badies project\whatsapp.txt', 'r', encoding = 'UTF-8') as text:
    text_str = text.read()

matches = re.findall(regex, text_str)
df = []

# 4. creating dataframe
for i in range(len(matches)):
    d = {
        'Time' : matches[i][0],   # this columns about writing times
        'Name' : matches[i][1],   # this columns about names
        'Content' : matches[i][2] # this columns about contents
    }
    df.append(d)

df = pd.DataFrame(df)

# 5. first touch to data
df.head()
df.info()
df.shape

len(df['Name'][0].split()[0])
for i in df['Name'][0]:
sorted(df['Name'][1].split(), key = len)[-1]

df['Time'] = pd.to_datetime(df['Time'])
df['Name'] = df['Name'].apply(lambda x : x.split()[0])

df['Total_Words'] = df['Content'].apply(lambda x : len(x.split()))
df['Content_Long'] = df['Content'].apply(lambda x : len(x))

df['Year'] = df['Time'].apply(lambda x : x.year)
df['Month'] = df['Time'].apply(lambda x : x.month)
df['Day_Period'] = pd.cut(df['Time'].apply(lambda x : x.hour), 3 , labels=['Night','Noon','Evening'])

# 6. analyzing the data

df.groupby('Name')['Time'].count() # en çok konuşanlar
df.groupby(['Name', 'Day_Period'])['Time'].count() # periyotlara göre konuşmacılar
df[df['Content'].str.contains('Medya')].groupby('Name')['Time'].count() # medya gönderen kullanıcılar

index_df=df['Content_Long'].sort_values(ascending=False)
df[df.index.isin(index_df)][['Name', 'Content', 'Content_Long']]\
    .sort_values(by='Content_Long', ascending=False)  #en uzun cümleler

df.groupby('Name')['Total_Words'].sum() / df.groupby('Name')['Total_Words'].count() # mesaj başına kelime sayısı

pl = df.groupby(['Name', 'Year'])['Time'].count().reset_index() # kişi bazında yıllık mesajlaşma sayısı
sns.lineplot(x='Year', y='Time', hue='Name', data=pl)
plt.show();

# 7. Work Cloud

text = df['Content'].apply(lambda x: x.strip().lower()) # hepsini küçülttük
text = text.str.replace("[^\w\s]", "") # noktalamalardan kurtulduk
text.str.replace("\d", "")  # rakamlardan kurtulduk

download('stopwords')
sw = stopwords.words('turkish')   # stopwords'ların hepsi küçük harf!!
text = text.apply(lambda i : ' '.join(i for i in i.split() if i not in sw)) #stopwordslerden kurtulduk

link_index = text[text.apply(lambda x : x.startswith('http'))].index.to_list() # sadece link olan mesajlar
space_index = text[text==''].index.to_list() # boş olan mesajlar
ind=space_index + link_index
text = text[~text.index.isin(ind)] # gereksiz satırlar silindi

sorted_text =pd.Series(' '.join(text).split()).value_counts()
sorted_text = sorted_text[sorted_text>8]

#mask=np.array(Image.open(r'E:\12. EĞİTİM\bootcamp\0. REGEX\doktora badies project\36575mask.png'))
mask=np.array(Image.open(r'E:\12. EĞİTİM\datas\bulut.jpg'))
text=' '.join(i for i in sorted_text.index)
wc = WordCloud(max_font_size=50, mask=mask, contour_width=60, contour_color='white', background_color='gray')
wc.generate(text)
plt.figure(figsize=[30,30])
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()
wc.to_file(r'E:\12. EĞİTİM\datas\netflix_chataa.png')


