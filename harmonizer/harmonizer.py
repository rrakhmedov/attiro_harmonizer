import json
import pandas as pd
from ast import literal_eval

def get_value(list_values,column):
    if type(list_values)!=list:
        return list_values
    interim=[]
    for i in range(len(list_values)):
        interim.append(list_values[i][column])
    return interim

def text_to_priority_number(text):
    if text=='high':
        return float(2)
    if text=='low':
        return float(0.1)
    if text=='excluded':
        return float(0.0000001)
    else:
        return float(1)
    
#after cartesian
def split_correct(text,numb):
    if text=='empty':
        return text
    return text.split('-',1)[numb]

def get_parsed_cartesian_outfit(outfit, upper_clothes_category,  style_clothes_transcript):
    interim=pd.DataFrame(outfit).T.set_axis([upper_clothes_category,'top','bottom','footwear'],axis=1).T.reset_index(drop=False).rename(columns={'index':'category',0:'transcriptTypeParams'})
    interim=interim.merge(style_clothes_transcript,on=['transcriptTypeParams','category'])
    interim['paramCombinations']=interim['paramCombinations'].apply(lambda x: literal_eval(x) if type(x)!=float else x)
    interim=interim.explode('paramCombinations').reset_index(drop=True).fillna('empty')
    interim['clothesParameters']=interim.paramCombinations.apply(lambda x: split_correct(x,0))
    interim['values']=interim.paramCombinations.apply(lambda x: split_correct(x,1))
    return interim

    

class FashionHarmonizer():
    def __init__(self,gender_types_with_parameters, gender_types, type_parameters, gender_style_type  ) -> None:
        self.gender_types_with_parameters=gender_types_with_parameters
        self.gender_types=gender_types
        self.type_parameters=type_parameters
        self.gender_style_type=gender_style_type
        # self.ref_llm_style_types=ref_llm_style_types
        # self.ref_llm_style_types=ref_llm_style_types #now without llm
        # self.ref_llm_style_combination = ref_llm_style_combination
    
    def transform_jsons_flatten_df(self):
        gender_types_with_parameters_df=pd.DataFrame(self.gender_types_with_parameters)
        gender_types_df=pd.DataFrame(self.gender_types)
        type_parameters_df=pd.DataFrame(self.type_parameters)
        # merge to get parameter for each type
        df=gender_types_df.merge(gender_types_with_parameters_df, left_on='type', right_on='clothes_type',how='left')
        #flatten df to get more explicit view
        df['clothesParameters']=df.parameters.apply(lambda x: get_value(x,'name'))
        df=df[['category','subcategory','type','clothesParameters']].explode('clothesParameters')
        # merge to get value of parameter
        df=df.merge(type_parameters_df,left_on=['category','clothesParameters'],
            right_on=['type','name'],how='left')
        df=df[['category','subcategory','type_x','clothesParameters','values']].rename(columns={'type_x':'type'}).explode('values')
        self.main_df=df
        self.main_df['priorityProb'] = 1.0
         
    def filter_type_by_style(self, style_type):
        gender_style_type_df=pd.DataFrame(self.gender_style_type)
        gender_style_type_df['types']=gender_style_type_df.types.apply(lambda x: literal_eval(str(x)))
        gender_style_type_df=gender_style_type_df.explode('types')
        gender_style_type_df=gender_style_type_df[gender_style_type_df['styleType']==style_type]
        self.main_df=self.main_df.merge(gender_style_type_df,left_on='type',right_on='types').iloc[:,:7]

    def assign_priority_clothingtype_rule(self, value, rule_path):
        with open(rule_path) as f:
            rules = json.load(f)
        rules_df=pd.DataFrame(rules)
        rules_df['priorityProb']=rules_df.priorityType.apply(text_to_priority_number)
        rules_df = rules_df[rules_df['key']==value]
        # merge where paramName=None
        # change name here !
        self.main_df=self.main_df.merge(rules_df[rules_df['paramName'].isnull()],left_on=['type'],right_on=['clothesType'],how='left')\
        [['category', 'subcategory', 'type', 'clothesParameters', 'values', 'priorityProb_x', 'priorityProb_y','styleType']]
        self.main_df['priorityProb_y']=self.main_df['priorityProb_y'].fillna(1)
        self.main_df['priorityProb']=self.main_df['priorityProb_y']*self.main_df['priorityProb_x']
        self.main_df.drop(columns=['priorityProb_x','priorityProb_y'],inplace=True)
        # merge where not None
        self.main_df=self.main_df.merge(rules_df[~rules_df['paramName'].isnull()],
                                    left_on=['type','clothesParameters','values'],
                                    right_on=['clothesType','paramName','paramValue'],how='left')\
        [['category', 'subcategory', 'type', 'clothesParameters', 'values', 'priorityProb_x', 'priorityProb_y','styleType']]
        self.main_df['priorityProb_y']=self.main_df['priorityProb_y'].fillna(1)
        self.main_df['priorityProb']=self.main_df['priorityProb_y']*self.main_df['priorityProb_x']
        self.main_df.drop(columns=['priorityProb_x','priorityProb_y'],inplace=True)


    def assign_priority_outfit_by_rules(self, gender, style, season):
        with open(f'data_combinations/cartesian_product/{gender}_{style}_outerwear.json') as f:
            all_outfits_outerwear= json.load(f)
        with open(f'data_combinations/cartesian_product/{gender}_{style}_layered_top.json') as f:
            all_outfits_layered_top= json.load(f)
        style_clothes_transcript=pd.read_csv(f'data_combinations/{gender}_style_clothing_transcript.csv',index_col=0)[['category','subcategory','type','transcriptTypeParams','paramCombinations']]
        style_clothes_transcript['paramCombinations']=style_clothes_transcript['paramCombinations'].apply(lambda x: literal_eval if type(x)==list else x)
        self.main_df=self.main_df.fillna('empty')
        result=pd.DataFrame()
        for outfit in all_outfits_outerwear:
            interim= get_parsed_cartesian_outfit(outfit=outfit, 
                                                 upper_clothes_category='outerwear',  
                                                 style_clothes_transcript=style_clothes_transcript)
            interim.merge(self.main_df[self.main_df['priorityProb']!=1.0],on=['type','clothesParameters','values'],how='left')
            result=pd.concat([result,interim])
        return result
    
    

        # for outfit in all_outfits_layered_top:
        #     interim= get_parsed_cartesian_outfit(outfit=outfit, 
        #                                          upper_clothes_category='layered_top',  
        #                                          style_clothes_transcript=style_clothes_transcript)
        #     interim.merge(self.main_df[self.main_df['priorityProb']!=1.0],on=['type','clothesParameters','values'],how='left')