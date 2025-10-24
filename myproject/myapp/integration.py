import requests
import json
from myproject import settings
from .models import Result, User
from openai import OpenAI
client = OpenAI(api_key=settings.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
# البرومت النهائي مع تعليمات واضحة + هيكل JSON
PROMPT_TEMPLATE = """
You are an AI career advisor analyzing IT graduates' data.

Instructions:
- Use the quiz answers or CV summary provided below.
- Return ONLY a valid JSON object in the following format.
- Do not include any extra explanation or text outside the JSON.

JSON structure to return:
{{
  "career_recommendation": "",
  "confidence_level": 0.0,
  "key_strengths": [],
  "personality_traits": [],
  "reasoning": "",
  "recommended_skills_to_learn": [],
  "growth_opportunities": ""
}}

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

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def analyze_user_data(user_id, quiz_data=None, cv_summary=""):
   

    user = User.objects.get(id=user_id)

    # تجهيز الـ prompt مع البيانات
    prompt_text = PROMPT_TEMPLATE.format(
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

    # headers = {
    #     "Authorization": f"Bearer {settings.GEMINI_API_KEY}",  
    #     "Content-Type": "application/json"
    # }

    # payload = {
    #     "model": "google/gemini-2.0-flash-exp:free",
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": [
    #                         {"type": "text", "text": prompt_text}
    #                         ]

    #         }
    #     ]
    # }

    try:
        
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an AI career advisor analyzing IT graduates' quiz answers and CV. "
                        "Return ONLY valid JSON as described."},
            {"role": "user", "content": prompt_text},
            ],
            stream=False
            )
        
        ai_output = response.choices[0].message.content
        print("AI Output:", ai_output)

        if not ai_output:
            raise ValueError("Empty AI response")

        # استخراج JSON فقط من النص
        start = ai_output.find("{")
        end = ai_output.rfind("}") + 1
        if start == -1 or end == -1:
            raise ValueError("No JSON found in AI response")

        ai_result = json.loads(ai_output[start:end])

        # تخزين النتيجة في قاعدة البيانات
        result = Result.objects.create(
        user=user,
        career_recommendation=ai_result.get("career_recommendation", "No recommendation found"),
        reasoning=ai_result.get("reasoning", ""),
        recommended_skills_to_learn=", ".join(ai_result.get("recommended_skills_to_learn", [])),
        confidence_level=ai_result.get("confidence_level", None),
        key_strengths=", ".join(ai_result.get("key_strengths", [])),
        personality_traits=", ".join(ai_result.get("personality_traits", [])),
        growth_opportunities=ai_result.get("growth_opportunities", ""),
        )

        return result

    except (ValueError, json.JSONDecodeError, Exception) as e:
        print("AI Integration Error:", e)
        return Result.objects.create(
            user=user,
            result="Analysis Error",
            description=str(e),
            recomindation="",
        )