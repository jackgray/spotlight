import React, { Component } from 'react';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import { ALL_BILLS_QUERY } from './Bills';

const DELETE_BILL_MUTATION = gql`
	mutation DELETE_BILL_MUTATION($id: ID!) {
		deleteBill(id: $id) {
			id
		}
	}
`;

class DeleteBill extends Component {
	// update cache directly instead of calling the server
	update = (cache, payload) => {
		const data = cache.readQuery({ query: ALL_BILLS_QUERY });
		console.log(data);
		// filter out deleted bill by its id
		data.bills = data.bills.filter((bill) => bill.id !== payload.data.deleteBill.id);
		// overwrite cache with filtered query
		cache.writeQuery({ query: ALL_BILLS_QUERY, data });
	};
	render() {
		return (
			<Mutation mutation={DELETE_BILL_MUTATION} variables={{ id: this.props.id }} update={this.update}>
				{(deleteBill, { error }) => (
					<button
						onClick={() => {
							if (confirm('Are you sure you want to remove this person?')) {
								deleteBill();
							}
						}}
					>
						{this.props.children}
					</button>
				)}
			</Mutation>
		);
	}
}

export default DeleteBill;
