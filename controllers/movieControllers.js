const Movie = require('../models/Movie'); // Movie 모델 불러오기

// 모든 영화 조회
exports.getMovies = async (req, res) => {
  try {
    const movies = await Movie.find(); // MongoDB에서 모든 영화 조회
    res.json(movies);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

// 영화 추가
exports.addMovie = async (req, res) => {
  try {
    const movie = new Movie(req.body); // 요청 데이터를 기반으로 새 영화 생성
    const savedMovie = await movie.save(); // MongoDB에 저장
    res.status(201).json(savedMovie); // 저장된 영화 반환
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
};
