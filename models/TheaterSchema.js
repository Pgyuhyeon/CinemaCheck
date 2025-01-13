const mongoose = require('mongoose');

const TheaterSchema = new mongoose.Schema({
  theaterCode: String, // 영화관 고유 코드
  name: String,        // 영화관 이름
  chain: String,       // 체인명 (CGV, 메가박스, 롯데시네마)
  address: String,     // 주소
  latitude: Number,    // 위도
  longitude: Number,   // 경도
  placeUrl: String,    // 카카오맵 URL
  officialUrl: String, // 상영시간표 URL
});

const Theater = mongoose.model('Theater', TheaterSchema);
module.exports = Theater;
