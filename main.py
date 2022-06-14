import openai
from few_shots_examples import *
import streamlit as st

KEY = "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"
WORD_IN_LINE = 20
CHARS_IN_LINE = 65
SEPARATE = "\n###\n"

examples = DESCRIPTION + desc1 + "\n" + GREETING + greet1 + SEPARATE + DESCRIPTION + desc2 + "\n" + GREETING + greet2 + SEPARATE + \
           DESCRIPTION + desc3 + "\n" + GREETING + greet3 + SEPARATE + DESCRIPTION + desc4 + "\n" + GREETING + greet4 + SEPARATE + \
           DESCRIPTION + desc5 + "\n" + GREETING + greet5 + SEPARATE + DESCRIPTION + desc6 + "\n" + GREETING + greet6 + SEPARATE + \
           DESCRIPTION

# DESCRIPTION + desc7 + "\n" + GREETING + greet7 + SEPARATE + \ + DESCRIPTION + desc8 + "\n" + GREETING + greet8 + SEPARATE + \
# DESCRIPTION + desc9 + "\n" + GREETING + greet9 + SEPARATE + DESCRIPTION + desc10 + "\n" + GREETING + greet10 + SEPARATE + \


class Description:
    def __init__(self, name, event, characteristics, relation, mutual_exp, anything_else):
        self.name = name
        self.event = event
        self.characteristics = characteristics
        self.relation = relation
        self.mutual_exp = mutual_exp
        self.anything_else = anything_else
        self.desc = ""

    def create_desc(self):
        self.desc = f"write a personal greeting for {self.name} for {self.event}.\n"
        if len(self.characteristics) > 0 or self.characteristics != "none":
            self.desc += f"refer to {self.name} personality: "
            self.desc += (" ".join([f"{self.name} is {characteristic}, " for characteristic in self.characteristics.split(", ")])).replace("  ",
                                                                                                                                           " ") + \
                         "\n"
        if self.relation != "none":
            self.desc += f"refer to our relation: we are {self.relation}.\n"
        if self.mutual_exp != "none":
            self.desc += f"refer to our mutual experiences: {self.mutual_exp}.\n"
        if self.anything_else != "none":
            self.desc += f"{self.anything_else}.\n"


def get_desc():
    name = input("To whom would you like to write a greeting?\n")
    event = input("for which event?\n")
    characteristics = input(f"what defines {name}? (write characteristic: character1, character2, ... -> {name} is character1, {name} "
                            f"is character2, ...\n")
    relation = input(f"What is the relation between {name} and you?\n")
    mutual_exp = input("is there any mutual experiences that you would like to share?\n")
    anything_else = input("is there anything that you would like to add?\n")
    desc = Description(name, event, characteristics, relation, mutual_exp, anything_else)
    desc.create_desc()
    return desc


# def write_pretty(text):
#     i = 0
#     for word in text.split(" "):
#         print(word, end=" ")
#         # sleep(.1)
#         if "\n" in word:
#             i = 0
#         if i > 0 and i % WORD_IN_LINE == 0:
#             print()
#         i += 1


def str_pretty(text):
    str = ""
    i = 0
    for word in text.split(" "):
        i += (1 + len(word))
        if "\n" in word:
            i = 0
        if i > CHARS_IN_LINE:
            str += "\n"
            i = 0
        str += word
        str += " "
    return str


def activate_gpt(text):
    openai.api_key = KEY
    print(text)
    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=text,
        temperature=0.9,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text


def run():
    st.title("Greeting Generator")
    mode = st.radio(label="mode", options=("Zero shots", "Few shots"), horizontal=True)
    name = st.text_input("To whom would you like to write a greeting?")
    event = st.text_input("for which purpose or event?")
    characteristics = st.text_input(f"what defines {name}?", value=f"character1, character2, ... -> {name} is character1, {name} is character2, ...")
    relation = st.text_input(f"What is the relation between {name} and you?")
    mutual_exp = st.text_input("is there any mutual experiences that you would like to share?", value="none")
    anything_else = st.text_input("is there anything that you would like to add?", value="none")
    person_description = Description(name, event, characteristics, relation, mutual_exp, anything_else)
    person_description.create_desc()
    description = examples + person_description.desc + GREETING if mode == "Few shots" else person_description.desc
    # if st.button("description"):
    #     st.text(str_pretty(description))
    if st.button("generate"):
        greeting = activate_gpt(description)
        st.text(str_pretty(greeting))


run()
