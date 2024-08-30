const { forwardTo } = require('prisma-binding');

const Query = {
	// user related queries:
	me(parent, args, ctx, info) {
		if (!ctx.request.userId) {
			return null;
		}
		return ctx.db.query.user(
			{
				where: { id: ctx.request.userId }
			},
			info
		);
	},
	async users(parents, args, ctx, info) {
		// 1. check if user is logged in
		if (!ctx.request.userId) {
			throw new Error('You must be logged in!');
		}
		console.log(ctx.request.userId);
		// 2. checks if user has permission to query all users
		hasPermission(ctx.request.user, [ 'ADMIN', 'PERMISSIONUPDATE' ]);

		// 3. query all users if user has ADMIN privileges
		return ctx.db.query.users({}, info);
	},
	// politician related queries
	politicians: forwardTo('db'),
	politician: forwardTo('db'),
	politiciansConnection: forwardTo('db'),
	async myPolitician(parents, args, ctx, info) {
		// 1. Authorize loggin
		if (!ctx.request.userId) {
			throw new Error('You arent logged in!');
		}
		// 2. Query list of myPoliticians
		const { politician } = await ctx.db.query(
			{
				where: { id: args.id }
			},
			info
		);
		// 3. Check if user has permissions
		const isOwner = politician.user.id === ctx.request.userId;
		const hasPermission = ctx.request.user.permissions.includes('ADMIN');
		if (!isOwner || !hasPermission) {
			throw new Error('You do not have permission');
		}
		return myPolitician;
	},

	myPoliticians: (parent, args, ctx) => {
		const { userId } = ctx.request;

		if (!userId) {
			throw new Error('You must log in to view myPoliticians');
		}

		const myPoliticians = ctx.prisma.politicians({
			where: {
				user: {
					id: userId
				}
			}
		});
		return myPoliticians;
	},
	async owner(parents, args, ctx, info) {
		owner = await ctx.db.query.politician(
			{
				where: {
					owner: {
						id: userId
					}
				}
			},
			info
		);
		return owner;
	},

	// bill related queries
	bill: forwardTo('db'),
	bills: forwardTo('db'),

	myBills(parent, args, ctx, info) {
		const { userId } = ctx.request;

		if (!userId) {
			throw new Error('You must log in to view myBills');
		}

		const myBills = ctx.db.query.bills({
			where: {
				user: {
					id: userId
				}
			},
			info
		});
		return myBills;
	},

	async billsScrape(parent, args, ctx, info) {
		// const { bill } = await ctx.db.query(
		// 	{
		// 		where: {
		// 			number: args.number
		// 		}
		// 	},
		// 	info
		// );
		const url =
			'https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22congress%22%3A115%2C%22type%22%3A%22bills%22%2C%22chamber%22%3A%22Senate%22%7D';
		puppeteer
			.launch()
			.then(async (browser) => {
				const page = await browser.newPage();
				await page.goto(url);
				await page.waitForSelector('li.expanded > a'); // bill number is inside a tag with href for the bill page. li.expanded represents a single billCard result

				const bills = await page.evaluate(() => {
					bills.numbers = Array.from(document.querySelectorAll('li.expanded . a'));
					return bills;
				});
			})
			.then(await browser.close())
			.catch(function(err) {
				console.log(err);
			});

		return bills;
	},
	// comment related queries
	comment: forwardTo('db'),
	comments: forwardTo('db'),
	async billComment(parent, args, ctx, info) {
		const { comment } = await ctx.db.query({
			where: {
				id: args.id
			},
			info
		});
		return comment;
	}
	// vote related queries
	// upvote: forwardTo('db'),
	// downvote: forwardTo('db')
};

module.exports = { Query };
