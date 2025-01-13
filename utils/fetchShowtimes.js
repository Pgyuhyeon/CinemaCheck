const { spawn } = require('child_process');
const Showtimes = require('../models/Showtimes'); // 상영시간표 모델

async function fetchShowtimes(theaterCode) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', ['fetch_cgv_showtimes.py', theaterCode]);

    let data = '';
    pythonProcess.stdout.on('data', (chunk) => {
      data += chunk.toString();
    });

    pythonProcess.stderr.on('data', (err) => {
      reject(err.toString());
    });

    pythonProcess.on('close', async () => {
      try {
        const showtimes = JSON.parse(data);

        // MongoDB에 저장 또는 업데이트
        await Showtimes.findOneAndUpdate(
          { theaterCode },
          { $set: { showtimes, updatedAt: Date.now() } },
          { upsert: true }
        );

        resolve(showtimes); // 저장된 데이터를 반환
      } catch (error) {
        reject(error);
      }
    });
  });
}

module.exports = fetchShowtimes;
