from flask import Flask, request, jsonify
from unsloth import FastLanguageModel
import torch

app = Flask(__name__)

# Model configuration
max_seq_length = 2084
dtype = None
load_in_4bit = True


model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "models/lora_model",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)
FastLanguageModel.for_inference(model) 


@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.get_json()

    # Extract instruction and input from the request
    instruction = data.get('instruction')
    user_input = data.get('input')

    if not instruction or not user_input:
        return jsonify({"error": "Both 'instruction' and 'input' are required."}), 400

    # Prepare the prompt for the model
    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    {}

    ### Input:
    {}

    ### Response:
    {}"""
    
    
    print(alpaca_prompt.format(instruction.replace("\n",''), user_input.strip(), ""))

    inputs = tokenizer(
    [
        alpaca_prompt.format(
            instruction, # instruction
            user_input, # input
            "", # output - leave this blank for generation!
        )
    ], return_tensors = "pt").to("cuda")

    # Generate the response from the model
    outputs = model.generate(**inputs, max_new_tokens = 150, use_cache = True)
    finalOutput = tokenizer.batch_decode(outputs)
    print("\n\n")
    print("*"*50)
    print(finalOutput)
    print("*"*50)
    
    # Extract the generated response
    finalResp = finalOutput[0].split("\n")
    finalText = ""
    cc = 0
    for i in finalResp:
        if i == '':
            continue
        if cc == 1:
            finalText += i + " "
        if "### Response:" in i:
            cc = 1
    
    finalText = finalText.strip()
    finalText = finalText.replace("<|end_of_text|>", "")
    print("*"*50)
    print(finalText)
    print("*"*50)

    return jsonify({"response": finalText})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
