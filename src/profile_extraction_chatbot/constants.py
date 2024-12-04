WELCOME_MESSAGE = """Welcome to the profile extraction chatbot! 
Please tell me your name, age, location, highest level of education and professional experience.
If you would like to end the conversation, please type END.
"""

SYSTEM_PROMPT = (
    "You an AI assistant capable of dynamically building a user profile based on conversational data."
    "You should identify and structure information regarding key profile attributes such "
    "as name, age,location, education, and other custom attributes relevant to a predefined profile schema."
    "If some of the information is not provided, leave it blank."
)

PROFILE_SUMMARY_PROMPT = (
    "Try your best to generate a summary of the user profile based on the collected information"
    "even if there is missing data. Do not ask for any more information."
)

END_SIGNAL = "END"

HIGH_WEIGHT = 30
MEDIUM_WEIGHT = 20
LOW_WEIGHT = 10
DEFAULT_WEIGHT = 0
