import openai
from bs4 import BeautifulSoup
import asyncio
import os
from pyppeteer import launch
from pyppeteer_stealth import stealth

# Set up OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')


async def browse_url(url: str):
  # Launch the browser
  browser = await launch(ignoreHTTPSErrors=True, args=['--no-sandbox'])
  # browser = await launch()
  
  # Create a new page
  page = await browser.newPage()
  # await stealth(page)
  
  # Define the URL you want to open
  
  # Open the URL
  await page.goto(url)
  
  # Wait for some time (e.g., 5 seconds) to allow the page to load completely
  await asyncio.sleep(5)
  rendered_content = await page.content()
  # Close the browser
  await browser.close()
  return rendered_content

def extract_text(html_content: str):
  # Parse the HTML content
  soup = BeautifulSoup(html_content, 'html.parser')

  # Extract the text from the HTML
  text = soup.get_text()
  return text

async def answer_from_url(url: str, question: str):
  # Get the HTML content of the URL
  html_content : str = await browse_url(url)
  
  # Extract the text from the HTML content
  text = extract_text(html_content)

  messages = [
    {'role': 'system', 'content': f'''Answer the following question from user in CSV format with header using context: 
{text}
'''},
    {'role': 'user', 'content': question},
  ]

  completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=messages
  )
  print(completion.choices[0].message)

  # Return the answer
  return [text, completion]


# Run the async function to open the URL
res: str = asyncio.get_event_loop().run_until_complete(answer_from_url("https://www.unsw.edu.au/study/undergraduate/bachelor-of-environmental-management?studentType=International", 
  "what is the duration of the course, fees and entry requirements?"))

print("result: ", res)


