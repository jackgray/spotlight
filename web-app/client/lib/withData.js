// makes apollo-client available via props
import withApollo from 'next-with-apollo';
import { split, ApolloLink, Observable } from 'apollo-link';
import { getMainDefinition } from 'apollo-utilities';
import { ApolloClient } from 'apollo-client';
import { setContext } from 'apollo-link-context';
import { HttpLink } from 'apollo-link-http';
import { InMemoryCache } from 'apollo-cache-inmemory';
import { onError } from 'apollo-link-error';
import { WebSocketLink } from 'apollo-link-ws';
import { SubscriptionClient } from 'subscriptions-transport-ws';

import { endpoint, prodEndpoint, wsEndpoint } from '../config';
import { Subscription } from 'react-apollo';

// To start with a hybrid WebSocket transport, that handles only subscriptions over WebSocket, create your SubscriptionClient and a regular HTTP network interface, then extend your network interface to use the WebSocket client for GraphQL subscriptions:

function createClient({ headers }) {
	// create a http link for queries and mutations
	const httpLink = new HttpLink({
		uri:

				process.env.NODE_ENV === 'development' ? endpoint :
				prodEndpoint,
		credentials: 'include'
	});

	// websocket link for subscriptions
	const wsLink =
		process.browser ? new WebSocketLink({
			uri: wsEndpoint,
			options: { reconnect: true }
		}) :
		() => console.log('SSR');

	// // configure the websocket connection for subscriptions
	// const client =
	// 	process.browser ? new SubscriptionClient(

	// 			process.env.NODE_ENV === 'development' ? wsEndpoint :
	// 			wsEndpoint,
	// 		{ reconnect: true }
	// 	) :
	// 	() => console.log('SSR');

	// const wsLink =
	// 	process.browser ? new WebSocketLink(client) :
	// 	() => console.log('SSR');

	// configure http-link for non-subscription calls
	const networkLink = split(
		({ query }) => {
			const { kind, operation } = getMainDefinition(query);
			return (
				kind === 'OperationDefinition' && operation === 'subscription'
			);
		},
		wsLink,
		httpLink
	);

	const cache = new InMemoryCache();

	const request = async (operation) => {
		operation.setContext({
			fetchOptions: {
				credentials: 'include'
			},
			headers
		});
	};

	const requestLink = new ApolloLink(
		(operation, forward) =>
			new Observable((observer) => {
				let handle;
				Promise.resolve(operation)
					.then((oper) => request(oper))
					.then(() => {
						handle = forward(operation).subscribe({
							next: observer.next.bind(observer),
							error: observer.error.bind(observer),
							complete: observer.complete.bind(observer)
						});
					})
					.catch(observer.error.bind(observer));

				return () => {
					if (handle) handle.unsubscribe();
				};
			})
	);

	return new ApolloClient({
		link: ApolloLink.from([
			onError(({ graphQLErrors, networkError }) => {
				if (graphQLErrors) {
					// sendToLoggingService(graphQLErrors);
					console.log(graphQLErrors);
				}
				if (networkError) {
					console.log(networkError);
					// logoutUser();
				}
			}),
			requestLink,
			networkLink
		]),
		cache,
		ssrMode: true
	});
}

export default withApollo(createClient);
