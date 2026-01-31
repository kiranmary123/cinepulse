**🎬 CinemaPulse — Real-time Customer Feedback Analysis**
CinemaPulse is a web-based application that allows users to submit movie and theatre feedback with star ratings, while enabling admins to view and analyze customer responses in real time. The system supports both local mode (in-memory storage) and AWS cloud integration using DynamoDB and SNS.

**✨ Features**

**👤 User Features**

Simple user login

Submit movie feedback with:

Movie selection

Theatre selection

Interactive star rating ⭐

Text feedback


**🛠 Admin Features**

Secure admin login

View all user feedbacks in a dashboard

Monitor movie ratings and comments


**☁️Cloud Features(AWS Version)**

Stores users and feedback in Amazon DynamoDB

Sends login notifications using Amazon SNS


**🧰 Tech Stack**

Frontend: HTML, CSS, JavaScript

Backend: Python (Flask)

Cloud Services: AWS DynamoDB, AWS SNS

Styling: Custom CSS


**📂 Project Structure**

CinemaPulse/
│
├── static/
│   ├── style.css        
│   └── js.script        
│
├── templates/
│   ├── index.html       
│   ├── dashboard.html   
│   ├── feedback.html    
│   ├── admin_login.html 
│   └── admin_dashboard.html
│
├── app.py               
├── app_aws.py          
├── requirements.txt
└── README.md
