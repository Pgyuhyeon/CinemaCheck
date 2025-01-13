const express = require('express');
const router = express.Router();
const movieController = require('../controllers/movieControllers'); // 컨트롤러 불러오기

// GET /movies - 모든 영화 조회
router.get('/', movieController.getMovies);

// POST /movies - 영화 추가
router.post('/', movieController.addMovie);

module.exports = router; // 라우터 내보내기
