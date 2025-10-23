# app/service/survey_stats_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..database.models.surveys import Surveys
from ..database.models.survey_question import SurveyQuestion, QuestionType
from ..database.models.responses import Response
from ..database.models.response_detail import ResponseDetail
from collections import defaultdict
from typing import Dict, List, Any


class SurveyStatsService:

    # 총합 데이터 통계 결과 조회
    @staticmethod
    async def get_complete_survey_stats(db: AsyncSession, survey_id: int) -> Dict[str, Any]: # 따로 스키마를 생성하지 않았기 때문에 Dict형태로 반환
        # 특정 survey_id 설문지와 모든 관련 데이터를 한 번에 조회
        query = (select(Surveys)
                 .options(
            selectinload(Surveys.questions)
                    .selectinload(SurveyQuestion.options),selectinload(Surveys.responses)
                    .selectinload(Response.details),selectinload(Surveys.email_logs)
                )
                .where(Surveys.survey_id == survey_id))

        result = await db.execute(query)
        survey = result.scalar_one_or_none()

        if not survey: # 설문지가 없다면
            raise ValueError(f"설문지를 찾을 수 없습니다: survey_id={survey_id}")

        # 전체 통계 계산
        distributed_count = len(survey.email_logs)  # 배포 수
        response_count = len(survey.responses)  # 응답 수
        completion_rate = (response_count / distributed_count * 100) if distributed_count > 0 else 0 # 응답 완료율

        # 질문 타입별 개수
        single_choice_count = sum(1 for q in survey.questions if q.question_type == QuestionType.single_choice) # 객관식 질문 수
        short_text_count = sum(1 for q in survey.questions if q.question_type == QuestionType.short_text) # 주관식 질문 수

        overall_stats = { # 통합 데이터 모음
            "survey_id": survey.survey_id,
            "survey_title": survey.title, # 설문지 제목
            "survey_description": survey.description, # 설문지 설명
            "distributed_count": distributed_count, # 이메일로 발송된 횟수
            "response_count": response_count, # 응답 수
            "completion_rate": round(completion_rate, 2), # 응담 완료율 - 소수점 2자리 까지 표현
            "total_questions": len(survey.questions), # 총 질문 개수
            "single_choice_count": single_choice_count, # 선택지 타입 질문 개수
            "short_text_count": short_text_count, # 텍스트 타입 질문 개수
            "created_at": survey.created_at.isoformat() if survey.created_at else None, # 설문 생성일
            "expire_at": survey.expire_at.isoformat() if survey.expire_at else None, # 설문 마감일
            "is_public": survey.is_public # 설문지 공개 여부
        }

        # 질문별 통계 계산
        single_choice_questions = []
        short_text_questions = []

        for question in survey.questions:
            if question.question_type == QuestionType.single_choice: # 객관식(선택지) 통계
                stats = SurveyStatsService._calculate_single_choice_stats(question, survey.responses, response_count)
                single_choice_questions.append(stats)

            elif question.question_type == QuestionType.short_text: # 주관식(단답형) 통계
                stats = SurveyStatsService._calculate_short_text_stats(question, survey.responses, response_count)
                short_text_questions.append(stats)

        # 모든 통계 데이터를 하나의 응답으로 반환
        return {
            "overall": overall_stats,
            "single_choice_questions": single_choice_questions, # 객관식 관련 데이터 모음
            "short_text_questions": short_text_questions # 주관식 관련 데이터 모음
        }

    # 객관식 응답 결과 계산
    @staticmethod
    def _calculate_single_choice_stats(question: SurveyQuestion, responses: List[Response], total_responses: int) -> Dict[str, Any]: # 따로 스키마를 생성하지 않았기 때문에 Dict형태로 반환
        # 각 선택지별 선택 횟수 계산
        option_counts = defaultdict(int)
        question_respondents = set()  # 이 질문에 응답한 사람들

        for response in responses: # 여러개의 응답지들을 순회하면서
            for detail in response.details: # 그 중 응답 결과지를 순회
                if detail.question_id == question.question_id and detail.selected_option_id: # 각 응답들의 타입이 맞다면 개수 + 1
                    option_counts[detail.selected_option_id] += 1
                    question_respondents.add(response.id)

        question_response_count = len(question_respondents)

        # 이 질문에 대한 응답 율 계산 => ((해당 질문 응답 개수/총 질문 개수) * 100) - 필수가 아닌 질문이 있기 때문에 응답율을 계산
        response_rate = (question_response_count / total_responses * 100) if total_responses > 0 else 0

        # 특정 질문 안에서 각 선택지에 대한 통계
        options_data = [] # 선택지 별 데이터를 담기 위한 배열 선언
        for option in question.options:
            count = option_counts.get(option.option_id, 0)
            # 이 질문에 응답한 데이터 중에서 특정 선택지의 비율 계산
            percentage = (count / question_response_count * 100) if question_response_count > 0 else 0

            options_data.append({
                "option_id": option.option_id,
                "option_text": option.option_text,
                "count": count,
                "percentage": round(percentage, 2)
            })

        return {
            "question_id": question.question_id,
            "question_text": question.question_text,
            "question_type": "single_choice",
            "total_responses": question_response_count,
            "response_rate": round(response_rate, 2),
            "options": options_data
        }

    # 주관식 응답 결과 계산
    @staticmethod
    def _calculate_short_text_stats(question: SurveyQuestion, responses: List[Response], total_responses: int) -> Dict[str, Any]: # 따로 스키마를 생성하지 않았기 때문에 Dict형태로 반환
        text_responses = []

        for response in responses:
            for detail in response.details:
                if (detail.question_id == question.question_id and
                        detail.text_response and
                        detail.text_response.strip()):
                    text_responses.append(detail.text_response)

        question_response_count = len(text_responses)

        # 응답률
        response_rate = (question_response_count / total_responses * 100) if total_responses > 0 else 0

        return {
            "question_id": question.question_id,
            "question_text": question.question_text,
            "question_type": "short_text",
            "total_responses": question_response_count,
            "response_rate": round(response_rate, 2),
            "sample_responses": text_responses[:5]  # 샘플 5개만
        }