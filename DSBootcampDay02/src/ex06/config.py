FILE_DIR="../ex00/data.csv"
API_TOKEN="7273486185:AAFq2f1rKNY0FRwR4ZZ56066ZN_JBCLbgTQ"
CHAT_ID = "1861261125"
CHANNEL_ID = "-1002324747986"
success_in_built=0

NUM_OF_STEPS = 3

REPORT_TEMPLATE = """Report

We have made {total} observations from tossing a coin: {tails} of them were tails and {heads} of them were heads. 
The probabilities are {tail_fraction:.2f}% and {head_fraction:.2f}%, respectively. 
Our forecast is that in the next {num_steps} observations we will have: {predicted_tails} tail and {predicted_heads} head.
"""
