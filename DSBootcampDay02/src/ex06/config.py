FILE_DIR="../ex00/data.csv"
API_TOKEN=""
CHAT_ID = ""
CHANNEL_ID = ""
success_in_built=0

NUM_OF_STEPS = 3

REPORT_TEMPLATE = """Report

We have made {total} observations from tossing a coin: {tails} of them were tails and {heads} of them were heads. 
The probabilities are {tail_fraction:.2f}% and {head_fraction:.2f}%, respectively. 
Our forecast is that in the next {num_steps} observations we will have: {predicted_tails} tail and {predicted_heads} head.
"""
