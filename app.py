from flask import Flask, request, jsonify, abort, render_template_string, redirect
import time
import random
import string
import threading

app = Flask(__name__)

# Store generated values with timestamps
generated_values = {}
user_tasks = {}

def generate_or_validate_token(token=None):
    current_time = time.time()
    validity_duration = 10 * 60  # 10 minutes in seconds

    # Cleanup expired tokens
    expired_tokens = [key for key, timestamp in generated_values.items() if current_time - timestamp > validity_duration]
    for key in expired_tokens:
        del generated_values[key]

    if token is None:
        # Generate a new token
        new_token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        generated_values[new_token] = current_time
        return new_token
    else:
        # Validate an existing token
        if token in generated_values and current_time - generated_values[token] <= validity_duration:
            return True
        else:
            return False

def generate_response_html(success=True):
    if success:
        return render_template_string('''
            <html>
            <head>
                <style>
                    body { text-align: center; padding: 50px; }
                    .overlay { font-size: 24px; color: green; }
                    .button { padding: 10px 20px; background-color: green; color: white; text-decoration: none; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="overlay">Success! Now you can use our bot.</div>
                <a href="https://t.me/+AjTismixDR80MDE1" class="button">Click here to go to our bot</a>
                <script>
                    setTimeout(function() {
                        window.location.href = "https://t.me/Tata_Play_Ripping_Group";
                    }, 5000);
                </script>
            </body>
            </html>
        ''')
    else:
        return render_template_string('''
            <html>
            <head>
                <style>
                    body { text-align: center; padding: 50px; }
                    .overlay { font-size: 24px; color: red; }
                    .button { padding: 10px 20px; background-color: red; color: white; text-decoration: none; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="overlay">Invalid request!</div>
                <a href="https://t.me/Tata_Play_Ripping_Group" class="button">Try again</a>
                <script>
                    setTimeout(function() {
                        window.location.href = "https://t.me/Tata_Play_Ripping_Group";
                    }, 5000);
                </script>
            </body>
            </html>
        ''')

@app.route('/@aryanchy/id', methods=['GET'])
def get_random_token():
    return jsonify(generate_or_validate_token())

@app.route('/<token>/user/<userid>', methods=['GET'])
def validate_user_and_add_task(token, userid):
    ref = request.headers.get("Referer")
    if 2<3:#ref == "https://atglinks.com/" and generate_or_validate_token(token):
        if userid not in user_tasks:
            user_tasks[userid] = {'tasks': 20}  
    return generate_response_html(success=True), 200
 #   else:
      #  return generate_response_html(success=False), 403

@app.route('/<token>/task/<userid>', methods=['GET'])
def add_task_to_user(token, userid):
    ref = request.headers.get("Referer")
    if 2<3:# ref == "https://atglinks.com/" and generate_or_validate_token(token):
        if userid in user_tasks:
            user_tasks[userid]['tasks'] += 10
        else:
            user_tasks[userid] = {'tasks': 10}
    return generate_response_html(success=True), 200
  #  else:
 #       return generate_response_html(success=False), 403

@app.route('/<token>/taskuse/<userid>', methods=['GET'])
def decrement_task_from_user(token, userid):
    if generate_or_validate_token(token):
        if userid in user_tasks and user_tasks[userid]['tasks'] > 0:
            user_tasks[userid]['tasks'] -= 1
            return jsonify(user_tasks), 200
        else:
            return jsonify({"error": "User not found or no tasks left"}), 404
    else:
        abort(403)

@app.route('/lst', methods=['GET'])
def list_users_with_tasks():
    return jsonify(user_tasks), 200

def reset_generated_values():
    while True:
        time.sleep(24 * 60 * 60)  # Wait for 24 hours
        generated_values.clear()  # Reset the generated values

# Start the reset thread
reset_thread = threading.Thread(target=reset_generated_values, daemon=True)
reset_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
