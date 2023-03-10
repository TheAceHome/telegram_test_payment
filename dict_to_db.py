import pandas as pd

def dict_to_db_func(data):
    fin_dict={}
    for key, value in data.items():
        if key in ['from','chat','successful_payment']:
            value = dict(value)
            for key1, value1 in value.items():
                fin_dict[key1] = value1

        elif key == 'date':
            value = pd.to_timedelta(value, unit='s') + pd.to_datetime('1960-1-1')
            fin_dict[key] = value

        else:
            fin_dict[key] = value

    print(fin_dict)

    df = pd.DataFrame(fin_dict,index=[0]).set_index('id')
    print(df)