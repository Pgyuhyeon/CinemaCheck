var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');

const mongoose = require('mongoose');





// MongoDB 연결 설정
const mongoURI = 'mongodb://localhost:27017/movieDatabase';
mongoose
  .connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('MongoDB 연결 성공'))
  .catch(err => console.error('MongoDB 연결 실패: ', err));



var app = express(); // Express 앱 초기화


// 라우트 파일 불러오기
var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var movieRoutes = require('./routes/movies'); // "/movies" 라우트를 처리하는 파일
const showtimesRoutes = require('./routes/showtimes');

// 뷰 엔진 설정
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

// 미들웨어 설정
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// 라우트 설정
app.use('/', indexRouter);
app.use('/users', usersRouter);
app.use('/movies', movieRoutes); // "/movies" 경로로 들어오는 요청 처리
app.use('/api/showtimes', showtimesRoutes);


// 404 에러 처리
app.use(function(req, res, next) {
  next(createError(404));
});

// 에러 핸들러
app.use(function(err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  res.status(err.status || 500);
  res.render('error');
});
app.listen(3000)
module.exports = app;
