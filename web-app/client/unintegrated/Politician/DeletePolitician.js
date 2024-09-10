import React, { Component } from 'react';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import { ALL_POLITICIANS_QUERY } from './Politicians';

const DELTE_POLITICIAN_MUTATION = gql`
	mutation DELTE_POLITICIAN_MUTATION($id: ID!) {
		deletePolitician(id: $id) {
			id
		}
	}
`;

class DeletePolitician extends Component {
	update = (cache, payload) => {
		// deletePolitician removes listing from the SERVER
		// udate will update the cache to sync the client side
		// 1. Read the cache
		const data = cache.readQuery({ query: ALL_POLITICIANS_QUERY });
		console.log(data);
		// 2. Filter removed listing out of the page
		data.politicians = data.politicians.filter((politician) => politician.id !== payload.data.deletePolitician.id);
		// 3. put the filtered data back
		cache.writeQuery({ query: ALL_POLITICIANS_QUERY, data });
	};
	render() {
		return (
			<Mutation mutation={DELTE_POLITICIAN_MUTATION} variables={{ id: this.props.id }} update={this.update}>
				{(deletePolitician, { error }) => (
					<button
						onClick={() => {
							if (confirm('Are you sure you want to remove this person?')) {
								deletePolitician();
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

export default DeletePolitician;
