/* eslint-env node */

const path = require("path");
module.exports = {
	/**
	 * 
	 * @param {Object} express host express object
	 * @param {Object} app host express instance 
	 * @param {Object} req request express object
	 * @param {Object} res response express obgect
	 */
	get: function( express, app, req, res ) {
		res.sendFile( path.resolve(__dirname, "./labirinth.html") );
	}
};
