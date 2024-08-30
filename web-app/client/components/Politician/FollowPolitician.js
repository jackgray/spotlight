import React, { Component } from 'react';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import { CURRENT_USER_QUERY } from '../User/User';
import { MY_POLITICIANS_QUERY } from './MyPoliticians';

const FOLLOW_POLITICIAN_MUTATION = gql`
	mutation followPolitician($id: ID!) {
		followPolitician(id: $id) {
			id
		}
	}
`;

class FollowPolitician extends Component {
	render() {
		const { id } = this.props;
		return (
			<Mutation
				mutation={FOLLOW_POLITICIAN_MUTATION}
				variables={{ id }}
				refetchQueries={[ { query: CURRENT_USER_QUERY, MY_POLITICIANS_QUERY } ]}
			>
				{(followPolitician, { loading }) => (
					<button disabled={loading} onClick={followPolitician}>
						{this.props.children}
						{loading && 'ing'}
					</button>
				)}
			</Mutation>
		);
	}
}

export default FollowPolitician;
export { FOLLOW_POLITICIAN_MUTATION };
