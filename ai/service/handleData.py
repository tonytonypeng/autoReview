import pandas as pd

class prepareData(object):
    def __init__(self):
        # 读取数据
        df_business = pd.read_csv('data/business.csv')
        df_review = pd.read_csv('data/review.csv')

        # 筛选出五星评价、餐厅
        five_star = df_review[df_review['stars'] == 5]
        restaurants = df_business[df_business['categories'].str.contains('Restaurant')]

        # 筛选出五星评价的餐厅
        restaurants_clean = restaurants[['business_id','name']]
        combo = pd.merge(restaurants_clean, five_star, on= 'business_id')

        # 去除空格，去重
        rnn_fivestar_reviw_only = combo[['text']]
        rnn_fivestar_reviw_only = rnn_fivestar_reviw_only.replace({r'\n+':''},regex=True)
        final = rnn_fivestar_reviw_only.drop_duplicates()

        final['text'] = '<SOR>' + final['text'].astype(str) + '<EOR>'

        final.to_csv('data/five_star_restaurants_reviews_only.csv', index= False, encoding= 'utf-8')
        final.to_csv('data/five_star_text.txt', header= None, sep= ' ')