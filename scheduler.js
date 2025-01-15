const { exec } = require("child_process");
const cron = require("node-cron");
const mongoose = require("mongoose");

// Helper function for delay
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

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

    for (const theater of theaters) {
      const { name: cinemaName, url: cinemaCode } = theater;
      if (!cinemaCode) {
        console.warn(`${cinemaName}에 code 필드가 없습니다. 건너뜁니다.`);
        continue;
      }

      const command = `python3 lottecinema_crawler.py "${cinemaName}" "${cinemaCode}"`;
      await new Promise((resolve) => {
        exec(command, (error, stdout, stderr) => {
          if (error) {
            console.error(`롯데시네마 Python 실행 오류: ${cinemaName} - ${error.message}`);
          } else {
            console.log(`롯데시네마 ${cinemaName} 업데이트 완료: ${stdout}`);
          }
          resolve();
        });
      });

      // 1분 대기
      await delay(500);
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
      const { theater_name: theaterName, theater_code: theaterCode, region_code: regionCode } = theater;

      if (!regionCode || !theaterCode) {
        console.warn(`CGV ${theaterName}에서 region_code 또는 theater_code가 없습니다. 건너뜁니다.`);
        continue;
      }

      const command = `python3 cgv_crawler.py "${regionCode}" "${theaterCode}" "${theaterName}"`;
      await new Promise((resolve) => {
        exec(command, (error, stdout, stderr) => {
          if (error) {
            console.error(`CGV Python 실행 오류: ${theaterName} - ${error.message}`);
          } else {
            console.log(`CGV ${theaterName} 업데이트 완료: ${stdout}`);
          }
          resolve();
        });
      });

      // 1분 대기
      await delay(500);
    }

    console.log("모든 CGV 영화관 업데이트 완료");
  } catch (error) {
    console.error("CGV 스케줄러 실행 중 오류 발생: ", error);
  }
}

// 메가박스 스케줄 업데이트 함수
async function updateMegaboxSchedules() {
  console.log("메가박스 스케줄러 실행 중...");

  try {
    if (!mongoose.connection.db) {
      console.log("MongoDB 연결 대기 중...");
      await new Promise((resolve) => mongoose.connection.once("open", resolve));
    }

    const theaters = await mongoose.connection.db
      .collection("theaters")
      .find({ name: { $regex: "메가박스" } })
      .toArray();

    if (!theaters.length) {
      console.log("메가박스 영화관 데이터를 찾을 수 없습니다.");
      return;
    }

    for (const theater of theaters) {
      let { name: cinemaName, branch_no: cinemaCode } = theater;
      if (!cinemaCode) {
        console.warn(`${cinemaName}에 code 필드가 없습니다. 건너뜁니다.`);
        continue;
      }

      cinemaName = cinemaName.replace(/\s+/g, "");
      const command = `python3 megabox_crawler.py "${cinemaCode}" "${cinemaName}"`;
      await new Promise((resolve) => {
        exec(command, (error, stdout, stderr) => {
          if (error) {
            console.error(`메가박스 Python 실행 오류: ${cinemaName} - ${error.message}`);
          } else {
            console.log(`메가박스 ${cinemaName} 업데이트 완료: ${stdout}`);
          }
          resolve();
        });
      });

      // 1분 대기
      await delay(500);
    }

    console.log("모든 메가박스 영화관 업데이트 완료");
  } catch (error) {
    console.error("메가박스 스케줄러 실행 중 오류 발생: ", error);
  }
}

// 스케줄러 시작 함수
function startScheduler() {
  console.log("스케줄러가 설정되었습니다.");

  // 매일 자정에 롯데시네마 스케줄러 실행
  cron.schedule("0 1 * * *", updateLotteCinemaSchedules);

  // 매일 오전 1시에 CGV 스케줄러 실행
  cron.schedule("0 2 * * *", updateCGVSchedules);

  // 매일 오전 2시에 메가박스 스케줄러 실행
  cron.schedule("0 3 * * *", updateMegaboxSchedules);

  // 테스트용 즉시 실행
   //updateMegaboxSchedules();
   //updateCGVSchedules();
   //updateLotteCinemaSchedules();
}

module.exports = { startScheduler, updateLotteCinemaSchedules, updateCGVSchedules, updateMegaboxSchedules };
