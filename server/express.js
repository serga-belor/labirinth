// Sergey Belorusets, 2018
//
// Module for http-server project to
// process routes associated with "labirinth" progect
// Use "express" to process requests and send responses
//

/* eslint no-console: ["error", { allow: ["log", "warn", "error"] }] */
/* eslint-env node */

const path = require("path");
module.exports = {
	/**
	 * @param {Object} express host express object
	 * @param {Object} app host express instance 
	 * @param {Object} req request express object
	 * @param {Object} res response express obgect
	 */
	get: function( express, app, req, res ) {
		res.sendFile( path.resolve(__dirname, "./labirinth.html") );
	},
	/**
	 * Add project's static resources
	 * @param {Object} express host express object
	 * @param {Object} app host express instance 
	 */
	static: function( express, app ) {
		console.log("labirinth static: " + __dirname);
		app.use( express.static( __dirname ) );
	}
};
