import React, { Component } from 'react';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import { CURRENT_USER_QUERY } from '../User/User';
import { MY_BILLS_QUERY } from './MyBills';

const FOLLOW_BILL_MUTATION = gql`
	mutation followBill($id: ID!) {
		followBill(id: $id) {
			id
		}
	}
`;

class FollowBill extends Component {
	render() {
		const { id } = this.props;
		return (
			<Mutation
				mutation={FOLLOW_BILL_MUTATION}
				variables={{ id }}
				refetchQueries={[ { query: CURRENT_USER_QUERY, MY_BILLS_QUERY } ]}
			>
				{(followBill, { loading }) => (
					<button disabled={loading} onClick={followBill}>
						{this.props.children}
						{loading && 'ing'}
					</button>
				)}
			</Mutation>
		);
	}
}

export default FollowBill;
export { FOLLOW_BILL_MUTATION };
