import React, { Component } from 'react';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import { CURRENT_USER_QUERY } from '../User/User';

const DOWNVOTE_BILL_MUTATION = gql`
	mutation downvoteBill($id: ID!) {
		downvoteBill(id: $id) {
			id
		}
	}
`;

class DownvoteBill extends Component {
	render() {
		const { id } = this.props;
		return (
			<Mutation
				mutation={DOWNVOTE_BILL_MUTATION}
				variables={{ id }}
				refetchQueries={[ { query: CURRENT_USER_QUERY } ]}
			>
				{(downvoteBill, { loading }) => (
					<button disabled={loading} onClick={downvoteBill}>
						{this.props.children}
						{loading && 'ing'}
					</button>
				)}
			</Mutation>
		);
	}
}

export default DownvoteBill;
export { DOWNVOTE_BILL_MUTATION };
