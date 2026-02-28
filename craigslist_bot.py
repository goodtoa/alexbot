import os, time, random
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from openai import OpenAI

load_dotenv(os.path.expanduser("~/.env"))
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ALEX_EMAIL = os.getenv("ALEX_EMAIL")
client = OpenAI(api_key=OPENAI_KEY)

def generate_response(job_title):
    prompt = "You are Alex, a freelance assistant. Write a 3-5 sentence response to this Craigslist job post: " + job_title + ". Never start with I. Reference the job specifically. State you can deliver fast. End with a confident offer. Sound human."
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

def reply_to_post(page, post_url, job_title):
    page.goto(post_url)
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    reply_button = page.query_selector("button.reply-button, a.reply-button, #replylink")
    if reply_button​​​​​​​​​​​​​​​​
