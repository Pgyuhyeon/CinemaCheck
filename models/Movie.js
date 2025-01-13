const mongoose = require('mongoose');

// 영화 스키마 정의
const movieSchema = new mongoose.Schema({
  title: { type: String, required: true },
  director: { type: String, required: true },
  releaseDate: { type: Date },
  genre: { type: String },
  createdAt: { type: Date, default: Date.now },
});

// Movie 모델 생성
const Movie = mongoose.model('Movie', movieSchema);

module.exports = Movie; // 외부에서 사용 가능하도록 내보내기
