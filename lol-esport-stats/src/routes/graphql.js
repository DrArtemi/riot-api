import { ApolloServer } from 'apollo-server-lambda';
import { ApolloServerPluginLandingPageGraphQLPlayground } from 'apollo-server-core';
import { makeSchema } from 'nexus';
import { PrismaClient } from '../utils/prisma';
import * as types from '../graphql';

const schema = makeSchema({
	types,
	outputs: false
});

/**
 * @type {import('apollo-server-lambda').ApolloServer}
 */
const server = new ApolloServer({
	schema,
	context: async () => ({
		db: new PrismaClient()
	}),
	playground: false,
	introspection: true,
	tracing: true,
	plugins: [ApolloServerPluginLandingPageGraphQLPlayground()]
});

const gqlHandler = server.createHandler();

/**
 * @type {import('@sveltejs/kit').RequestHandler}
 */
const handler = async ({ method: httpMethod, headers, path, rawBody: body }) =>
	await gqlHandler(
		{
			httpMethod,
			headers,
			path,
			body,
			requestContext: { version: '2.0' }
		},
		{},
		(err, { statusCode: status, body, headers }) => {
			if (err) {
				return Promise.reject(err);
			} else {
				return Promise.resolve({
					status,
					body,
					headers
				});
			}
		}
	);

export const get = handler;
export const post = handler;
