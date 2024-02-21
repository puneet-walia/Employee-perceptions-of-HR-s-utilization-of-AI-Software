import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

nltk.download('punkt')
nltk.download('stopwords')

excel_file_path = '/Users/puneetwalia/Desktop/NEW_TCD/final_sheet.xlsx' 
df = pd.read_excel(excel_file_path)

authors_column = 'Authors'
posts_column = 'Posts'

author_posts = df.groupby(authors_column)[posts_column].apply(lambda x: ' '.join(x)).reset_index()

def process_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return filtered_tokens

author_posts['Processed Posts'] = author_posts[posts_column].apply(process_text)

all_tokens = [token for tokens_list in author_posts['Processed Posts'] for token in tokens_list]

fdist = FreqDist(all_tokens)

fdist.plot(30, cumulative=False)
plt.show()
