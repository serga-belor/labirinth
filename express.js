/* eslint-env node */

const path = require("path");
module.exports = function(express, app, req, res) {
	res.sendFile( path.resolve(__dirname, "./labirinth.html") );
};
