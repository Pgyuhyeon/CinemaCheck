const mongoose = require('mongoose');

// 상영시간표 스키마 정의
const ShowtimesSchema = new mongoose.Schema({
  theaterCode: { type: String, required: true }, // 영화관 코드 (고유 식별자)
  showtimes: [
    {
      movieTitle: String,  // 영화 제목
      time: String,        // 상영 시간
      seats: String        // 잔여 좌석 정보
    }
  ],
  updatedAt: { type: Date, default: Date.now } // 데이터 최신화 시간
});

// 모델 생성
const Showtimes = mongoose.model('Showtimes', ShowtimesSchema);

module.exports = Showtimes;
