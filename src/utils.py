import itertools
import pandas as pd
def get_parameters_combinations(value):
    if type(value)!=list:
        return value
    result=[]
    for l in itertools.product(*value):
        result.append(list(l))
    return result

def get_param_value_union(list_values,column,column2):
    if type(list_values)!=list:
        return list_values
    interim=[]
    for i in list_values:
        params=i[column]
        params= [i[column2] + '-' + j for j in params]
        interim.append(params)
    return interim

def get_promt_text_params(clothing_type, parameters_combinations):
    if type(parameters_combinations)!=list:
        return clothing_type
    result=''
    for text in parameters_combinations:
        result+=' '+text
    # clothing_type=clothing_type.replace('_',' ')
    result=result+' '+clothing_type
    #get rid of blanks at start
    return result.lstrip(' ')

def get_df_with_clothing_parameters_transcript(gender_types,gender_types_with_parameters):
    gender_types_df=pd.DataFrame(gender_types)
    gender_types_with_parameters_df=pd.DataFrame(gender_types_with_parameters)
    df=gender_types_df.merge(gender_types_with_parameters_df, left_on='type', right_on='clothes_type',how='left')
            #flatten df to get more explicit view
    df['paramValueUnion']=df.parameters.apply(lambda x: get_param_value_union(x,'values','name'))
    df['paramCombinations']=df.paramValueUnion.apply(lambda x: get_parameters_combinations(x))
    df=df.explode('paramCombinations').reset_index(drop=True)
    df['transcriptTypeParams']=df.apply(lambda x: get_promt_text_params(clothing_type=x['type'],parameters_combinations=x['paramCombinations']),axis=1)
    return df 