const express = require('express');
const fetchShowtimes = require('../utils/fetchShowtimes'); // Python 실행 함수
const Showtimes = require('../models/Showtimes'); // MongoDB 스키마

const router = express.Router();

// 상영시간표 요청 처리
router.get('/:theaterCode', async (req, res) => {
  const { theaterCode } = req.params;

  try {
    // Python 스크립트 실행 (크롤링)
    const showtimesData = await fetchShowtimes(theaterCode);
    // MongoDB에 저장 또는 업데이트
    await Showtimes.findOneAndUpdate(
      { theaterCode }, // 조건: 특정 영화관 코드
      { $set: { showtimes: showtimesData, updatedAt: Date.now() } }, // 저장 또는 업데이트할 데이터
      { upsert: true } // 데이터가 없으면 새로 생성
    );

    // 저장된 데이터를 반환
    res.status(200).json(showtimesData);
  } catch (error) {
    console.error('오류 발생:', error);
    res.status(500).json({ error: '상영시간표를 가져오는 데 실패했습니다.' });
  }
});

module.exports = router;
