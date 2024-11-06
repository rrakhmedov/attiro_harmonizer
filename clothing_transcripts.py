import pandas as pd
import json 
from ast import literal_eval
from src.utils import get_df_with_clothing_parameters_transcript
#cartesian function

with open('data/female/female-style-type.json') as f:
    female_style_type = json.load(f)
with open('data/male/male-style-type.json') as f:
    male_style_type = json.load(f)
with open('data/female/female-types-with-parameters.json') as f:
    female_types_with_parameters = json.load(f)
with open('data/female/female-types.json') as f:
    female_types = json.load(f)
with open('data/male/male-types-with-parameters.json') as f:
    male_types_with_parameters = json.load(f)
with open('data/male/male-types.json') as f:
    male_types = json.load(f)

#layered_top
female_layered_top_df=pd.read_csv('data/female/female_layered_top.csv',index_col=0)
male_layered_top_df=pd.read_csv('data/male/male_layered_top.csv',index_col=0)
# style types in flatten dataframe
female_style_type_df=pd.DataFrame(female_style_type).explode('types').reset_index(drop=True)
male_style_type_df=pd.DataFrame(male_style_type).explode('types').reset_index(drop=True)
# get df with clothing and parameteres combined. each row corresponds to clothing combination
#save
female_df_clothing_transcript=get_df_with_clothing_parameters_transcript(gender_types=female_types,gender_types_with_parameters=female_types_with_parameters)
male_df_clothing_transcript=get_df_with_clothing_parameters_transcript(gender_types=male_types,gender_types_with_parameters=male_types_with_parameters)
female_df_clothing_transcript.to_csv('data_combinations/female_style_clothing_transcript.csv')
male_df_clothing_transcript.to_csv('data_combinations/male_style_clothing_transcript.csv')
#merge between styles and types all combination parameters
df_female_style_clothing_type=female_style_type_df.merge(female_df_clothing_transcript,left_on='types',right_on='type')
df_male_style_clothing_type=male_style_type_df.merge(male_df_clothing_transcript,left_on='types',right_on='type')
# replace top with layered_top
df_female_style_clothing_type=df_female_style_clothing_type.merge(female_layered_top_df,on='type',how='left')
df_male_style_clothing_type=df_male_style_clothing_type.merge(male_layered_top_df,on='type',how='left')
df_female_style_clothing_type['newCategory']=df_female_style_clothing_type.apply(lambda x: 'layered_top' if x['category'] =='top' and x['layered_top']==1.0 else x['category'],axis=1)
df_male_style_clothing_type['newCategory']=df_male_style_clothing_type.apply(lambda x: 'layered_top' if x['category'] =='top' and x['layered_top']==1.0 else x['category'],axis=1)
# get compressed types with parameters according to style and newCategory
df_female_style_clothing_type=df_female_style_clothing_type.groupby(['styleType','newCategory'],as_index=False)['transcriptTypeParams'].apply(list)
df_male_style_clothing_type=df_male_style_clothing_type.groupby(['styleType','newCategory'],as_index=False)['transcriptTypeParams'].apply(list)
# making dictionary for newCategorys and clothing types with parameters
df_female_style_clothing_type['transcriptTypeParams']=df_female_style_clothing_type.apply(lambda x: {x['newCategory']:x['transcriptTypeParams']},axis=1)
df_male_style_clothing_type['transcriptTypeParams']=df_male_style_clothing_type.apply(lambda x: {x['newCategory']:x['transcriptTypeParams']},axis=1)
# get compressed types with params accorgind to style
df_female_style_clothing_type=df_female_style_clothing_type.groupby('styleType',as_index=False)['transcriptTypeParams'].apply(list)
df_male_style_clothing_type=df_male_style_clothing_type.groupby('styleType',as_index=False)['transcriptTypeParams'].apply(list)
# saving compressed data
df_female_style_clothing_type.to_csv('data_combinations/female_style_clothing_types.csv')
df_male_style_clothing_type.to_csv('data_combinations/male_style_clothing_types.csv')