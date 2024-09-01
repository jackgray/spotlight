import { Query, Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import Error from '../ErrorMessage';
import Table from '../styles/Table';
import PropTypes from 'prop-types';

const possiblePermissions = [
	'ADMIN',
	'USER',
	'POLITICIANCREATE',
	'POLITICIANUPDATE',
	'POLITICIANDELETE',
	'PERMISSIONUPDATE'
];

const UPDATE_PERMISSIONS_MUTATION = gql`
	mutation updatePermissions($permissions: [Permission], $userId: ID!) {
		updatePermissions(permissions: $permissions, userId: $userId) {
			id
			permissions
			name
			email
		}
	}
`;

const ALL_USERS_QUERY = gql`
	query {
		users {
			id
			name
			email
			permissions
		}
	}
`;

const Permissions = (props) => (
	<Query query={ALL_USERS_QUERY}>
		{({ data, loading, error }) => (
			<div>
				<Error error={error} />
				<div>
					<h2>Manage Permssions</h2>
					<Table>
						<thead>
							<tr>
								<th>Name </th>
								<th>Email</th>
								{possiblePermissions.map((permission) => (
									<th key={permission}>{permission}</th>
								))}
								<th>👇</th>
							</tr>
						</thead>
						<tbody>
							{data.users.map((user) => (
								<UserPermissions user={user} key={user.id} />
							))}
						</tbody>
					</Table>
				</div>
			</div>
		)}
	</Query>
);

class UserPermissions extends React.Component {
	static propTypes = {
		user: PropTypes.shape({
			name: PropTypes.string,
			email: PropTypes.string,
			id: PropTypes.string,
			permissions: PropTypes.array
		}).isRequired
	};
	state = {
		permissions: this.props.user.permissions
	};
	handlePermissionChange = (e) => {
		const checkbox = e.target;
		// make copy of current permissions
		let updatedPermissions = [ ...this.state.permissions ];
		// check if permission is to be added or removed
		if (checkbox.checked) {
			// add permission
			updatedPermissions.push(checkbox.value);
		} else {
			updatedPermissions = updatedPermissions.filter(
				(permission) => permission !== checkbox.value
			);
		}
		this.setState({ permissions: updatedPermissions });
	};
	render() {
		const user = this.props.user;
		return (
			<Mutation
				mutation={UPDATE_PERMISSIONS_MUTATION}
				variables={{
					permissions: this.state.permissions,
					userId: this.props.user.id
				}}
			>
				{(updatedPermissions, { loading, error }) => (
					<div>
						{error && (
							<tr>
								<td>{user.name}</td>
								<td>{user.email}</td>
								{possiblePermissions.map((permission) => (
									<td key={permission}>
										<label
											htmlFor={`${user.id}-permission-${permission}`}
										>
											<input
												id={`${user.id}-permission-${permission}`}
												type="checkbox"
												checked={this.state.permissions.includes(
													permission
												)}
												value={permission}
												onChange={
													this.handlePermissionChange
												}
											/>
										</label>
									</td>
								))}
								<td>
									<SickButton
										type="button"
										disabled={loading}
										onClick={updatedPermissions}
									>
										Updat{
											loadiing ? 'ing' :
											'e'}
									</SickButton>
								</td>
							</tr>
						)}
					</div>
				)}
			</Mutation>
		);
	}
}
