from flask import Flask, request, jsonify
import requests
import re
import os

# Developed & Powered By MATRIX (@V7R7X)

# Request Example : http://yourdomain/api?apikey=djsvidkgo489fjsoak&link=<instagram_link>.

app = Flask(__name__)

# Predefined API key
API_KEY = 'YuvrajmodzV3-57107'

@app.route('/api', methods=['GET'])
def get_instagram_title():
    # Get the API key and link from the request parameters
    api_key = request.args.get('apikey')
    link = request.args.get('link')

    # Validate API key
    if api_key != API_KEY:
        return jsonify({'error': 'API key is invalid.'}), 403

    # Validate if the link is an Instagram URL
    if link and 'instagram.com' in link:
        try:
            # Send a GET request to the Instagram link
            response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
            
            # Check if the request was successful
            if response.status_code == 200:
                html = response.text
                
                # Use regex to extract the <title> tag content
                match = re.search(r'<title>(.*?)<\/title>', html)
                
                # Check if the title was found
                if match:
                    title = match.group(1).strip()  # Get the title and remove extra spaces
                    
                    # Extract name and username
                    cleaned_title = re.sub(r' \u2022.*$', '', title)  # Remove everything after "•"
                    cleaned_title = cleaned_title.replace('&#064;', '@')  # Replace HTML entity with @
                    
                    # Split name and username
                    name, username = cleaned_title.split(' (', 1)
                    username = username.strip(')')  # Remove the closing parenthesis
                    
                    return jsonify({'name': name, 'username': username})
                else:
                    return jsonify({'error': 'Title not found.'}), 404
            else:
                return jsonify({'error': 'Unable to retrieve the page.'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid Instagram link.'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port, debug=True)
