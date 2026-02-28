import os, time, random, json
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from openai import OpenAI

load_dotenv(os.path.expanduser("~/.env"))
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
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

def load_cookies(context):
    with open("/root/fb_cookies.json", "r") as f:
        cookies = json.load(f)
    for cookie in cookies:
        cookie.pop("storeId", None)
        cookie.pop("hostOnly", None)
        cookie.pop("session", None)
        if cookie.get("sameSite") == "no_restriction":
            cookie["sameSite"] = "None"
        if cookie.get("sameSite") is None:
            cookie["sameSite"] = "Lax"
    context.add_cookies(cookies)

def scrape_and_reply(page, group_url):
    page.goto(group_url)
    page.wait_for_load_state("networkidle")
    time.sleep(5)
    page.screenshot(path="/root/fb_group.png")
    print("Screenshot saved for:", group_url)
    print("URL:", page.url)
    print("Title:", page.title())

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    load_cookies(context)
    page = context.new_page()
    page.goto("https://www.facebook.com")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.screenshot(path="/root/fb_home.png")
    print("Home URL:", page.url)
    print("Home Title:", page.title())
    for group in GROUPS:
        scrape_and_reply(page, group)
        time.sleep(random.randint(5, 10))
    browser.close()
