const { exec } = require("child_process");
const cron = require("node-cron");
const mongoose = require("mongoose");

// 롯데시네마 스케줄 업데이트 함수
async function updateLotteCinemaSchedules() {
  console.log("롯데시네마 스케줄러 실행 중...");

  try {
    if (!mongoose.connection.db) {
      console.log("MongoDB 연결 대기 중...");
      await new Promise((resolve) => mongoose.connection.once("open", resolve));
    }

    const theaters = await mongoose.connection.db
      .collection("theaters")
      .find({ name: { $regex: "롯데시네마" } })
      .toArray();

    if (!theaters.length) {
      console.log("롯데시네마 영화관 데이터를 찾을 수 없습니다.");
      return;
    }

    const limit = 5; // 동시에 실행할 Python 스크립트 수 제한
    for (let i = 0; i < theaters.length; i += limit) {
      const batch = theaters.slice(i, i + limit);
      const promises = batch.map((theater) => {
        const { name: cinemaName, url: cinemaCode } = theater;
        if (!cinemaCode) {
          console.warn(`${cinemaName}에 code 필드가 없습니다. 건너뜁니다.`);
          return Promise.resolve();
        }
        const command = `python3 lottecinema_crawler.py "${cinemaName}" "${cinemaCode}"`;
        return new Promise((resolve, reject) => {
          exec(command, (error, stdout, stderr) => {
            if (error) {
              console.error(`롯데시네마 Python 실행 오류: ${cinemaName} - ${error.message}`);
              reject(error);
            } else {
              console.log(`롯데시네마 ${cinemaName} 업데이트 완료: ${stdout}`);
              resolve(stdout);
            }
          });
        });
      });
      await Promise.all(promises);
    }
    console.log("모든 롯데시네마 영화관 업데이트 완료");
  } catch (error) {
    console.error("롯데시네마 스케줄러 실행 중 오류 발생: ", error);
  }
}

// CGV 스케줄 업데이트 함수
async function updateCGVSchedules() {
  console.log("CGV 스케줄러 실행 중...");

  try {
    if (!mongoose.connection.db) {
      console.log("MongoDB 연결 대기 중...");
      await new Promise((resolve) => mongoose.connection.once("open", resolve));
    }

    const theaters = await mongoose.connection.db
      .collection("theaters")
      .find({ theater_name: { $regex: "CGV" } })
      .toArray();

    if (!theaters.length) {
      console.log("CGV 영화관 데이터를 찾을 수 없습니다.");
      return;
    }

    for (const theater of theaters) {
      const { theater_name: theater_name, theater_code: theater_code, region_code: region_code } = theater;

      if (!region_code || !theater_code) {
        console.warn(`CGV ${theater_name}에서 region_code 또는 theater_code가 없습니다. 건너뜁니다.`);
        continue;
      }

      const command = `python3 cgv_crawler.py "${region_code}" "${theater_code}" "${theater_name}"`;
      exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error(`CGV Python 실행 오류: ${theater_name} - ${error.message}`);
          return;
        }
        console.log(`CGV ${theater_name} 업데이트 완료: ${stdout}`);
      });
    }
    console.log("모든 CGV 영화관 업데이트 완료");
  } catch (error) {
    console.error("CGV 스케줄러 실행 중 오류 발생: ", error);
  }
}

// 스케줄러 시작 함수
function startScheduler() {
  console.log("스케줄러가 설정되었습니다.");
  // updateCGVSchedules();
  // 매일 자정에 롯데시네마 스케줄러 실행
  cron.schedule("0 0 * * *", updateLotteCinemaSchedules);

  // 매일 오전 1시에 CGV 스케줄러 실행
  cron.schedule("0 1 * * *", updateCGVSchedules);
}

module.exports = { startScheduler, updateLotteCinemaSchedules, updateCGVSchedules };
