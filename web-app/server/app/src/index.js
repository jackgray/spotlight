const cookieParser = require('cookie-parser');
const jwt = require('jsonwebtoken');
const logger = require('morgan');

require('dotenv').config({ path: 'variables.env' });
const createServer = require('./createServer');
const db = require('./db');

const server = createServer();

// TODO: use express middleware to handle cookies (JWT)
server.express.use(cookieParser());

// For Scraping
server.express.use(logger('dev'));

// logging in: decode jwt and store to userId for request access
server.express.use((req, res, next) => {
	const { token } = req.cookies;
	if (token) {
		const { userId } = jwt.verify(token, process.env.APP_SECRET);
		// save userId to req object for session auth
		req.userId = userId;
	}
	next();
});

// if no userId, break
server.express.use(async (req, res, next) => {
	if (!req.userId) return next();
	const user = await db.query.user(
		{ where: { id: req.userId } },
		'{ id, permissions, email, name }'
	);
	req.user = user;
	next();
});

server.start(
	{
		cors: {
			credentials: true,
			origin: process.env.FRONTEND_URL
		}
	},
	(deets) => {
		console.log(
			`Server is now running on port http://localhost:${deets.port}`
		);
	}
);
