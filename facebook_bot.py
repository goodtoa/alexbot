import os, time, random
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from openai import OpenAI

load_dotenv(os.path.expanduser("~/.env"))
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
FB_EMAIL = os.getenv("FB_EMAIL")
FB_PASS = os.getenv("FB_PASS")
client = OpenAI(api_key=OPENAI_KEY)

GROUPS = [
    "https://www.facebook.com/groups/virtualassistantjobs",
    "https://www.facebook.com/groups/freelancejobsonline",
    "https://www.facebook.com/groups/hireavirtualassistant",
]

def generate_response(post_text):
    prompt = "You are Alex, a freelance assistant. Write a 3-5 sentence response to this job post: " + post_text + ". Never start with I. Reference the job specifically. State you can deliver fast. End with a confident offer. Sound human. No buzzwords."
    response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content

def login(page):
    page.goto("https://www.facebook.com")
    page.wait_for_load_state("networkidle")
    page.fill("input[name=email]", FB_EMAIL)
    page.fill("input[name=pass]", FB_PASS)
    page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    print("Logged in")

def scrape_and_reply(page, group_url):
    page.goto(group_url)
    page.wait_for_load_state("networkidle")
    time.sleep(5)
    page.screenshot(path="/root/fb_group.png")
    print("Screenshot saved for:", group_url)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    page = context.new_page()
    login(page)
    page.screenshot(path="/root/fb_login.png")
    print("Login screenshot saved")
    for group in GROUPS:
        scrape_and_reply(page, group)
        time.sleep(random.randint(5, 10))
    browser.close()
