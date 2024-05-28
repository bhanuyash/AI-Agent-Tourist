from flask import Flask, request, make_response,jsonify
import pandas as pd
from flask_cors import CORS
from aiagent import AI_AGENT
from tqdm import tqdm


# app = Flask(__name__)
# CORS(app)

# @app.route('/ATS/train_model', methods=['POST'])
def get_tourist_info(city_name):
    ai_agent = AI_AGENT()
    country_of_city = ai_agent.open_ai_completion(system_prompt= "Strictly only give me one word/entity answer",
                                                       user_prompt=f"Which country is {city_name} situated in?")
    
    print(country_of_city,"\n")
    tourist_attractions = ai_agent.open_ai_completion(system_prompt= "Strictly give me the answer as a list in comma separated values",
                                                    user_prompt=f"give me a list of all attractions in {city_name}")
    print(tourist_attractions)
    
    tourist_attractions_list = tourist_attractions.split(",")
    
    details = []

    for attraction in tqdm(tourist_attractions_list,desc="Fetching details for each attraction"):
        
        description = ai_agent.open_ai_completion(system_prompt="Strictly give me a detailed description in minimum 2000 characters and maximum 2500 characters.",
                                                        user_prompt=f"Give details that would be useful for a tourist about {attraction} in {city_name}")
        
        gemini_desc = ai_agent.gemini_completion(system_prompt="Strictly give me a detailed description in minimum 2000 characters and maximum 2500 characters.",
                               user_prompt=f"Give details that would be useful for a tourist about {attraction} in {city_name}")
        details.append({
            "Country": country_of_city,
            "City": city_name,
            "Attraction": attraction,
            "CHAT GPT Description": description,
            "Gemini Description": gemini_desc,
        })

    df = pd.DataFrame(details)
    
    df.to_excel("tourist_info.xlsx", index=False)
    
    return df
    
    
    
if __name__ == '__main__':
    city_name = "Bangalore"
    df = get_tourist_info(city_name)
    print("\n",df)
    # app.run(debug=True, host="0.0.0.0", port=5001)