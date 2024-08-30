const { forwardTo } = require('prisma-binding');

const Subscription = {
	bills: {
		subscribe: (parent, args, ctx, info) => {
			return ctx.db.subscription.bill(
				{
					where: {
						mutation_in: [ 'CREATED', 'UPDATED' ]
					}
				},
				info
			);
		}
	},

	billCreated: {
		subscribe: (parent, args, ctx, info) => {
			const selectionSet = `{ previousValues { id title }}`;

			return ctx.db.subscription.bill(
				{
					where: {
						mutation_in: [ 'CREATED' ]
					}
				},
				selectionSet
			);
			{
				mutation;
			}
		}
	},

	billDeleted: {
		subscribe: (parent, args, ctx, info) => {
			const selectionSet = `{previousValues { id title }}`;
			return ctx.db.subscription.bill(
				{
					where: {
						mutation_in: [ 'DELETED' ]
					}
				},
				selectionSet
			);
		},
		resolve: (payload, args, context, info) => {
			const resolver =
				payload ? payload.bill.previousValues :
				payload;
			return resolver;
		}
	}
};

module.exports = { Subscription };
