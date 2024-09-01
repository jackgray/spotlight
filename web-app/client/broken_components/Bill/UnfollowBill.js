import React, { Component } from 'react';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import { CURRENT_USER_QUERY } from '../User/User';
import { MY_BILLS_QUERY } from './MyBills';

const UNFOLLOW_BILL_MUTATION = gql`
	mutation unfollowBill($id: ID!) {
		unfollowBill(id: $id) {
			id
		}
	}
`;

class UnfollowBill extends Component {
	update = (cache, payload) => {
		console.log('update function called');
		const data = cache.readQuery({ query: MY_BILLS_QUERY });
		console.log(data);
		data.me.myBills = data.me.myBills.filter((myBill) => myBill.id !== payload.data.unfollowBill.id);

		cache.writeQuery({ query: MY_BILLS_QUERY, data });
	};
	render() {
		const { id } = this.props;
		return (
			<Mutation mutation={UNFOLLOW_BILL_MUTATION} variables={{ id }} update={this.update}>
				{(unfollowBill, { loading }) => (
					<button
						disabled={loading}
						onClick={() => {
							if (confirm('Are you sure you want to unfollow this person?')) {
								unfollowBill();
							}
						}}
					>
						{this.props.children}
						{loading && 'ing'}
					</button>
				)}
			</Mutation>
		);
	}
}

export default UnfollowBill;
export { UNFOLLOW_BILL_MUTATION };
