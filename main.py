import requests
import json

def get_final_thought(query, api_key, url):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "inputs": {},
        "query": query,
        "response_mode": "streaming",
        "user": "abc-123",
        "files": []
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    final_thought = None

    if response.status_code == 200:
        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data:'):
                        json_str = decoded_line[5:]  # Remove 'data: ' prefix
                        json_data = json.loads(json_str)
                        if json_data.get('event') == 'agent_thought':
                            final_thought = json_data.get('thought')
        except Exception as e:
            print(f'Error processing streamed data for query "{query}": {e}')
    else:
        print(f'Failed to send data for query "{query}": {response.text}')

    return final_thought

# Your API key and endpoint
api_key = 'API Key'
url = 'https://app.genai4all.org/v1/chat-messages'

input_file_path = 'input.txt'  # Path to the file containing the queries
output_file_path = 'output.txt'  # Path to the file where you want to save the answers

with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
    for line in input_file:
        query = line.strip()
        if query:  # Check if the line is not empty
            answer = get_final_thought(query, api_key, url)
            output_file.write(f"Query: {query}\n")
            if answer:
                output_file.write(f"Answer: {answer}\n")
            else:
                output_file.write("Answer: No answer received\n")
            output_file.write("\n")  # Add a blank line between each Q&A pair

print(f"Process completed. Check the answers in '{output_file_path}'.")
