# Bring in deps
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import streamlit.components.v1 as components


# App framework
st.set_page_config(layout="wide")
st.title('💭Activity Recommendation App')

# Section for API Key Input
st.subheader('Enter Your API Key')
api_key = st.text_input('API Key', type='password')

# Check if the API key is entered to proceed
if api_key:
    st.success('API Key entered successfully.')
    os.environ['OPENAI_API_KEY'] = api_key
else:
    st.warning('Please enter your API Key to proceed.')
    
prompt = st.text_input('Enter your activity preferences for today:')

if st.button('Get Recommendations'):
    if prompt:
        results = ''
        suggestions = ''
        
        # Prompt templates
        plan_template = PromptTemplate(
            input_variables=['preferences'],
            template=(
                "AutoGPT, create two distinct itineraries for a full day in Baku based on these preferences: {preferences}. "
                "Format each plan with clear sections for morning, afternoon, evening, and night activities. "
                "For each section, provide one recommended activity or location, suitable for the time of day, "
                "and ensure all locations are within a reasonable travel distance from each other. "
                "The activities should be related to music, art, sports, and include dining options. "
                "The response format should be: "
                "Itinerary 1:"
                "Morning: [Activity/Location]"
                "Afternoon: [Activity/Location]"
                "Evening: [Activity/Location]"
                "Night: [Activity/Location]"
                "Itinerary 2:"
                "Morning: [Activity/Location]"
                "Afternoon: [Activity/Location]"
                "Evening: [Activity/Location]"
                "Night: [Activity/Location]"
                "Please provide diverse, engaging, and memorable suggestions for each part of the day. For each activity, make sentences"
                "as short as possible."
            )
        )

        # Memory
        plan_memory = ConversationBufferMemory(input_key='preferences', memory_key='chat_history')
        
        # LLMs
        llm = OpenAI(temperature=0.9, max_tokens=1000)
        plan_chain = LLMChain(llm=llm, prompt=plan_template, verbose=True, output_key='plan', memory=plan_memory)
        
        # Show stuff to the screen if there's a prompt
        if prompt:
            # Run the overall chain with the initial user prompt and Wikipedia research
            results = plan_chain.run(preferences=prompt)

            # Extract the plan and suggestions from the results
            suggestions = results

            def parse_itineraries(suggestions):
                parsed_sections = {}
                itinerary_1, itinerary_2 = suggestions.split("Itinerary 2:")
                
                parsed_sections['itinerary_1_morning'], others = itinerary_1.split("Afternoon: ")
                parsed_sections['itinerary_1_morning'] = parsed_sections['itinerary_1_morning'].replace("Itinerary 1:", "")
                parsed_sections['itinerary_1_morning'] = parsed_sections['itinerary_1_morning'].replace("Morning:", "")
                
                parsed_sections['itinerary_1_afternoon'], others = others.split("Evening: ")
                parsed_sections['itinerary_1_afternoon'] = parsed_sections['itinerary_1_afternoon'].replace("Afternoon:", "")
                
                parsed_sections['itinerary_1_evening'], others = others.split("Night: ")
                parsed_sections['itinerary_1_evening'] = parsed_sections['itinerary_1_evening'].replace("Evening:", "")
                
                parsed_sections['itinerary_1_night'] = others.replace("Night:", "")
                
                parsed_sections['itinerary_2_morning'], others = itinerary_2.split("Afternoon: ")
                parsed_sections['itinerary_2_morning'] = parsed_sections['itinerary_2_morning'].replace("Itinerary 2:", "")
                parsed_sections['itinerary_2_morning'] = parsed_sections['itinerary_2_morning'].replace("Morning:", "")
                
                parsed_sections['itinerary_2_afternoon'], others = others.split("Evening: ")
                parsed_sections['itinerary_2_afternoon'] = parsed_sections['itinerary_2_afternoon'].replace("Afternoon:", "")
                
                parsed_sections['itinerary_2_evening'], others = others.split("Night: ")
                parsed_sections['itinerary_2_evening'] = parsed_sections['itinerary_2_evening'].replace("Evening:", "")
                
                parsed_sections['itinerary_2_night'] = others.replace("Night:", "")

                return parsed_sections

            # Parse the itineraries using the suggestions from the GPT model
            parsed_itineraries = parse_itineraries(suggestions)

            # Access the individual sections
            itinerary_1_morning = parsed_itineraries['itinerary_1_morning']
            itinerary_1_afternoon = parsed_itineraries['itinerary_1_afternoon']
            itinerary_1_evening = parsed_itineraries['itinerary_1_evening']
            itinerary_1_night = parsed_itineraries['itinerary_1_night']
            itinerary_2_morning = parsed_itineraries['itinerary_2_morning']
            itinerary_2_afternoon = parsed_itineraries['itinerary_2_afternoon']
            itinerary_2_evening = parsed_itineraries['itinerary_2_evening']
            itinerary_2_night = parsed_itineraries['itinerary_2_night']
            
            # CSS Content
            css = """
                * {
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #333;
                }
            """
            
            # Inject CSS with Markdown
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
            
            # URL for the bullet point image (using an online accessible URL)
            bullet_point_url = "https://i.imgur.com/rWzrXDK.png"
            
           # HTML content with placeholders for itinerary variables
            html_content = f"""
            <html>
            <head>
                <style>/* Main part */
                h2 {{
                    color: #FFF;
                }}
                
                main {{
                    padding: 20px;
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #333;
                }}

                #daily-plans {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 50px;
                    justify-content: space-around;
                    width: 100%;
                }}

                .daily-plan {{
                    width: 400px; /* Adjust width as needed */
                    height: auto; /* Adjust height as needed */
                    border: 2px solid black;
                    text-align: center;background-color: #001F3F;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-around;
                    margin-left: 0;
                }}

                .daily-plan ul {{
                    list-style-type: none; /* Removes default list styling */
                    padding: 0; /* Removes default padding */
                    margin-left: 20px; 
                    display: flex;
                    flex-direction: column;
                    justify-content: space-around;
                }}

                .daily-plan ul li.plan-item {{
                    font-size: 16px;
                    line-height: 1.5;
                    color: #fff;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.2); 
                    text-align: left;
                }}

                .daily-plan ul li.plan-item:last-child {{
                    border-bottom: none; /* Removes the border from the last item */
                }}

                button {{
                    background-color: #3498db;
                    color: #fff;
                    border: none;
                    padding: 10px;
                    margin: 10px;
                    width: 100px;
                    height: 50px;
                    cursor: pointer;
                    transition: background-color 0.3s ease-in-out;
                }}

                button:hover {{
                    background-color: #2980b9;
                }}

                .plan-item {{
                    margin-bottom: 15px;
                    font-size: 16px;
                    line-height: 1.5;
                    padding-left: 0;
                    color: #3498db; /* or any other color that fits the back of the card */
                }}

                .icon {{
                    display: inline-block;
                    width: 17px; /* Adjust as necessary to match your actual icon size */
                    height: 17px; /* Adjust as necessary to match your actual icon size */
                    margin-top: 3px;
                    background-size: contain; /* Ensures the icon fits within the element */
                    background-repeat: no-repeat;
                    background-image: url({bullet_point_url}); /* Adjust the path if needed */
                }}
                </style>
            </head>
            <main>
                <section id="daily-plans">
                    <article class="daily-plan">
                        <h2>Baku Journey #1</h2>
                        <ul>
                            <li class="plan-item"><span class="icon");"></span>Morning: {itinerary_1_morning}</li>
                            <li class="plan-item"><span class="icon");"></span>Afternoon: {itinerary_1_afternoon}</li>
                            <li class="plan-item"><span class="icon");"></span>Evening: {itinerary_1_evening}</li>
                            <li class="plan-item"><span class="icon");"></span>Night: {itinerary_1_night}</li>
                        </ul>
                        <div class="buttons">
                            <button class="like-btn">Like</button>
                            <button class="save-btn">Save</button>
                        </div>
                    </article>
                    <article class="daily-plan">
                        <h2>Baku Journey #2</h2>
                        <ul>
                            <li class="plan-item"><span class="icon");"></span>Morning: {itinerary_2_morning}</li>
                            <li class="plan-item"><span class="icon"></span>Afternoon: {itinerary_2_afternoon}</li>
                            <li class="plan-item"><span class="icon");"></span>Evening: {itinerary_2_evening}</li>
                            <li class="plan-item"><span class="icon");"></span>Night: {itinerary_2_night}</li>
                        </ul>
                        <div class="buttons">
                            <button class="like-btn">Like</button>
                            <button class="save-btn">Save</button>
                        </div>
                    </article>
                </section>
            </main>
            """

            # Display the formatted HTML content with Streamlit variables
            components.html(html_content, height=1500, width=1000)

            # Display the history and Wikipedia research
            with st.expander('Plan History'):
                st.info(plan_memory.buffer)
    else:
        st.warning("Please enter some preferences to get recommendations.")