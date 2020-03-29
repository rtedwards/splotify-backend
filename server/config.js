// config.js
const dotenv = require('dotenv');
dotenv.config();
module.exports = {
    client_id: process.env.SPOTIFY_CLIENT_ID,
    client_secret: process.env.SPOTIFY_CLIENT_SECRET,
    redirect_uri: process.env.SPOTIFY_REDIRECT_URI,
    port: process.env.PORT
};