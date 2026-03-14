import config
from analytics import Analytics

analytics = Analytics(config.DATA_FILE,config.NUM_OF_STEPS)
data = analytics.data
total = len(data)
heads, tails = analytics.counts()
head_fraction, tail_fraction = analytics.fractions()

predictions = analytics.predict_random()
predict_heads = sum(1 for p in predictions if p[0] == 1)
predict_tails = sum(1 for p in predictions if p[1] == 1)

report = config.REPORT_TEMPLATE.format(
    total=total,
    heads=heads,
    tails=tails,
    head_fraction=head_fraction,
    tail_fraction=tail_fraction,
    num_steps=config.NUM_OF_STEPS,
    predicted_heads=predict_heads,
    predicted_tails=predict_tails
)
print(report)
analytics.save_file(report,"report")