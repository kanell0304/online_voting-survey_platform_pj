import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MdOutlineDeleteForever } from "react-icons/md";

export default function MySurveysPage() {

  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [mySurveys, setMySurveys] = useState([]);
  const [isDeleteModal, setIsDeleteModal] = useState(false);
  const [selectSurveyId, setSelectSurveyId] = useState(null);

useEffect(()=>{
    const token = document.cookie.split("; ").find(x => x.startsWith("access_token") == 0);
    console.log(token)
    if(token){
      (async () => {
        try{
          setIsLoggedIn(true);
          const res = await axios.get(`http://localhost:8081/users/userme`, {withCredentials: true});
          const res_mySurveys = await axios.get(`http://localhost:8081/surveys`, {withCredentials: true});
          setMySurveys(res_mySurveys.data)
        } catch(err){
          console.error("정보 가져오기 실패:", err)
        }
      })();
    }
    else{
        setIsLoggedIn(false);
    }
  }, [])

  const handleCreateClick = () => {
    navigate("/create");
  }

  const handleResultClick = (survey_id) => {
    navigate(`/survey-result/${survey_id}`);
  }

  const handlePostClick = (survey_id) => {
    navigate(`/distribute/${survey_id}`);
  }

  const handleEditClick = (survey_id) => {
    navigate(`/edit/${survey_id}`);
  }

  const handleDeleteClick = (survey_id) => {
    setIsDeleteModal(true);
    setSelectSurveyId(survey_id);
  }

  const handleDeleteConfirmClick = async() => {
    console.log(`selectSurveyId: ${selectSurveyId}`)
    try{
      const res = await axios.delete(`http://localhost:8081/surveys/${selectSurveyId}`, {withCredentials: true});
      setMySurveys(prevSurveys => prevSurveys.filter(survey => survey.survey_id !== selectSurveyId));
      alert("설문지가 삭제되었습니다.");
      setIsDeleteModal(false);
    } catch(err){
      console.error("정보 가져오기 실패:", err)
    }
  }

  const handleDeleteCancleClick =() => {
    setIsDeleteModal(false);
  }

  const [sortType, setSortType] = useState("created_at");

  const toggle =()=>{
    setSortType(type=>{
      if(type === "created_at") return "title";
      else if(type === "title") return "expire_at";
      return "created_at";
    });
  };

  const sortedSurveys = [...mySurveys].sort((a, b)=>{
    if(sortType == "title") return a.title.localeCompare(b.title, 'ko');
    else if(sortType === "expire_at") return new Date(a.expire_at) - new Date(b.expire_at);
    return new Date(a.created_at) - new Date(b.created_at);
  });


  return (
    <div className="min-h-screen bg-neutral-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">My Surveys</h1>
          <p className="text-gray-600">지금까지 만든 설문 목록입니다.</p>
          {/* css toggle 부분 도와주세요ㅠㅠㅠ */}
          <button onClick={toggle} className='text-gray-600'>{(sortType === "created_at") ? "정렬: 생성일순" : (sortType === "title") ? "정렬: 가나다순" : "정렬: 마감일순"}</button>
          <button onClick={handleCreateClick} className="px-3 py-1 ml-184 text-sm text-white bg-gray-600 rounded-md hover:bg-gray-700">설문지 작성하기</button>
        </div>

        {/* 설문 목록을 그리드 형태로 표시 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sortedSurveys.length === 0 ? (
            <p className="text-gray-500 col-span-full text-center py-8">아직 작성된 설문지가 없습니다.</p>
            ):(
          sortedSurveys.map(survey => {
            const days = 3
            const expireDate = (new Date(survey.expire_at) - new Date()) <= days * 86400000 //시,분,초,밀리초 곱한값
            const dDay = Math.ceil((new Date(survey.expire_at) - new Date()) / 86400000)

            return (
            <div key={survey.survey_id} className={`p-4 bg-white border rounded-lg shadow ${expireDate?'border-red-600' : 'border'}`}>
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold mb-2">{survey.title}</h3>
                <button onClick={() => handleDeleteClick(survey.survey_id)} className="px-3 py-1 rounded-md hover:bg-gray-300"><MdOutlineDeleteForever /></button>
              </div>
              <div className="text-sm mb-4">
                <span className="text-gray-500">생성일: {survey.created_at.split('T')[0]}</span><br/>
                <span className={expireDate ? 'text-red-400' : 'text-gray-500'}>마감일: {survey.expire_at.split('T')[0]} {dDay>0 ? `(D-${dDay})`:'(마감)'}</span>
              </div>
              <div className="flex justify-end space-x-2">
                <button onClick={() => handleResultClick(survey.survey_id)} className="px-3 py-1 text-sm text-white bg-gray-600 rounded-md hover:bg-gray-700">
                  결과
                </button>
                <button onClick={() => handlePostClick(survey.survey_id)} className="px-3 py-1 text-sm text-white bg-blue-500 rounded-md hover:bg-blue-600">
                  배포
                </button>
                <button onClick={() => handleEditClick(survey.survey_id)} className="px-3 py-1 text-sm text-white bg-blue-500 rounded-md hover:bg-blue-600">
                  수정
                </button>
              </div>
            </div>
          )}))}
        </div>
        <div>
        {isDeleteModal && (
          <div className="fixed inset-0 bg-black/20 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full mx-4">
              <h2 className="text-xl font-bold mb-4 text-gray-800">삭제 확인</h2>
              <p className="text-gray-600 mb-6">해당 설문지을 정말 삭제하시겠습니까?<br />삭제된 설문지 데이터는 복구할 수 없습니다.</p>
              <div className="flex justify-end space-x-3">
                <button onClick={() => handleDeleteConfirmClick()} className="px-4 py-2 text-sm text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors">삭제</button>
                <button onClick={() => handleDeleteCancleClick()} className="px-4 py-2 text-sm text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors">취소</button>
              </div>
            </div>
          </div>
        )}
        </div>
      </div>
    </div>
  );
}