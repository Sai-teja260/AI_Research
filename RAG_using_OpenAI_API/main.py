from openai_helper import ask_openai

def main():
    print("Welcome to the College Q&A System!")
    print("Type your question (or 'quit' to exit):")
    
    while True:
        question = input("> ")
        if question.lower() == "quit":
            print("Goodbye!")
            break
        
        try:
            answer = ask_openai(question)
            print("Answer:", answer)
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()
