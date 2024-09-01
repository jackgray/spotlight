import React, { Component } from 'react';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import { CURRENT_USER_QUERY } from '../User/User';
import { MY_POLITICIANS_QUERY } from './MyPoliticians';

const UNFOLLOW_POLITICIAN_MUTATION = gql`
	mutation unfollowPolitician($id: ID!) {
		unfollowPolitician(id: $id) {
			id
		}
	}
`;

class UnfollowPolitician extends Component {
	update = (cache, payload) => {
		console.log('update function called');
		const data = cache.readQuery({ query: MY_POLITICIANS_QUERY });
		console.log(data);
		data.me.myPoliticians = data.me.myPoliticians.filter(
			(myPolitician) => myPolitician.id !== payload.data.unfollowPolitician.id
		);

		cache.writeQuery({ query: MY_POLITICIANS_QUERY, data });
	};
	render() {
		const id = this.props.id;
		return (
			<Mutation mutation={UNFOLLOW_POLITICIAN_MUTATION} variables={{ id }} update={this.update}>
				{(unfollowPolitician, { error }) => (
					<button
						onClick={() => {
							if (confirm('Are you sure you want to unfollow this person?')) {
								unfollowPolitician();
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

export default UnfollowPolitician;
export { UNFOLLOW_POLITICIAN_MUTATION };
