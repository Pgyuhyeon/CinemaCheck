var createError = require("http-errors");
var express = require("express");
var path = require("path");
var cookieParser = require("cookie-parser");
var logger = require("morgan");
const mongoose = require("mongoose");
const cors = require("cors"); // CORS 패키지 추가
const { startScheduler, updateLotteCinemaSchedules } = require("./scheduler");

const theaterRoutes = require('./routes/theaters');

const mongoURI = "mongodb://localhost:27017/theaterDB";




mongoose
  .connect(mongoURI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("MongoDB 연결 성공"))
  .catch((err) => console.error("MongoDB 연결 실패: ", err));

var app = express();

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "pug");

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));
app.use('/api/theaters', theaterRoutes);
// CORS 설정 추가
app.use(cors()); // 모든 도메인 허용
// app.use(cors({ origin: 'http://your-frontend-domain.com' })); // 특정 도메인만 허용
// 스케줄러 실행
startScheduler();
// updateLotteCinemaSchedules();

app.use(function (req, res, next) {
  next(createError(404));
});

app.use(function (err, req, res, next) {
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};
  res.status(err.status || 500);
  res.render("error");
});

app.listen(3000, () => {
  console.log("서버가 http://localhost:3000 에서 실행 중입니다.");
});

module.exports = app;
