# 💬 Chat Tracker - WhatsApp Chat Analyzer

Chat Tracker is an intelligent and interactive web application designed to analyze and summarize exported WhatsApp chat files. Whether it’s a one-on-one conversation or a group chat, Chat Tracker reveals fascinating insights into your conversations with a clean, user-friendly interface built using Streamlit.

Check Out The Application [visit here !](https://whatsapp-insights.streamlit.app/)

## 🌟 Features
### 📌 Comprehensive Chat Analysis
- **Total Messages:** See the overall message count in individual or group chats.
- **Media & Links Shared:** Track how many images, videos, and links were exchanged.
- **Deleted Messages:** Detect how many messages were deleted in the conversation.
### 👥 User-Specific Insights (Group Chats)
- **Most Active User:** Find out who dominates the conversation.
- **Least Active User:** Identify silent participants.
- **User-wise Stats:** Breakdown of messages, media, links, and deleted messages per user.
### 📅 Timeline & Activity Trends
- **Hourly Activity:** Check which time of the day the chat is most active.
- **Daily & Weekly Trends:** Analyze chat patterns over weekdays and weekends.
- **Monthly Breakdown:** Observe how messaging frequency changes month-wise.
### 😃 Emoji & Text Analysis
- Top Emojis Used: Discover the most frequently used emojis in the chat.
- Most Common Words: See which words dominate the conversation.
- Sentiment Trends (Future Scope): Get a glimpse of the emotional tone of chats.
### 📂 Easy Upload & Processing
- Simply export your WhatsApp chat (without media) and upload it to Chat Tracker.
- Instant analysis with interactive charts and visualizations.

## 🚀 How to Use?
Step 1: Export Your WhatsApp Chat
Open the WhatsApp chat (individual or group) you want to analyze.
Click on Export Chat (without media).
Save the .txt file.

## 📋 Installation Instructions

To get started with this project, follow the instructions below to set up the environment and install the necessary dependencies.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Shabeenabd/DriveWorthAI-CarPricePredictor.git
cd DriveWorthAI-CarPricePredictor
```
### Step 2: Set Up Python Environment
1. Create a virtual environment:
```bash
python3 -m venv venv
```
2. Activate the virtual environment:
```bash
# For Windows
venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate

```
3. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Project Structure

```bash
ChatTrackr/
│
├── app                                            # Web Application 
│    ├── app.py                                    
│    ├── helper.py                                 # helper functions for the streamlit application
│    └── requirements.txt                          # Dependencies for Web Application 
│   
├── data                                           # whatsapp exported chats
│     ├── whatsappchat_1.zip                               
│     └── whatsappchat_2.zip                               
│  
├── src                                         
│     └── chat analyzer.ipynb                      # Jupyter notebook for preprocessing and visualization
│
├── requirements.txt                               # Project Dependencies
│
└── README.md                                      # This README file
```
