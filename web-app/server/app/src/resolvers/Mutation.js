const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { randomBytes } = require('crypto');
const { promisify } = require('util');
const { hasPermission } = require('../utils');

const Mutation = {
	async createPolitician(parent, args, ctx, info) {
		// TODO: check if user is logged in
		const { userId } = ctx.request;
		const politician = await ctx.db.mutation.createPolitician(
			{
				data: {
					...args
				}
			},
			info
		);
		return politician;
	},
	async updatePolitician(parent, args, ctx, info) {
		// make a copy of new fields
		const updates = { ...args };
		// remove ID from the updates (don't update ID)
		delete updates.id;
		// run update method
		return await ctx.db.mutation.updatePolitician({
			data: updates,
			where: {
				id: args.id
			},
			info
		});
	},

	async deletePolitician(parent, args, ctx, info) {
		const where = { id: args.id };
		//1. find the item
		const politician = await ctx.db.query.politician({ where }, `{id name}`);
		// check for permissions
		// delete listing
		return ctx.db.mutation.deletePolitician({ where }, info);
	},
	async followPolitician(parent, args, ctx, info) {
		// 1. Check permissions
		const { userId } = ctx.request;
		if (!userId) {
			throw new Error('Sign in or create an account to follow politicians.');
		}

		connect = await ctx.db.mutation.updatePolitician({
			data: {
				followers: {
					connect: {
						id: userId
					}
				}
			},
			where: {
				id: args.id
			}
		});

		return connect;
	},
	async unfollowPolitician(parent, args, ctx, info) {
		// 1. Check permissions
		const { userId } = ctx.request;
		if (!userId) {
			throw new Error('Sign in or create an account to save myPoliticians.');
		}

		disconnect = await ctx.db.mutation.updatePolitician({
			data: {
				followers: {
					disconnect: {
						id: userId
					}
				}
			},
			where: {
				id: args.id
			}
		});

		return disconnect;
	},

	async toggleFollowPolitician(parent, args, ctx, info) {
		const { userId } = ctx.request;
		if (!userId) {
			throw new Error('You must be signed in');
		}

		me = await ctx.db.query.me({
			data: {
				myPoliticians: {
					where: {
						id: politician.id
					}
				}
			}
		});

		connect = await ctx.db.mutation.updatePolitician({
			where: {
				id: args.id
			},
			data: {
				followers: {
					connect: { id: userId }
				}
			}
		});
		disconnect = await ctx.db.mutation.updatePolitician({
			where: { id: args.id },
			data: {
				followers: {
					disconnect: { id: userId }
				}
			}
		});
		return null;
	},

	async createBill(parent, args, ctx) {
		// TODO: check if user is logged in
		const { userId } = ctx.request;
		const bill = await ctx.prisma.createBill({
			code: args.code,
			title: args.title,
			summary: args.summary,
			committees: args.summary,
			sponsor: args.sponsor
		});
		return bill;
	},
	updateBill(parent, args, ctx, info) {
		// make a copy of new fields
		const updates = { ...args };
		// remove ID from the updates (don't update ID)
		delete updates.id;
		// run update method
		return ctx.db.mutation.updateBill({
			data: updates,
			where: {
				id: args.id
			},
			info
		});
	},
	async deleteBill(parent, args, ctx, info) {
		const where = { id: args.id };
		//1. find the item
		const politician = await ctx.db.query.politician({ where }, `{id name}`);
		// check for permissions
		// delete listing
		return ctx.db.mutation.deleteBill({ where }, info);
	},
	async followBill(parent, args, ctx, info) {
		// 1. Check permissions
		const { userId } = ctx.request;
		if (!userId) {
			throw new Error('Sign in or create an account to follow politicians.');
		}

		return await ctx.db.mutation.updateBill({
			data: {
				followers: {
					connect: {
						id: userId
					}
				}
			},
			where: {
				id: args.id
			}
		});
	},
	async unfollowBill(parent, args, ctx, info) {
		// 1. Check permissions
		const { userId } = ctx.request;
		if (!userId) {
			throw new Error('Sign in or create an account to save myBills.');
		}

		return await ctx.db.mutation.updateBill({
			data: {
				followers: {
					disconnect: {
						id: userId
					}
				}
			},
			where: {
				id: args.id
			}
		});
	},

	async upvoteBill(parent, args, ctx, info) {
		const { userId } = ctx.request;
		if (!userId) {
			throw new Error('You must be logged in');
		}
		const upvoted = ctx.prisma.$exists.bill({
			id: args.id,
			upvotes: {
				id: userId
			}
		});
		const downvoted = ctx.prisma.$exists.bill({
			id: args.id,
			downvotes: {
				id: userId
			}
		});
		if (upvoted && downvoted) {
			console.log('found upvote and downvote. disconnecting one.');
			upvote = await ctx.db.mutation.updateBill(
				{
					data: {
						downvotes: {
							disconnect: {
								id: userId
							}
						}
					},
					where: {
						id: args.id
					}
				},
				info
			);
		} else if (upvoted) {
			console.log('undoing previous upvote');
			upvote = await ctx.db.mutation.updateBill(
				{
					upvotes: {
						disconnect: {
							id: userId
						}
					},
					where: {
						id: args.id
					}
				},
				info
			);
		} else if (downvoted) {
			console.log('previously downvoted. changing your mind...');
			upvote = await ctx.db.mutation.updateBill(
				{
					data: {
						downvotes: {
							disconnect: {
								id: userId
							}
						},
						upvotes: {
							connect: {
								id: userId
							}
						}
					},
					where: { id: args.id }
				},
				info
			);
		} else {
			console.log('default');
			upvote = await ctx.db.mutation.updateBill(
				{
					data: {
						upvotes: {
							connect: { id: userId }
						}
					},
					where: { id: args.id }
				},
				info
			);
		}
		return upvote;
	},

	async downvoteBill(parent, args, ctx, info) {
		const { userId } = ctx.request;
		if (!userId) {
			throw new Error('You must be logged in');
		}

		const upvoted = ctx.prisma.$exists.bill({
			id: args.id,
			upvotes: {
				id: userId
			}
		});

		const downvoted = ctx.prisma.$exists.bill({
			id: args.id,
			downvotes: {
				id: userId
			}
		});

		let downvote;
		if (upvoted && downvoted) {
			downvote = await ctx.db.mutation.updateBill({
				data: {
					upvotes: {
						disconnect: {
							id: userId
						}
					}
				},
				where: {
					id: args.id
				}
			});
		} else if (downvoted) {
			downvote = await ctx.db.mutation.updateBill({
				data: {
					downvotes: {
						disconnect: {
							id: userId
						}
					}
				},
				where: {
					id: args.id
				}
			});
		}
		if (upvoted) {
			downvote = await ctx.db.mutation.updateBill({
				data: {
					upvotes: {
						disconnect: {
							id: userId
						}
					},
					downvotes: {
						connect: {
							id: userId
						}
					}
				},
				where: {
					id: args.id
				}
			});
		} else {
			downvote = await ctx.db.mutation.updateBill({
				data: {
					downvotes: {
						connect: {
							id: userId
						}
					}
				},
				where: { id: args.id }
			});
		}
		return downvote;
	},

	async commentBill(parent, args, ctx) {
		const { userId } = ctx.request;
		if (!userId) {
			throw new Error('You must sign in to leave a comment');
		}
		const comment = await ctx.prisma.updateBill({
			data: {
				comments: {
					create: {
						content: args.content,
						author: { connect: { id: userId } }
					}
				}
			},
			where: { id: args.id }
		});

		return comment;
	},

	async scrapeBill(parent, { number, title }, ctx, info) {
		const exists = await ctx.db.query.bill({ where: { number } });
		if (exists) {
			throw new Error(`There is already a bill ${number} in the database. It is titled ''${exists.title}''`);
		}

		const $ = cheerio.load(data);
		const items = [];
		$('p').filter((i, el) => {
			const data = $(el);
			const number = data.find('[data-begin]').first().text();
			const title = data.find('.paragraphtitle').first().text();
			//const content = data.find('.reftext').children().first().text();
			const order = i;
			const type = null;
			const item = {};
		});
		const bill = await ctx.db.mutation.createBill(
			{
				data: {
					...args,
					title
				}
			},
			info
		);
		return bill;
	},

	pushNotification: (parent, args) => {
		const newNotification = { label: args.label };
		notifications.push(newNotification);
		return newNotification;
	},
	createNotification: (parent, args, ctx, info) => {
		return ctx.db.mutation.createNotification(
			{
				data: {
					...args
				}
			},
			info
		);
	},

	async signup(parent, args, ctx, info) {
		// convert email to lowercase
		args.email = args.email.toLowerCase();
		// hash password
		const password = await bcrypt.hash(args.password, 10);
		// createUser in db
		const user = await ctx.db.mutation.createUser(
			{
				data: {
					...args,
					password,
					permissions: { set: [ 'USER' ] }
				}
			},
			info
		);
		// generate a JWT for user auth
		const token = jwt.sign({ userId: user.id }, process.env.APP_SECRET);
		// set token as a cookie in res object
		ctx.response.cookie('token', token, {
			httpOnly: true,
			maxAge: 1000 * 60 * 60 * 24 * 265 // 1 year
		});
		return user;
	},
	async signin(parent, { email, password }, ctx, info) {
		// 1. Try to match user to email given
		const user = await ctx.db.query.user({ where: { email } });
		if (!user) {
			throw new Error(`The email address ${email} does not have an account`);
		}
		// 2. Authenticate password
		const valid = await bcrypt.compare(password, user.password);
		if (!valid) {
			throw new Error('Invalid Password :(');
		}
		// 3. Create token
		const token = jwt.sign({ userId: user.id }, process.env.APP_SECRET);
		// 4. make token a cookie to store auth in browser
		ctx.response.cookie('token', token, {
			httpOnly: true,
			maxAge: 1000 * 60 * 60 * 24 * 365
		});
		return user;
	}
};

module.exports = { Mutation };
