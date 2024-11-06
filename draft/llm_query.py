from fireworks.client import Fireworks
import pandas as pd 
from ast import literal_eval
from src.msgs import get_right_msg
from tqdm import tqdm

def get_llm_response(msg):
    client = Fireworks(api_key="fw_3ZkkhpugiDMHrjoXdFZ6D44c")
    response = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p1-405b-instruct",
    messages=[
    {
        "role": "system",
        "content": "You are fashion expert with extensive knowledge of clothing styles, clothing types and their combinations"
    },
    {
        "role": "user",
        "content": msg
    }
    ],
    max_tokens=100000)
    return response.choices[0].message.content

#
df_female_style_promt=pd.read_csv('data/female_style_promt.csv',index_col=0)
df_male_style_promt=pd.read_csv('data/male_style_promt.csv',index_col=0)
df_female_style_promt['promtTypeParams']=df_female_style_promt['promtTypeParams'].apply(literal_eval)
df_male_style_promt['promtTypeParams']=df_male_style_promt['promtTypeParams'].apply(literal_eval)
# season and priority
df_styleProportion=pd.DataFrame([{'casual':3,'classic':1,'smart-casual':2,'street':1,'old-money':1,'oversized':1,'minimalism':1}]).T.reset_index()\
    .rename(columns={'index':'styleType',0:'proportionPriority'})
df_styleProportion['proportionPriority']=df_styleProportion.proportionPriority/df_styleProportion.proportionPriority.sum()
# number of generations
df_female_style_promt=df_female_style_promt.merge(df_styleProportion,on='styleType')
df_male_style_promt=df_male_style_promt.merge(df_styleProportion,on='styleType')
df_female_style_promt['generationNumber']=(df_female_style_promt.proportionPriority*9600).astype(int)
df_male_style_promt['generationNumber']=(df_male_style_promt.proportionPriority*6400).astype(int)
#
df_female_style_promt['seasons']=[['winter','autumn','summer','spring']]*len(df_female_style_promt)
df_male_style_promt['seasons']=[['winter','autumn','summer','spring']]*len(df_male_style_promt)
df_female_style_promt['generationNumber']=df_female_style_promt.apply(lambda x: int(x['generationNumber']/len(x['seasons'])),axis=1)
df_male_style_promt['generationNumber']=df_male_style_promt.apply(lambda x: int(x['generationNumber']/len(x['seasons'])),axis=1)
#
df_female_style_promt=df_female_style_promt.explode('seasons').reset_index(drop=True)
df_male_style_promt=df_male_style_promt.explode('seasons').reset_index(drop=True)

for i in tqdm(range(0,len(df_male_style_promt))):
    gender='male'
    list_promtTypeParams=df_male_style_promt['promtTypeParams'][i]
    season=df_male_style_promt.seasons[i]
    style=df_male_style_promt.styleType[i]
    number=df_male_style_promt.generationNumber[i]
    # number=5
    if season=='summer' or season =='spring':
        tmplt='''{"layered_top": "value",
        "top": "value",
        "bottom": "value",
        "footwear": "value"}'''
    else:
        tmplt='''{"outerwear": "value",
        "top": "value",
        "bottom": "value",
        "footwear": "value"}'''

    msg=get_right_msg(style=style,
                  season=season,
                  number=number,
                  list_promtTypeParams=list_promtTypeParams,
                  tmplt=tmplt)
    output=get_llm_response(msg)
    with open(f"data_llm/outputs/{season}_{style}_{gender}_{number}.txt", "w") as text_file:
        text_file.write(output)