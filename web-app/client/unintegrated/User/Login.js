import React, { Component } from 'react';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import Link from 'next/link';
import Form from '../styles/Form';
import Error from '../ErrorMessage';
import { CURRENT_USER_QUERY } from './User';

const LOGIN_MUTATION = gql`
	mutation LOGIN_MUTATION($email: String!, $password: String!) {
		signin(email: $email, password: $password) {
			id
			email
			name
		}
	}
`;

class Login extends Component {
	state = {
		name: '',
		password: '',
		email: ''
	};
	saveToState = (e) => {
		this.setState({ [e.target.name]: e.target.value });
	};
	render() {
		return (
			<div>
				<Mutation
					mutation={LOGIN_MUTATION}
					variables={this.state}
					refetchQueries={[ { query: CURRENT_USER_QUERY } ]}
				>
					{(signup, { error, loading }) => (
						<Form
							method="post"
							onSubmit={async (e) => {
								e.preventDefault();
								await signup();
								this.setState({
									name: '',
									email: '',
									password: ''
								});
							}}
						>
							<fieldset disabled={loading} aria-busy={loading}>
								<h2>Sign into your account</h2>
								<Error error={error} />
								<label htmlFor="email">
									Email
									<input
										type="email"
										name="email"
										placeholder="email"
										value={this.state.email}
										onChange={this.saveToState}
									/>
								</label>
								<label htmlFor="password">
									Password
									<input
										type="password"
										name="password"
										placeholder="password"
										value={this.state.password}
										onChange={this.saveToState}
									/>
								</label>

								<button type="submit">Sign In!</button>
							</fieldset>
						</Form>
					)}
				</Mutation>
				<div>
					Don't have an account?{' '}
					<button>
						<Link href="/signup">
							<a>Sign Up</a>
						</Link>
					</button>
				</div>
			</div>
		);
	}
}

export default Login;
