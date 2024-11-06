import pandas as pd
import json 
from ast import literal_eval
import numpy as np
from src.utils import get_df_with_clothing_parameters_transcript
from src.cartesian import LazyCartesianProduct
#cartesian function
def get_clothes_combinations(transcriptTypeParamsValues,N):
    result = {}
    for d in transcriptTypeParamsValues:
        result.update(d)
    #
    first_list=[result['outerwear'],result['top'],result['bottom'],result['footwear']]
    first_cp = LazyCartesianProduct(first_list)
    first_indices=np.random.randint(0,first_cp.maxSize,size=N//2).tolist()
    first_cp_result = [first_cp.entryAt(i) for i in first_indices]
    #
    second_list=[result['layered_top'],result['top'],result['bottom'],result['footwear']]
    second_cp = LazyCartesianProduct(second_list)
    second_indices=np.random.randint(0,second_cp.maxSize,size=N//2).tolist()
    second_cp_result = [second_cp.entryAt(i) for i in second_indices]
    return first_cp_result,second_cp_result
#

# preparing data for next stage
df_female_style_clothing_type=pd.read_csv('data_combinations/female_style_clothing_types.csv',index_col=0)
df_male_style_clothing_type=pd.read_csv('data_combinations/male_style_clothing_types.csv',index_col=0)
df_female_style_clothing_type['transcriptTypeParams']=df_female_style_clothing_type['transcriptTypeParams'].apply(literal_eval)
df_male_style_clothing_type['transcriptTypeParams']=df_male_style_clothing_type['transcriptTypeParams'].apply(literal_eval)
# distribution of proportions between styles
df_styleProportion=pd.DataFrame([{'casual':3,'classic':1,'smart-casual':2,'street':1,'old-money':1,'oversized':1,'minimalism':1}]).T.reset_index()\
    .rename(columns={'index':'styleType',0:'proportionPriority'})
df_styleProportion['proportionPriority']=df_styleProportion.proportionPriority/df_styleProportion.proportionPriority.sum()
# assigning generationNumber
df_female_style_clothing_type=df_female_style_clothing_type.merge(df_styleProportion,on='styleType')
df_male_style_clothing_type=df_male_style_clothing_type.merge(df_styleProportion,on='styleType')
df_female_style_clothing_type['generationNumber']=(df_female_style_clothing_type.proportionPriority*9600).astype(int)
df_male_style_clothing_type['generationNumber']=(df_male_style_clothing_type.proportionPriority*6400).astype(int)
#save again
df_female_style_clothing_type.to_csv('data_combinations/female_style_clothing_types.csv')
df_male_style_clothing_type.to_csv('data_combinations/male_style_clothing_types.csv')
# cartesian part male
gender ='male'
for i in range(df_male_style_clothing_type.shape[0]):
    combinations=get_clothes_combinations(transcriptTypeParamsValues=df_male_style_clothing_type.transcriptTypeParams[i],
                             N=df_male_style_clothing_type.generationNumber[i])
    #
    with open('data_combinations/cartesian_product/'+f'{gender}_'+df_male_style_clothing_type['styleType'][i]+'_outerwear.json', 'w') as f:
        json.dump(combinations[0], f)
    #
    with open('data_combinations/cartesian_product/'+f'{gender}_'+df_male_style_clothing_type['styleType'][i]+'_layered_top.json', 'w') as f:
        json.dump(combinations[1], f)
# cartesian part female    
gender ='female'
for i in range(df_female_style_clothing_type.shape[0]):
    combinations=get_clothes_combinations(transcriptTypeParamsValues=df_female_style_clothing_type.transcriptTypeParams[i],
                             N=df_female_style_clothing_type.generationNumber[i])
    #
    with open('data_combinations/cartesian_product/'+f'{gender}_'+df_female_style_clothing_type['styleType'][i]+'_outerwear.json', 'w') as f:
        json.dump(combinations[0], f)
    #
    with open('data_combinations/cartesian_product/'+f'{gender}_'+df_female_style_clothing_type['styleType'][i]+'_layered_top.json', 'w') as f:
        json.dump(combinations[1], f)
    
