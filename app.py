from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = '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'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.json.get('message')
        if message:
            response = get_bot_response(message)
        else:
            response = "Please enter a message"
        return jsonify({'response': response})
    else:
        return render_template('index.html')


def get_api_response(prompt: str) -> str:
    text: str = ''

    try:
        response: dict = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            temperature=0.9,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[' Human:', ' AI:']
        )

        choices: dict = response.get('choices')[0]
        text = choices.get('text','')

    except Exception as e:
        print('ERROR:', e)
        text ='Something went wrong...'

    return text


def update_list(message: str, pl: list[str]):
    pl.append(message)

def create_prompt(message: str, pl: list[str]) -> str:
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt

def get_bot_response(message: str) -> str:
    prompt_list: list[str] = ['You will pretend to be a psychologists and answer qustions professionally',
                              '\nHuman: What time is it?',
                              '\nAI: Its 12:00 PM']
    prompt: str = create_prompt(message, prompt_list)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, prompt_list)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:]
    else:
        bot_response = 'Something went wrong...'

    return str(bot_response)

if __name__ == '__main__':
    app.run(debug=True)