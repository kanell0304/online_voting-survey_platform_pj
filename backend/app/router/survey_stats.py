from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from ..database.database import get_db
from ..service.survey_stats_service import SurveyStatsService
from ..database.models.responses import Response
from ..database.models.response_detail import ResponseDetail

router = APIRouter(prefix="/survey_stats", tags=["Survey Stats"])

# 특정 설문지 결과에 대한 통합 데이터 조회(선택지, 텍스트 질문 결과 포함) - 이 api에 텍스트도 포함
@router.get("/{survey_id}/complete")
async def get_complete_survey_stats(survey_id: int, db: AsyncSession = Depends(get_db)):
    try:
        stats = await SurveyStatsService.get_complete_survey_stats(db, survey_id)
        return {"success": True, "data": stats}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")


# 특정 설문지 결과에 대한 '텍스트' 데이터만 조회 - 일단 만들긴 했는데 텍스트는 따로 통계데이터로 활용하기 힘들거 같아 위의 api를 사용하시면 될거같음
# 용도: 특정 텍스트 응답타입의 질문에 응답 결과들을 보고 싶을떄 사용
# ex) 질문: 여기에 올때 어떤 방식으로 왔나요?
# - question_id:1, text: 버스를 타고 왔습니다.
# - question_id:2, text: 자가용를 타고 왔습니다.
# - question_id:3, text: 지하철를 타고 왔습니다.
@router.get("/{survey_id}/questions/{question_id}/text-responses")
async def get_all_text_responses(survey_id: int, question_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ResponseDetail.id, ResponseDetail.text_response, Response.submitted_at)
        .join(Response, Response.id == ResponseDetail.response_id)
        .where(and_(Response.survey_id == survey_id, ResponseDetail.question_id == question_id, ResponseDetail.text_response.isnot(None), ResponseDetail.text_response != '')) # 응답 텍스트가 없으면 ''(빈칸)
        .order_by(Response.submitted_at.desc())
    )

    responses = result.all()

    # 총 응답 개수 조회
    count_result = await db.execute(
        select(func.count(ResponseDetail.id)) # 응답 결과 테이블에서 총 질문 개수를 조회해옴
        .join(Response, Response.id == ResponseDetail.response_id)
        .where(and_(Response.survey_id == survey_id,ResponseDetail.question_id == question_id,ResponseDetail.text_response.isnot(None),ResponseDetail.text_response != ''))
    )

    total_count = count_result.scalar() # 특정 설문지의 총 응답 개수를 저장

    return {
        "success": True, # 응답 성공 여부
        "data": {
            "survey_id": survey_id, # 설문지 id
            "question_id": question_id, # 질문 id
            "total": total_count,
            "responses": [
                {
                    "id": r.id,
                    "text": r.text_response, # 응답 결과(텍스트) ex) 따로 추가적인 피드백은 없습니다.
                    "submitted_at": r.submitted_at.isoformat() if r.submitted_at else None # 응답 시간
                }
                for r in responses
            ]
        }
    }