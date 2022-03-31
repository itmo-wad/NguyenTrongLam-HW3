- Create a flask app which connects to MongoDB and runs at ‘http://localhost:5000’
- User can sign up at ‘/signup’
- Login page at ‘/auth’ .If success, return a secret page to user. If not, give user a flash message about the error.
- Store username, password in database
- Form to upload image at ‘/upload’
- Save uploaded image to folder ‘upload’ on server side, allow only specified extensions
  
Deploy:
- virutalenv -p python3 venv 
- source venv/bin/activate
- pip3 install -r requirements.txt
- python3 app.py 
