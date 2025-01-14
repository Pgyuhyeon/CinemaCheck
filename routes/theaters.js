const express = require('express');
const router = express.Router();
const axios = require('axios');
const mongoose = require('mongoose');

// Haversine Formula: 두 지점 간의 거리 계산
const calculateDistance = (lat1, lon1, lat2, lon2) => {
  const toRadians = (degree) => (degree * Math.PI) / 180;

  const R = 6371; // 지구 반지름 (단위: km)
  const dLat = toRadians(lat2 - lat1);
  const dLon = toRadians(lon2 - lon1);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRadians(lat1)) *
      Math.cos(toRadians(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c; // 거리 반환 (단위: km)
};

// 카카오 API로 영화관 검색 함수
const searchTheaters = async (latitude, longitude) => {
  const kakaoApiUrl = 'https://dapi.kakao.com/v2/local/search/category.json';
  const headers = {
    Authorization: `KakaoAK c81b20db6a96b199e2fe6b8f1ea1cbed`, // 카카오 REST API 키
  };

  const params = {
    category_group_code: 'CT1', // 영화관 카테고리 코드
    x: longitude, // 경도
    y: latitude, // 위도
    radius: 5000, // 반경 5km
    size: 15, // 한 번에 가져올 결과 수
    sort: 'distance', // 거리순 정렬
  };

  let theaters = [];
  let page = 1;
  const maxPages = 45; // 카카오 API 최대 페이지 제한

  try {
    while (page <= maxPages) {
      const response = await axios.get(kakaoApiUrl, {
        headers,
        params: { ...params, page },
      });

      if (response.status !== 200) {
        console.error(`Error: ${response.status} - ${response.statusText}`);
        break;
      }

      const data = response.data.documents;
      theaters = [...theaters, ...data];

      // 다음 페이지가 없는 경우 종료
      if (data.length < params.size) break;

      page += 1;
    }
  } catch (error) {
    console.error('Error fetching theaters:', error.message);
  }

  // CGV, 롯데시네마, 메가박스만 필터링
  return theaters.filter((theater) =>
    ['CGV', '롯데시네마', '메가박스'].some((brand) => theater.place_name.includes(brand))
  );
};

// MongoDB에서 영화 상영 정보 검색 및 거리 계산 추가
const fetchMoviesFromDBWithDistance = async (movieName, theaters, userLatitude, userLongitude, date) => {
  const movieSchedules = [];

  for (const theater of theaters) {
    const theaterName = theater.place_name.replace(/\s+/g, ''); // 띄어쓰기 제거
    const theaterDb = mongoose.connection.useDb(theaterName); // 데이터베이스 이름
    const collection = theaterDb.collection('Movies'); // Movies 컬렉션

    try {
      const query = date ? { MovieName: movieName, Date: date } : { MovieName: movieName };
      const movies = await collection.find(query).toArray();
      if (movies.length > 0) {
        const distance = calculateDistance(
          userLatitude,
          userLongitude,
          parseFloat(theater.y), // 카카오 API에서 가져온 위도
          parseFloat(theater.x) // 카카오 API에서 가져온 경도
        );

        movieSchedules.push({
          theaterName: theater.place_name, // 원래 이름 유지
          schedules: movies.map((movie) => ({
            CinemaName: movie.CinemaName,
            MovieName: movie.MovieName,
            StartTime: movie.StartTime,
            ScreenName: movie.ScreenName,
            BookingSeatCount: movie.BookingSeatCount,
            TotalSeatCount: movie.TotalSeatCount,
            Date: movie.Date,
            Distance: `${distance.toFixed(2)} km`,
          })),
        });
      }
    } catch (error) {
      console.error(`Error fetching data for theater ${theaterName}:`, error.message);
    }
  }

  return movieSchedules;
};

// API 엔드포인트
router.get('/', async (req, res) => {
  try {
    const { latitude, longitude, movieName, date } = req.query;

    if (!latitude || !longitude || !movieName) {
      return res.status(400).json({ error: 'latitude, longitude, and movieName are required' });
    }

    const userLatitude = parseFloat(latitude);
    const userLongitude = parseFloat(longitude);

    // 카카오 API로 근처 영화관 검색
    const theaters = await searchTheaters(userLatitude, userLongitude);

    // MongoDB에서 영화 상영 정보 가져오기 + 거리 추가
    const movieSchedules = await fetchMoviesFromDBWithDistance(movieName, theaters, userLatitude, userLongitude, date);

    // 응답 반환
    res.json({
      message: 'Movie schedules retrieved successfully',
      movieSchedules,
    });
  } catch (error) {
    console.error('Error in API:', error.message);
    res.status(500).json({ error: 'An error occurred while fetching theaters or movies' });
  }
});

module.exports = router;
