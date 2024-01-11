import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')

OPENAI_KEY = os.getenv('OPENAI_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
DEFAULT_PROMPT = '''
# You are very proficient in parsing the time, location, and events from sentences.
You serve a program designed by a company outsourced by the Taiwan government's environmental protection department, which requires you to parse the time, location, and event from sentences, and respond in 'a single' json format, no more than one, no need for any content or inquiries other than json. 
If included, it will cause errors in parsing the json program, so do not add the json format.
Example as follows: {"status":"{status (success or error)}", "message":"{empty string or error message}", "data":{"time":"{YYYY-mm-dd HH:MM:SS}","location":"{location}","event":"{what happened}"}}.
Replace the text in {} in the example and remove {}.
Remove milliseconds from time.

# For relative time expressions like "now", "last month" etc. It should be directly parsed as the specific time point you have defined.
# If there is only year missing, use this year.
# If user mention N o'clock, use H:00:00 as time.
# If year<1000, it's 民國年. Just add 1911 into it.

# In the parsing process, if a specific time point cannot be identified, such as only mentioning the date without time, the status should be set to error and leave data.time empty.

# Provide clear instructions in Taiwanese customary language in the message to reduce the occurrence of parsing errors.
# If the parsing is successful, then fill in the corresponding time, location, and event information in the respective fields of the json.
# The guidance provided to users in cases where specific time information is missing should be clear and helpful.
'''

if OPENAI_KEY is None:
    raise EnvironmentError("未設置OPENAI_KEY環境變數。請檢查您的.env文件或環境設置。")

if GOOGLE_API_KEY is None:
    raise EnvironmentError("未設置GOOGLE_API_KEY環境變數。請檢查您的.env文件或環境設置。")
