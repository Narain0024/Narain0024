# Add a dict here for every repo you want on a notebook page, then run:  python3 tools/build.py
# doodle options: prompts | finance | esp32 | arduino | robot | gear | chart
PROJECTS = [
    dict(slug="my-prompts", name="My-Prompts",
         blurb="A growing library of prompts for LLM workflows: written, tested, tweaked, repeated.",
         stack=["Prompt design", "LLM workflows"],
         repo="https://github.com/Narain0024/My-Prompts", doodle="prompts", tilt=-1.4),
    dict(slug="finance-tracker", name="my-finance-tracker",
         blurb="A small web app for keeping an eye on money, built with plain HTML, CSS and JavaScript.",
         stack=["HTML", "CSS", "JavaScript"],
         repo="https://github.com/Narain0024/my-finance-tracker", doodle="finance", tilt=1.2),
]
