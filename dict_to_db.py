import pandas as pd
from sqlalchemy import create_engine, text

def dict_to_db_func(data,payment_id):

    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

    fin_dict={}
    fin_dict['message_id'] = data.message_id
    fin_dict['id'] = data['from'].id
    fin_dict['payment_id'] = payment_id
    fin_dict['is_bot'] = data['from'].is_bot
    fin_dict['first_name'] = data['from'].first_name
    fin_dict['username'] = data['from'].username
    fin_dict['language_code'] = data['from'].language_code
    fin_dict['chat_id'] = data.chat.id
    fin_dict['chat_first_name'] = data.chat.first_name
    fin_dict['chat_username'] = data.chat.username
    fin_dict['chat_type'] = data.chat.type
    fin_dict['date'] = data.date
    df = pd.DataFrame(fin_dict, index=[0]).set_index('id')
    df.to_sql(name='client_data', con=engine, if_exists='append')