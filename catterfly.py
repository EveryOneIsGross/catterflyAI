'''
This is very messy sorry, it executes and i think illustrates the idea well.
there is no error handling and lots of looping issues.
guiding prompts are delibrately general.
leaf logic is trash and needs defining.

originally the script was based on embeddings all input and using search and cosine logic to build each stage but I couldn't hold the idea in my brain so started over, it worked ish so I will add function back l8rz.

'''

import requests
import re
from rake_nltk import Rake
import textblob
from textblob import TextBlob
from gpt4all import GPT4All
from textwrap import shorten


MODEL_PATH = "orca-mini-3b.ggmlv3.q4_0.bin"

def abstract_input(input_str):
    r = Rake()
    r.extract_keywords_from_text(input_str)
    return r.get_ranked_phrases()

# Previous get_highest_ranked_noun function (now outside the Caterpillar class)

def get_highest_ranked_noun(input_str):

    blob = TextBlob(input_str)
    nouns = list(blob.noun_phrases)  # Extract noun phrases
    if not nouns:  # If no nouns are found, return an empty string
        return ""
    # Extract keywords using Rake
    r = Rake()
    r.extract_keywords_from_text(input_str)
    ranked_keywords = r.get_ranked_phrases()
    # Find the highest-ranked noun
    for keyword in ranked_keywords:
        for noun in nouns:
            if noun in keyword:
                return noun  # Return the first highest-ranked noun found
    return nouns[0]  # Return the first noun as a fallback

class Caterpillar:
    def __init__(self, model, agent_name):
        self.model = model
        self.path_taken = []
        self.agent_name = agent_name  # Use the agent_name provided during instantiation



    def navigate_leaf(self, user_input, max_nodes=10, match_count=0):
        # Base cases for recursion
        if max_nodes <= 0 or match_count >= 3:
            return

        keywords = abstract_input(user_input)
        prompt = f"By understanding {', '.join(keywords)}, describe {self.agent_name} :"

        decision = self.model.generate(prompt, max_tokens=15, temp=1, repeat_penalty=1.5).strip()
        # Remove nouns from decision
        blob = TextBlob(decision)
        nouns = list(blob.noun_phrases)
        for noun in nouns:
            decision = decision.replace(noun, '').strip()

        self.path_taken.append({"keywords": keywords, "decision": decision, "agent_name": self.agent_name})
       
        print(f"Node Decision for {self.agent_name} - {decision}")
        print("Keywords:", keywords)
        print("Decision:", decision)
        # Check if the decision contains any of the extracted keywords
        # Inside the navigate_leaf method
        matched = any(keyword.lower() in decision.lower() for keyword in keywords)
        print("Matched:", matched)
        if matched:
            max_nodes -= 4  # You can adjust this decrement value if needed
            match_count += 1
        else:
            max_nodes -= 2

        # Proceed with the next navigation if required
        if max_nodes > 0:
            self.navigate_leaf(decision, max_nodes, match_count)



def wikipedia_search(query):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'utf8': 1,
        'srsearch': query
    }

    response = requests.get(url, params=params)
    data = response.json()
    results = []
    for i in data['query']['search']:
        # Strip HTML tags using a regex pattern
        clean_snippet = re.sub('<.*?>', '', i['snippet'])
        results.append(i['title'] + ': ' + clean_snippet)
    return "\n".join(results)



class Cocoon:
    def __init__(self, caterpillar_path, user_query, agent_name):
        self.path = caterpillar_path
        self.user_query = user_query
        self.agent_name = agent_name
        self.personality_traits = self.construct_personality()
        print(f"Agent Name: {self.agent_name}")


    def decision_based_vocabulary_expansion(self, vocabulary):
        for entry in self.path:
            vocabulary.append(entry['decision'])
        return vocabulary

    def construct_personality(self):
        vocabulary = self.user_query.split()
        vocabulary = self.decision_based_vocabulary_expansion(vocabulary)
        # Return top 3 keywords as personality traits
        return abstract_input(' '.join(vocabulary))[:3]

class Butterfly:
    def __init__(self, model, personality_traits, agent_name):
        self.model = model
        self.traits = personality_traits
        self.agent_name = agent_name
        self.last_response = ""
        print(f"{self.agent_name} Initialized with traits:", personality_traits)


    def interact(self, input_text):
        system_prompt = (f"You are {self.agent_name} with memories of {', '.join(self.traits)}, based on the last interaction: "
                         f"{self.last_response}. Respond strictly in character as {self.agent_name} answer {input_text}:")
        sentiment = textblob.TextBlob(input_text).sentiment.polarity

        tokens, temp = (1000, 0.6) if sentiment > 0 else (500, 0.7) if sentiment == 0 else (250, 0.5)
        self.last_response = self.model.generate(system_prompt, max_tokens=tokens, temp=temp, repeat_penalty=1.5).strip()
        return self.last_response


class TheyHazTools:
    def __init__(self, model, personality_traits, tools=[]):
        self.model = model
        self.traits = personality_traits
        self.available_tools = tools
        self.current_chat_session = []
        self.last_response = ""  # Store the last response here

    def handle_tool_interaction(self, input_text):
        selected_tool = next((tool for tool in self.available_tools if tool.lower() in input_text.lower()), None)
        
        if selected_tool:
            if selected_tool == "Wikipedia":
                results = wikipedia_search(input_text)
                summarized_results = shorten(results, width=512)  # Summarize the results to a manageable length
                print(f"Using Tool '{selected_tool}' for interaction.")
                response = summarized_results
            else:
                response = "Tool not supported yet."  # Placeholder for other tools in the future
            return response
        else:
            return None  # Return None if no tool-based interaction is identified


# Create an instance of the GPT4All model
model = GPT4All(MODEL_PATH)

# Initialization for Caterpillar
input_str_for_caterpillar = input("Enter your input for the caterpillar: ")
agent_name = get_highest_ranked_noun(input_str_for_caterpillar)  # Extract agent_name here
# Instantiate the Caterpillar
caterpillar = Caterpillar(model, agent_name)
caterpillar.navigate_leaf(input_str_for_caterpillar)
cocoon = Cocoon(caterpillar.path_taken, input_str_for_caterpillar, caterpillar.agent_name)
selected_tools = ["Wikipedia"]
print(f"Selected Tools: {selected_tools}")
# Instantiate Butterfly and TheyHazTools
butterfly = Butterfly(model, cocoon.personality_traits, cocoon.agent_name)
tools_handler = TheyHazTools(model, cocoon.personality_traits, selected_tools)

# Interaction loop
while True:
    input_str = input("Enter your input for the butterfly: ")
    if input_str.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break

    # Check for tool-based interactions
    tool_response = tools_handler.handle_tool_interaction(input_str)
    
    if tool_response:
        # If there's a tool-based interaction, print the tool's response
        print(tool_response)
        butterfly.last_response = tool_response  # Update butterfly's last response with the tool's response
    else:
        # Otherwise, proceed with a regular Butterfly interaction
        butterfly_response = butterfly.interact(input_str)
        print(butterfly_response)  # Print the generated response
