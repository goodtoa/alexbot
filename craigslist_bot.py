import os, time, random
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from openai import OpenAI

load_dotenv(os.path.expanduser("~/.env"))
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ALEX_EMAIL = os.getenv("ALEX_EMAIL")
client = OpenAI(api_key=OPENAI_KEY)

def generate_response(job_title):
    prompt = "You are Alex, a freelance assistant. Write a 3-5 sentence response to this Craigslist job: " + job_title + ". Never start with I. Reference the job. Deliver fast. Confident offer. Sound human."
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

def reply_to_post(page, post_url, job_title):
    page.goto(post_url)
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    reply_button = page.query_selector("button.reply-button, a.reply-button, #replylink")
    if reply_button:
        reply_button.click()
        time.sleep(2)
        email_field = page.query_selector("input[type=email]")
        if email_field:
            email_field.fill(ALEX_EMAIL)
        message_field = page.query_selector("textarea")
        if message_field:
            reply = generate_response(job_title)
            message_field.fill(reply)
            submit = page.query_selector("button[type=submit]")
            if submit:
                submit.click()
                print("Reply sent for:", job_title)
                time.sleep(random.randint(30, 60))
    else:
        print("No reply button for:", job_title)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    page = context.new_page()
    page.goto("https://newyork.craigslist.org/search/cpg")
    page.wait_for_load_state("networkidle")
    posts = page.query_selector_all("a.posting-title")
    job_list = []
    for post in posts[:3]:
        title = post.inner_text()
        url = post.get_attribute("href")
        job_list.append((title, url))
    for title, url in job_list:
        print("Found job:", title)
        reply_to_post(page, url, title)
        time.sleep(random.randint(5, 10))
    browser.close()
