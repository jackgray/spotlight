import React, { Component } from 'react';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import { CURRENT_USER_QUERY } from '../User/User';
import { ALL_BILLS_QUERY } from './Bills';

const UPVOTE_BILL_MUTATION = gql`
	mutation upvoteBill($id: ID!) {
		upvoteBill(id: $id) {
			id
		}
	}
`;

// TODO: use SINGLE_BILL_QUERY instead of refetching all bills

class UpvoteBill extends Component {
	update = (cache, payload) => {
		const data = cache.readQuery({ query: ALL_BILLS_QUERY });
		console.log(data);
		data.bills.upvotes = data.bills.upvotes.filter((upvote) => upvote.name !== payload.data.upvote.name);
		console.log(data.bills.upvote.name);
		cache.writeQuery({ query: ALL_BILLS_QUERY, data });
	};
	render() {
		const { id } = this.props;
		console.log(this.props);
		return (
			<Mutation
				mutation={UPVOTE_BILL_MUTATION}
				variables={{ id }}
				refetchQueries={[ { query: CURRENT_USER_QUERY, ALL_BILLS_QUERY } ]}
			>
				{(upvoteBill, { loading }) => (
					<button disabled={loading} onClick={upvoteBill}>
						{this.props.children}
					</button>
				)}
			</Mutation>
		);
	}
}

export default UpvoteBill;
export { UPVOTE_BILL_MUTATION };
