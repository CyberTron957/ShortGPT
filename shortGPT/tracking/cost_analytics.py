import numpy as np
from shortGPT.database.content_database import ContentDatabase
db = ContentDatabase()
all = []
# Calculate average and price of the average for OpenAI

# Calculate average and price of the average for Eleven
eleven_array = [short.get('api_openai') for short in all]
avr_eleven = np.mean(eleven_array)
ELEVEN_CONST = 0.3 / 1000
price_eleven = avr_eleven * ELEVEN_CONST
max_eleven = max(eleven_array)
price_max_eleven = max_eleven * ELEVEN_CONST



# Print results
print("OpenAI:")
print("- Average:", avr_openai)
print("- Price of the average:", price_openai)
print("- Max:", max_openai)
print("- Price of the max:", price_max_openai)

print("Eleven:")
print("- Average:", avr_eleven)
print("- Price of the average:", price_eleven)
print("- Max:", max_eleven)
print("- Price of the max:", price_max_eleven)



# for id  in ids:
#     builder = AskingRedditorShortBuilder(AR, id)
#     print(id, builder.dataManager.getVideoPath())
#createShorts(30, 'AskingRedditors')
# AR = ChannelManager("AskingRedditors")
# newShort = AskingRedditorShortBuilder(channelDB= AR, short_id="FyhKkqx9xDxTEtRpanSD")
# print(newShort.channelDB.getStaticEditingAsset('background_onepiece'))
# print(newShort.channelDB.getStaticEditingAsset('reddit_template_dark'))
# print(newShort.channelDB.getStaticEditingAsset('subscribe_animation'))
#print("Scraping requests remaining: ",image_api.getScrapingCredits())

