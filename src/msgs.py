def get_right_msg(style, season, number,list_promtTypeParams, tmplt):
    list_input_format='''[{'clothing_category1':['value1','value2'....]},{'clothing_category2':['value1','value2'....]},...]'''
    if season=='winter':
        msg = f'''
        I'm going to give you a clothing style, season for combinations, a list of clothing types with their parameters, and I want:

        Combine types of clothing with each other if you think that the combination of clothes fits the specified style, season, and fits the look that is fashionable to wear. 
        Provide all combinations. Exclude combinations, if they are not matching with the input conditions.


        Input format:
        Number of output outfits: number
        Clothing style: "style"
        Season for outfits: "season"
        List of clothing types: {list_input_format}

        output format:


        [
        {
        tmplt
        },
        …
        ]

        It is very important. Categories outerwear, top, bottom, footwear can not be null
        It is very important. Categories outerwear and top should match each other.
        It is very important. Do not forget, it is very cold outside. Do not recommend items which are not suitable for such weather, like leather jacket or bomber or windbreaker

        Now do the work for the following input:
        Number of output outfits: {number}
        Clothing style: {style}
        Season: {season}
        List of clothing types: {list_promtTypeParams}

        It is very important that you only provide the final output without any additional comments or remarks
        It is very important not add colours to outfits. 
        It is very important only using data from "List of clothing types" as they are written without adding or changing format
        It is very important to return {number} different outfits
        '''
    if season=='summer':
        msg = f'''
                I'm going to give you a clothing style, season for combinations, a list of clothing types with their parameters, and I want:

                Combine types of clothing with each other if you think that the combination of clothes fits the specified style, season, and fits the look that is fashionable to wear. 
                Provide all combinations. Exclude combinations, if they are not matching with the input conditions.


                Input format:
                Number of output outfits: number
                Clothing style: "style"
                Season for outfits: "season"
                List of clothing types: {list_input_format}
                

                output format:


                [
                {
                tmplt
                },
                …
                ]

                It is very important.Category layered_top can be null but in this case category top cannot be null and vice versa
                It is very important. Categories top, bottom, footwear can not be null
                It is very important. Categories layered_top and top should match each other. For example. layered_top=sweatshirt does not match top = tank_top
                It is very important. Do not forget, it is hot outside. Do not recommend items which are not suitable for such weather.

                Now do the work for the following input:
                Number of output outfits: {number}
                Clothing style: {style}
                Season: {season}
                List of clothing types: {list_promtTypeParams}

                It is very important that you only provide the final output without any additional comments or remarks
                It is very important not add colours to outfits. 
                It is very important only using data from "List of clothing types" as they are written without adding or changing format
                It is very important to return {number} different outfits
                '''
    if season=='spring':
            msg = f'''
                        I'm going to give you a clothing style, season for combinations, a list of clothing types with their parameters, and I want:

                        Combine types of clothing with each other if you think that the combination of clothes fits the specified style, season, and fits the look that is fashionable to wear. 
                        Provide all combinations. Exclude combinations, if they are not matching with the input conditions.


                        Input format:
                        Number of output outfits: number
                        Clothing style: "style"
                        Season for outfits: "season"
                        List of clothing types: {list_input_format}


                        output format:


                        [
                        {
                        tmplt
                        },
                        …
                        ]

                        It is very important.Category layered_top can be null but in this case category top cannot be null and vice versa
                        It is very important. Categories top, bottom, footwear can not be null
                        It is very important. Categories layered_top and top should match each other. For example. layered_top=sweatshirt does not match top = tank_top
                        It is very important. Do not forget, it is not that cold outside but still not too hot. Do not recommend items which are not suitable for such weather.

                        Now do the work for the following input:
                        Number of output outfits: {number}
                        Clothing style: {style}
                        Season: {season}
                        List of clothing types: {list_promtTypeParams}

                        It is very important that you only provide the final output without any additional comments or remarks
                        It is very important not add colours to outfits. 
                        It is very important only using data from "List of clothing types" as they are written without adding or changing format
                        It is very important to return {number} different outfits
                    '''
    if season=='autumn':
         msg = f'''
                    I'm going to give you a clothing style, season for combinations, a list of clothing types with their parameters, and I want:

                    Combine types of clothing with each other if you think that the combination of clothes fits the specified style, season, and fits the look that is fashionable to wear. 
                    Provide all combinations. Exclude combinations, if they are not matching with the input conditions.


                    Input format:
                    Number of output outfits: number
                    Clothing style: "style"
                    Season for outfits: "season"
                    List of clothing types: {list_input_format}

                    output format:


                    [
                    {
                    tmplt
                    },
                    …
                    ]

                    It is very important. Categories outerwear, top, bottom, footwear can not be null
                    It is very important. Categories outerwear and top should match each other.
                    It is very important. Do not forget, it is cold and might be rainy outside. Do not recommend items which are not suitable for such weather, like parka or down_jacket

                    Now do the work for the following input:
                    Number of output outfits: {number}
                    Clothing style: {style}
                    Season: {season}
                    List of clothing types: {list_promtTypeParams}

                    It is very important that you only provide the final output without any additional comments or remarks
                    It is very important not add colours to outfits. 
                    It is very important only using data from "List of clothing types" as they are written without adding or changing format
                    It is very important to return {number} different outfits
                    '''
    return msg


#                    List of clothing types: [
#                    "value",
 #                   "value",
 #                   "value",
 #                   …
 #                   ]