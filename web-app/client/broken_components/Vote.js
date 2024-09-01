import React, { Component } from 'react';
import { Mutation, Query } from 'react-apollo';
import gql from 'graphql-tag';
import { CURRENT_USER_QUERY } from './User/User';
import { ALL_BILLS_QUERY } from './Bill/Bills';

const UPVOTE_BILL_MUTATION = gql`
	mutation upvoteBill($id: ID!) {
		upvoteBill(id: $id) {
			id
		}
	}
`;

const DOWNVOTE_BILL_MUTATION = gql`
	mutation downvoteBill($id: ID!) {
		downvoteBill(id: $id) {
			id
		}
	}
`;

const VOTES_QUERY = gql`
	query bill($id: ID!) {
		upvotes {
			id
		}
		downvotes {
			id
		}
	}
`;

// TODO: use SINGLE_BILL_QUERY instead of refetching all bills

class Vote extends Component {
	render() {
		const { id } = this.props;
		return (
			<div>
				<Mutation
					mutation={UPVOTE_BILL_MUTATION}
					variables={{ id }}
					// refetchQueries={[ { query: CURRENT_USER_QUERY, ALL_BILLS_QUERY } ]}
				>
					{(upvoteBill, { loading }) => (
						<button disabled={loading} onClick={upvoteBill}>
							👍
						</button>
					)}
				</Mutation>

				{/* <Query query={VOTES_QUERY} variables={{ id }}>
					{({ error, data }) => {
						if (error) return `Error retrieving query. ${error.message}`;

						return <span>{data.bill.upvotes.length - data.bill.downvotes.length}</span>;
					}}
				</Query> */}
				<Mutation
					mutation={DOWNVOTE_BILL_MUTATION}
					variables={{ id }}
					refetchQueries={[ { query: CURRENT_USER_QUERY } ]}
				>
					{(downvoteBill, { loading }) => (
						<button disabled={loading} onClick={downvoteBill}>
							👎
						</button>
					)}
				</Mutation>
			</div>
		);
	}
}

export default Vote;
