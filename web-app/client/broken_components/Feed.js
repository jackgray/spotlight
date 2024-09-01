// import React, { Component } from 'react';
// import gql from 'graphql-tag';
// import { Subscription } from 'react-apollo';

// const BILL_UPDATED_SUBSCRIPTION = gql`
// 	subscription bills {
// 		bills {
// 			node {
// 				id
// 				title
// 			}
// 		}
// 	}
// `;

// const BILL_CREATED_SUBSCRIPTION = gql`
// 	subscription billCreated($title: String) {
// 		billCreated(title: $title) {
// 			bill {
// 				mutation
// 				updatedFields
// 				node {
// 					title
// 				}
// 			}
// 		}
// 	}
// `;

// class Feed extends Component {
//     _updateCacheAfterChange = (store, createBill, billId) => {
//     const data= strore.readQuery({query: BILLS_QUERY})

// }

// const Feed = ({ title }) => (
// 	<div>
// 		<div>Subscriptions</div>
// 		<Subscription
// 			subscription={BILL_CREATED_SUBSCRIPTION}
// 			variables={{ title }}
// 		>
// 			{({ data: { billCreated }, loading }) => (
// 				<h4>New bill added: {!loading && billCreated.node.title}</h4>
// 			)}
// 		</Subscription>
// 	</div>
// );

// export default Feed;
