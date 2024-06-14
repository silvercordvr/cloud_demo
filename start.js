/*================= ARGS =============*/
// --------- npm start 

const { spawn } = require('child_process');

const npmPath = process.platform === 'win32' ? 'npm.cmd' : 'npm';

function spawnProcess(name, script) {
  return new Promise((resolve) => {
    const process = spawn(npmPath, ['run', script], { stdio: 'inherit' });
    process.on('close', (code) => {
      if (code !== 0) {
        console.error(`Process ${name} finished with error code: ${code}`);
      }
      resolve(`Process ${name} finished with code ${code}`);
    });
  });
}

Promise.all([
  spawnProcess('Python Photo', 'start-python-photo'),
  spawnProcess('Python TTS', 'start-python-tts'),
  spawnProcess('Python STT', 'start-python-stt'),
  spawnProcess('Python App', 'start-python-app'),
  spawnProcess('Node Server', 'start-node')
]).then(results => {
  console.log('All processes started with result:', results);
});

