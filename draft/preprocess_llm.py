import pandas as pd
import json 

from src.utils import get_parameters_combinations,get_param_value_union,get_promt_text_params,get_df_with_clothing_promt


with open('data/female-style-type.json') as f:
    female_style_type = json.load(f)
with open('data/male-style-type.json') as f:
    male_style_type = json.load(f)
with open('data/female-types-with-parameters.json') as f:
    female_types_with_parameters = json.load(f)
with open('data/female-types.json') as f:
    female_types = json.load(f)
with open('data/male-types-with-parameters.json') as f:
    male_types_with_parameters = json.load(f)
with open('data/male-types.json') as f:
    male_types = json.load(f)

#
female_style_type_df=pd.DataFrame(female_style_type).explode('types').reset_index(drop=True)
male_style_type_df=pd.DataFrame(male_style_type).explode('types').reset_index(drop=True)
#
female_df_clothing_promt=get_df_with_clothing_promt(gender_types=female_types,gender_types_with_parameters=female_types_with_parameters)
male_df_clothing_promt=get_df_with_clothing_promt(gender_types=male_types,gender_types_with_parameters=male_types_with_parameters)
#
df_female_style_promt=female_style_type_df.merge(female_df_clothing_promt,left_on='types',right_on='type')
df_male_style_promt=male_style_type_df.merge(male_df_clothing_promt,left_on='types',right_on='type')
#
df_female_style_promt=df_female_style_promt.groupby(['styleType','category'],as_index=False)['promtTypeParams'].apply(list)
df_male_style_promt=df_male_style_promt.groupby(['styleType','category'],as_index=False)['promtTypeParams'].apply(list)
#
df_female_style_promt['promtTypeParams']=df_female_style_promt.apply(lambda x: {x['category']:x['promtTypeParams']},axis=1)
df_male_style_promt['promtTypeParams']=df_male_style_promt.apply(lambda x: {x['category']:x['promtTypeParams']},axis=1)
#
df_female_style_promt=df_female_style_promt.groupby('styleType',as_index=False)['promtTypeParams'].apply(list)
df_male_style_promt=df_male_style_promt.groupby('styleType',as_index=False)['promtTypeParams'].apply(list)
#
df_female_style_promt.to_csv('data/female_style_promt.csv')
df_male_style_promt.to_csv('data/male_style_promt.csv')