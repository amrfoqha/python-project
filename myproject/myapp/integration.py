import requests , json
from django.conf import settings
from .models import Result, User
from .prompt_template import PROMPT_TEMPLATE

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def analyze_user_data(user_id, quiz_data, cv_summary=""):
    user = User.objects.get(id=user_id)

    prompt = PROMPT_TEMPLATE.format(
        user_background=quiz_data.get("background", ""),
        user_field_interest=quiz_data.get("interest", ""),
        user_favorite_project=quiz_data.get("project", ""),
        user_technical_skills=quiz_data.get("skills", ""),
        user_experience=quiz_data.get("experience", ""),
        user_career_goals=quiz_data.get("goals", ""),
        user_work_preference=quiz_data.get("work_type", ""),
        user_industry_awareness=quiz_data.get("awareness", ""),
        user_soft_skills=quiz_data.get("soft_skills", ""),
        user_cv_summary=cv_summary,
    )

    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "system", "content": """
You are an AI career advisor analyzing IT graduates' data.

If the user answered quiz questions, use their answers.
If only a CV is provided, extract skills, experience, and projects from it.
If both exist, combine all data for the best result.

Analyze the input and return a structured JSON with:
{
  "career_recommendation": "",
  "confidence_level": 0.0,
  "key_strengths": [],
  "personality_traits": [],
  "reasoning": "",
  "recommended_skills_to_learn": [],
  "growth_opportunities": ""
}

User Answers:
{user_background}
{user_field_interest}
{user_favorite_project}
{user_technical_skills}
{user_experience}
{user_career_goals}
{user_work_preference}
{user_industry_awareness}
{user_soft_skills}

User CV Summary:
{user_cv_summary}
"""
},
            ],
        "temperature": 0.7
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
    data = response.json()
    ai_output = data['choices'][0]['message']['content']
    ai_result = json.loads(ai_output)

    result = Result.objects.create(
        user=user,
        result=ai_result.get("career_recommendation", ""),
        description=ai_result.get("reasoning", ""),
        recomindation=", ".join(ai_result.get("recommended_skills_to_learn", []))
    )

    return result
