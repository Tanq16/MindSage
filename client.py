import requests
import sys
import os

def build_request_data():
    tt = input("GPT-3.5 (Y) or GPT-4 (n): ")
    model = "gpt4" if tt == "n" else "gpt3.5"
    tt = input("Entering a link? (Y/n): ")
    link = 0 if tt == "n" else 1
    if link:
        userin = input("Link: ")
    else:
        print("Enter text (write EOF to end): ")
        userin = ""
        while 1:
            tt = input()
            if not tt == "EOF":
                userin += tt
            else:
                break
    return {"model":model, "link":link, "input":userin}

actionlist = ['write_essay', 'summarize', 'analyze_claims', 'ai', 'create_mermaid_visualization', 'create_visualization', 'explain_docs', 'explain_code', 'extract_article_wisdom', 'extract_wisdom', 'find_logical_fallacies', 'improve_writing', 'write_semgrep_rule', 'extract_insights', 'create_logo']
defaultaction = "summarize"

def main():
    if len(sys.argv) > 1:
        r = requests.post("http://192.168.86.95:5000/" + defaultaction, headers={"Content-Type":"application/json"}, json=build_request_data())
    else:
        for i in range(len(actionlist)):
            print(i+1, ":", actionlist[i])
        action = input()
        r = requests.post("http://192.168.86.95:5000/" + actionlist[int(action)-1], headers={"Content-Type":"application/json"}, json=build_request_data())

    print()
    print("-------------------------------------------------------")
    print(r.text)

if __name__ == "__main__":
    main()

