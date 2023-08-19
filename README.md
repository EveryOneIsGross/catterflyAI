![catterfly](https://github.com/EveryOneIsGross/catterflyAI/assets/23621140/d2ee9a71-bbb5-4629-8d01-964bfb117fbd)

catterfly is a unique framework that imitates the life cycle of a butterfly to embody the query, define it and then chat with the user as a construction of that initial input.

It is represented as three states:

## Caterpillar Phase:

Biological: The caterpillar consumes and learns about its environment, growing and preparing for its transformation.

catterfly: The Caterpillar class makes decisions based on user input and constructs a path based on this input. This phase is about consuming information and setting the foundation.

## Cocoon Phase:

Biological: In the chrysalis, the caterpillar undergoes complete liquification and transformation. Many structures of the caterpillar are broken down into their basic components and are reconstructed to form the new structures of the butterfly.

catterfly: The Cocoon class takes the decisions (path) from the Caterpillar phase and constructs a 'personality' (akin to the new structures of the butterfly). This is a transformational phase where the input is distilled into a new context or perspective.

## Butterfly Phase:

Biological: The butterfly emerges with a completely different form, with wings and other structures that allow it to interact with its environment in entirely new ways. It now perceives and interacts with the world differently than when it was a caterpillar.

catterfly: The Butterfly class, informed by the constructed 'personality', interacts with the user in a dynamic manner. It has a 'memory' of past interactions (last response) and interacts based on that and the user's input, offering a new dimensional context. The idea of a caterpillar's mind being "dissolved" before being reconstructed is analogous to the process of taking user input, abstracting and breaking it down, and then reformulating it with a new "personality" or context. It also has basic tool use being able to search wikipedia and add the result into chat context. 

In both the biological phenomenon and with catterfly, there's a theme of transformation and renewal — the idea that something can be broken down to its core components and then rebuilt into something new and different, with the capacity for new types of interactions.

---
![catterfly_flow](https://github.com/EveryOneIsGross/catterflyAI/assets/23621140/0f5763f5-5201-4786-9b57-8fe31bb2443c)

A user's query was generated. This input calls the Caterpillar. But every being needed an identity, a name. The function, get_highest_ranked_noun, was invoked. It summoned the powers of TextBlob and Rake, scanning the user's query, searching for nouns that stood out. With its newfound name, the Caterpillar was ready to embark on its journey.

(This part correlates to the initialization and the naming of the Caterpillar based on the user's input.)

Guided by its purpose, the Caterpillar began its quest to understand the user's intent. It employed abstract_input, extracting the essence of the query, the keywords that held meaning. With each iteration, it delved deeper, questioning its own understanding, trying to describe the essence of its name in the context of the user's query. But the universe threw a twist: the Caterpillar was forbidden to use nouns in its decisions. It had to think abstractly, focusing on actions and descriptions.

(This is the recursive function navigate_leaf, where the Caterpillar continuously seeks understanding by generating decisions based on keywords and avoids using nouns.)

As the Caterpillar ventured forth, it left a trail of decisions in its wake. These decisions, stored in path_taken, were not just memories; they were lessons, insights into its evolving understanding. And as it faced challenges, it had to decide whether to forge ahead or to retrace its steps, adjusting its path based on matches to the user's intent.

(This illustrates the logic where the Caterpillar checks if its decisions match the extracted keywords and decides how many steps to proceed or backtrack.)

Having gathered enough wisdom, the Caterpillar entered a phase of introspection. This was the Cocoon phase. It examined its journey, piecing together its experiences to form a coherent personality. By melding its original user query with the decisions it made, the Cocoon derived traits that would define its next form.

(This represents the Cocoon class, which takes the Caterpillar's path and constructs personality traits for the next phase.)

From the Cocoon emerged the Butterfly, a being of wisdom and grace. It held memories of its past form, the traits derived from its journey. It was now ready to interact with the universe, responding to queries with the wisdom it had accumulated. But it was cautious; it would only recall its past responses a limited number of times, ensuring it didn't get trapped in its own echo chamber.

(The Butterfly class denotes the evolution of the Caterpillar, now ready to interact based on its derived traits and past interactions, but with a limit on feedback loops.)

In its interactions, the Butterfly had help. They were the Tools, repositories of vast knowledge like 'Wikipedia'. They would provide answers to questions that were beyond the Butterfly's experience. And so, with the assistance of TheyHazTools, the Butterfly could tap into these vast resources when needed.

(This is the integration of external tools, like Wikipedia, to assist in answering certain user queries.)
