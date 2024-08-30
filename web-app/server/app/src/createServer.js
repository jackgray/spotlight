const { GraphQLServer } = require('graphql-yoga');
const { resolvers } = require('./resolvers');
const db = require('./db');
const { prisma } = require('../prisma-client-js');

// Create the GraphQL Yoga Server

function createServer() {
	return new GraphQLServer({
		typeDefs: 'src/schema.graphql',
		resolvers,
		resolverValidationOptions: {
			requireResolversForResolveType: false
		},
		context: (req) => {
			return { ...req, db, prisma };
		}
	});
}

module.exports = createServer;
