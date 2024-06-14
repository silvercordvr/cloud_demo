// ================== Test authorization for alpha web-server ONLY!

const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..', 'python', 'users.txt');

function readCredentialsFromFile(filePath) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                return reject(err);
            }
            const [username, password] = data.split('\n')[0].trim().split(':');
            resolve({ username: username.trim(), password: password.trim() });
        });
    });
}

async function createAuthHeadersFromFile() {
    try {

        const { username, password } = await readCredentialsFromFile(filePath);
        const token = Buffer.from(`${username}:${password}`, 'utf8').toString('base64');
        return {
            'Authorization': `Basic ${token}`,
            'Content-Type': 'application/json'
        };
    } catch (err) {
        console.error(`Error reading credentials from file: ${err.message}`);
        throw err;
    }
}

function returnHeaderForClient() {
    const token = Buffer.from(`${'test'}:${'111111'}`, 'utf8').toString('base64');
        return {
            'Authorization': `Basic ${token}`,
            'Content-Type': 'application/json'
        };
}

module.exports = {
    createAuthHeadersFromFile
};