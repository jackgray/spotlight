import React, { Component } from 'react';
import { graphql } from 'react-apollo';
import gql from 'graphql-tag';

const PUSH_NOTIFICATION_MUTATION = gql`
	mutation PushNotificationMutation($label: String!) {
		pushNotification(label: $label) {
			label
		}
	}
`;

class PushNotification extends Component {
	state = { label: '' };
	_pushNotification = async () => {
		const { label } = this.state;
		await this.props.PushNotificationMutation({
			variables: {
				label
			}
		});
		this.setState({ label: '' });
	};

	render() {
		return (
			<div>
				<input
					value={this.state.label}
					onChange={this.setState({ label: e.target.value })}
					type="text"
					placeholder="label"
				/>
				<button onClick={() => this._pushNotification()}>Submit</button>
			</div>
		);
	}
}

export default graphql(PUSH_NOTIFICATION_MUTATION, {
	name: 'pushNotificationMutation'
})(PushNotification);
