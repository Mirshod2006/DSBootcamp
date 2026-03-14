from analytics import Research, Analytics
import config

if __name__ == '__main__':
    research = Research(config.FILE_DIR)
    analytics = Analytics(research.file_read(),config.NUM_OF_STEPS)
    predictions=analytics.predict_random()
    predict_heads, predict_tails=research.Calculations(predictions).counts()

    report = config.REPORT_TEMPLATE.format(
        total=research.head+research.tail,
        heads=research.head,
        tails=research.tail,
        head_fraction=research.head_fraction,
        tail_fraction=research.tail_fraction,
        num_steps=config.NUM_OF_STEPS,
        predicted_heads=predict_heads,
        predicted_tails=predict_tails
    )
    analytics.save_file(report,"report")
    research.send_message_telegram()